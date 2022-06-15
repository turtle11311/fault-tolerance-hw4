from __future__ import annotations
from array import array
import base64
from concurrent import futures
from csv import excel_tab
import imp
import logging
import json
import time
from unittest import result
import jsonschema
from random import Random
from typing import Dict, Tuple, List
import time
from google.protobuf.timestamp_pb2 import Timestamp

from nacl.signing import VerifyKey
from nacl.exceptions import ValueError, BadSignatureError
import grpc

from innerProto import inner_pb2_grpc
from innerProto import inner_pb2

from proto import voting_pb2
from proto import voting_pb2_grpc


class ElectionSpecError(Exception):
    def __init__(self, election_name: str) -> None:
        super().__init__()
        self.election_name = election_name
    def __str__(self) -> str:
        return "Election[{}] provide wrong parameters".format(self.election_name)

class InvalidElecitonNameError(Exception):
    def __init__(self, election_name: str) -> None:
        super().__init__()
        self.election_name = election_name
    def __str__(self) -> str:
        return "Election[{}] not exists".format(self.election_name)

class ElectionOngoingException(Exception):
    def __init__(self, election_name: str) -> None:
        super().__init__()
        self.election_name = election_name
    def __str__(self) -> str:
        return "Election[{}] still ongoing. election result is not available yet.".format(self.voter_name, self.election_name)

class VoterGroupError(Exception):
    def __init__(self, election_name: str, voter_name: str) -> None:
        super().__init__()
        self.election_name = election_name
        self.voter_name = voter_name
    def __str__(self) -> str:
        return "Voter[{}] isn't allow for election {}".format(self.voter_name, self.election_name)

class HasBeenVotedError(Exception):
    def __init__(self, election_name: str, voter_name: str) -> None:
        super().__init__()
        self.election_name = election_name
        self.voter_name = voter_name
    def __str__(self) -> str:
        return "Voter[{}] is casted before in election {}".format(self.voter_name, self.election_name)

class ElectionReplicaError(Exception):
    def __init__(self, election_name: str) -> None:
        super().__init__()
        self.election_name = election_name
    def __str__(self) -> str:
        return "{} replication failed".format(self.election_name)

class Voter():
    def __init__(self, name: str, group: str, pub_key: bytes) -> None:
        self.name = name
        self.group = group
        self.pub_key = pub_key
        
    class JSONEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Voter):
                return {'name': obj.name, 'group': obj.group, 'public_key': base64.b64encode(obj.pub_key).decode('utf-8')}
            # Let the base class default method raise the TypeError
            return json.JSONEncoder.default(self, obj)
    

class Election():
    def __init__(self, name: str, groups: array, choices: array, end_date: str) -> None:
        self.name = name
        self.groups = groups
        self.choices = choices
        self.end_date = end_date
        
    class JSONEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Election):
                return {'name': obj.name, 'groups': obj.groups, 'choices': obj.choices, 'end_date': obj.end_date}
            # Let the base class default method raise the TypeError
            return json.JSONEncoder.default(self, obj)

class ElectionList():
    def __init__(self, name: str,  choices: array, voterList: array) -> None:
        self.name = name
        self.choices = choices
        self.voterList = voterList
        
    class JSONEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Election):
                return {'name': obj.name,  'choices': obj.choices, 'voterList': obj.voterList}
            # Let the base class default method raise the TypeError
            return json.JSONEncoder.default(self, obj)

class ElectDataLoader():
    def __init__(self):
        #self.voter = Dict[str, Voter] = dict()
        self.elections: Dict[str, Election] = dict()
        self.electionList: Dict[str, ElectionList] = dict()
        

    def CreateElect(self, name: str, groups: array, choices: array, end_date: array):
        # election is existing error
        if name in self.elections:
            raise ElectionSpecError(name)
        # at least one group and one choice 
        if not len(groups) or not len(choices):
            raise ElectionSpecError(name)
        self.elections[name] = Election(name=name, groups=list(groups), choices=list(choices) ,end_date=str(end_date.ToJsonString()))
        dict_choices = dict.fromkeys(choices,0) # list convert to dict
        self.electionList[name] = ElectionList(name=name, choices=dict_choices ,voterList=[])

    def UpdateResultList(self, voter: Voter, election_name: str, choice_name: str):
        try:
            electios = self.elections[election_name]
            electioList = self.electionList[election_name]
            if voter.group not in electios.groups:
                raise VoterGroupError(election_name, voter.name)
            elif voter.name in electioList.voterList:
                raise HasBeenVotedError(election_name, voter.name)
            else:
                self.electionList[election_name].choices[choice_name]+=1
                self.electionList[election_name].voterList.append(voter.name)
        except KeyError:
            raise InvalidElecitonNameError(election_name)

            
    def GetResultList(self, election_name: str) -> List[Election]:
        if election_name not in self.elections:
            raise InvalidElecitonNameError(election_name)
        electioList = self.electionList[election_name]
        elecTime = Timestamp()
        CurrentTime = time.time()
        elecTime.FromJsonString(self.elections[election_name].end_date)
        if int(elecTime.seconds) > int(CurrentTime): 
            # The election is still ongoing. Election result is not available yet.
            return 2,[]
        result = electioList.choices
        return 0,result

    def Backup(self, code : int):
        backup = []
        for election in self.elections:
            count = []
            end_time = Timestamp()
            end_time.FromJsonString(self.elections[election].end_date)
            choice_list = self.electionList[election].choices
            for key in choice_list:
                count.append(inner_pb2.VoteCount(choice_name=key, count=choice_list[key]))
            backup.append(inner_pb2.ElectionStatus(
                name = self.electionList[election].name,
                groups = self.elections[election].groups,
                choices = self.elections[election].choices,
                count = count,
                voters =self.electionList[election].voterList,
                end_date = end_time
                ))
        return backup

    def Recovery(self, backup):
        for i in range(len(backup)):   
            choices = {}
            for k in backup[i].count:
                choices[k.choice_name] = k.count

            self.electionList[backup[i].name] = ElectionList(
                name = backup[i].name, 
                choices = choices ,
                voterList = list(backup[i].voters))

            self.elections[backup[i].name] = Election(
                name = backup[i].name, 
                groups = list(backup[i].groups), 
                choices = list(backup[i].choices) ,
                end_date = str(backup[i].end_date.ToJsonString()))

class eVotingReplica(inner_pb2_grpc.eVotingReplicaServicer):
    
    def CreateElect(self, elect_name: str, groups: array, choices: array, end_date: array):
        with grpc.insecure_channel('localhost:50052') as channel:
            try:
                Replica_stub = inner_pb2_grpc.eVotingReplicaStub(channel)
                Replica_status = Replica_stub.ElectionReplica(inner_pb2.Election(
                    name = elect_name,
                    groups = groups,
                    choices = choices,
                    end_date = end_date,
                ))
                if Replica_status.code == 2:
                    raise ElectionSpecError(elect_name)
                elif Replica_status.code != 0:
                    raise  ElectionReplicaError(elect_name)
            except grpc.RpcError as e:
                logging.error(e)

    def CastVote(self, voter: Voter, elect_name: str, choice_name: str):
        with grpc.insecure_channel('localhost:50052') as channel:
            try:
                Replica_stub = inner_pb2_grpc.eVotingReplicaStub(channel)
                Replica_status = Replica_stub.CastVoteReplica(inner_pb2.Vote(
                    election_name=elect_name,
                    choice_name =choice_name,
                ))
                if Replica_status.code == 2:
                    raise InvalidElecitonNameError(elect_name)
                elif Replica_status.code == 3:
                    raise VoterGroupError(elect_name, voter.name)
                elif Replica_status.code == 4:
                    raise HasBeenVotedError(elect_name, voter.name)
                elif Replica_status.code != 0:
                    raise  ElectionReplicaError(elect_name)
            except grpc.RpcError as e:
                logging.error(e)

        

class eVotingServer(voting_pb2_grpc.eVotingServicer, inner_pb2_grpc.eVotingReplicaServicer):
    def __init__(self) -> None:
        self.electDB = ElectDataLoader()
        self.replica = eVotingReplica()

    """ eVotingServicer """

    def CreateElection(self, request, context):
        status = 0
        try:
            #token = request.token.value
            #voter = self.authenticator.verify_token(token)
            self.replica.CreateElect(request.name, request.groups, request.choices, request.end_date)
            self.electDB.CreateElect(request.name, request.groups, request.choices, request.end_date)
        except ElectionSpecError as e:
            logging.warning(e)
            status = 2
        except Exception as e:
            logging.warning(e)
            # Unknown error
            status = 3
        except ElectionReplicaError as e:
            logging.warning(e)
            status = 4
        finally:
            return voting_pb2.Status(code=status)

    def CastVote(self, request, context):
        status = 0
        try:
            #token = request.token.value
            #voter = self.authenticator.verify_token(token)
            voter = Voter(name='Hello1',group='student',pub_key=123) # for test
            self.replica.CastVote(voter, request.election_name, request.choice_name)
            self.electDB.UpdateResultList(voter, request.election_name, request.choice_name)

        except InvalidElecitonNameError as e:
            logging.warning(e)
            status = 2
        except VoterGroupError as e:
            logging.warning(e)
            status = 3
        except HasBeenVotedError as e:
            logging.warning(e)
            status = 4
        except Exception as e:
            logging.warning(e.with_traceback())
            # Unknown error
            status = 5
        except ElectionReplicaError as e:
            logging.warning(e)
            status = 6
        finally:
            return voting_pb2.Status(code=status)

    def GetResult(self,request, context):
        status = 0
        try:
            status,GetResult_dic = self.electDB.GetResultList(request.name)
            count = []
            for key in GetResult_dic:
                count.append(voting_pb2.VoteCount(choice_name=key, count=GetResult_dic[key]))
        except InvalidElecitonNameError as e:
            logging.warning(e)
            status = 1
            count = []
        finally:
            return voting_pb2.ElectionResult( \
                status = status, \
                count = count)

    """ eVotingReplicaServicer """

    def ElectionReplica(self, request, context):
        status = 0
        try:
            logging.info("Server1 is backing up elections {}".format(request.name))
            self.electDB.CreateElect(request.name, request.groups, request.choices, request.end_date)
        except ElectionSpecError as e:
            logging.warning(e)
            status = 2
        except Exception as e:
            logging.warning(e)
            # Unknown error
            status = 3
        finally:
            return inner_pb2.Status(code=status)

    def CastVoteReplica(self, request, context):
        status = 0
        try:
            logging.info("Server1 is backing up voting")
            voter = Voter(name='Hello2',group='student',pub_key=123) # for test
            self.electDB.UpdateResultList(voter,request.election_name, request.choice_name)
        except InvalidElecitonNameError as e:
            logging.warning(e)
            status = 2
        except VoterGroupError as e:
            logging.warning(e)
            status = 3
        except HasBeenVotedError as e:
            logging.warning(e)
            status = 4
        except Exception as e:
            logging.warning(e.with_traceback())
            # Unknown error
            status = 5
        except ElectionReplicaError as e:
            logging.warning(e)
            status = 6
        finally:
            return inner_pb2.Status(code=status)

    def ElectionRecovery(self, request, context):  
        try:
            elections = request.elections
            print("Recovery server2")
            
        except Exception as e:
            logging.warning(e)
            return inner_pb2.Status(code = 0)
        finally:
            return inner_pb2.Status(code = 1)

    """ Recovery """

    def ElectionRecovery(self, request, context):  
        try:
            logging.info("Restoring Backup Server 2")
            backup = self.electDB.Backup(request.code)
            
        except Exception as e:
            logging.warning(e)
            #return inner_pb2.Elections(elections = backup)
        finally:
            return inner_pb2.Elections(elections = backup)

    def CheckRecovery(self):
        with grpc.insecure_channel('localhost:50052') as channel:
            try:
                status = 1
                inner_stub = inner_pb2_grpc.eVotingReplicaStub(channel)
                backup = inner_stub.ElectionRecovery(inner_pb2.Status(code = 1))
                #print(backup)
                self.electDB.Recovery(backup.elections)
                
            except grpc.RpcError as e:
                logging.error(" Server 2 Crash ")
                status = 0
            finally:
                if status:
                    logging.info(" Server 1 Online ")
                else:
                    logging.warning(" Server 1 Recovery Failed ")
 
    def serve(self):
        try:
            self.CheckRecovery()
            self._grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
            inner_pb2_grpc.add_eVotingReplicaServicer_to_server(self, self._grpc_server)
            voting_pb2_grpc.add_eVotingServicer_to_server(self, self._grpc_server)
            self._grpc_server.add_insecure_port('[::]:50051')
            self._grpc_server.start()
            self._grpc_server.wait_for_termination()
        except KeyboardInterrupt:
            pass