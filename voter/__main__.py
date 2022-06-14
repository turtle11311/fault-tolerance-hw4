from __future__ import print_function
import base64
from os import path
from google.protobuf.timestamp_pb2 import Timestamp
from nacl.public import PrivateKey
from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import Base64Encoder
from google.protobuf.timestamp_pb2 import Timestamp
import logging
import grpc
from innerProto import inner_pb2
from innerProto import inner_pb2_grpc

from proto import voting_pb2
from proto import voting_pb2_grpc

voter_name = 'Hello'

def test_server1():
    #key_loader = KeyLoader('voter_key')
    #logging.debug('verifykey: {}'.format(key_loader.verify_key.encode(encoder=Base64Encoder).decode('utf-8')))
    print('\n =========== Test Server1 ===========')
    with grpc.insecure_channel('localhost:50051') as channel:
        try:
            print('\n【Test "CreateElection" function】')
            #Election_stub = inner_pb2_grpc.eVotingReplicaStub(channel)
            Election_stub = voting_pb2_grpc.eVotingStub(channel)
            end_time = Timestamp()
            end_time.FromJsonString('2023-01-01T00:00:00Z')
            election_status = Election_stub.CreateElection(voting_pb2.Election(
                name='Election1',
                groups=['teacher'],
                choices=['number1','number2'],
                end_date=end_time,
               ))

            end_time = Timestamp()
            end_time.FromJsonString('2022-01-01T00:00:00Z')
            election_status = Election_stub.CreateElection(voting_pb2.Election(
                name='Election2',
                groups=['student'],
                choices=['number1','number2'],
                end_date=end_time,
                ))

            if election_status.code==0:
                print('-> Test "Election create" success!')
                logging.info('Election created successfully')

            election_status = Election_stub.CreateElection(voting_pb2.Election(
                name='Election1',
                groups=[],
                choices=[],
                end_date=end_time,
                ))
            if election_status.code==2:
                print('-> Test "Missing groups or choices" success!')
                logging.warning('Missing groups or choices specification')

        except grpc.RpcError as e:
            logging.error(e)


        try:
            print('\n【Test "CastVote" function】')
            CastVote_stub = voting_pb2_grpc.eVotingStub(channel)
            castVote_status = CastVote_stub.CastVote(voting_pb2.Vote(
                election_name='Election2',
                choice_name ='number1',
                ))
            if castVote_status.code==0:
                print('-> Test "successful vote" success!')
                logging.info('Successful vote')
            
            CastVote_stub = voting_pb2_grpc.eVotingStub(channel)
            castVote_status = CastVote_stub.CastVote(voting_pb2.Vote(
                election_name='Election1000',
                choice_name ='number1',
                ))
            if castVote_status.code==2:
                print('-> Test "Invalid election name" success!')
                logging.warning('Invalid election name')
           
            CastVote_stub = voting_pb2_grpc.eVotingStub(channel)
            castVote_status = CastVote_stub.CastVote(voting_pb2.Vote(
                election_name='Election1',
                choice_name ='number1',
               ))
            if castVote_status.code==3:
                print('-> Test "wrong group" success!')
                logging.warning('The voter’s group is not allowed in the election')
           
            CastVote_stub = voting_pb2_grpc.eVotingStub(channel)
            castVote_status = CastVote_stub.CastVote(voting_pb2.Vote(
                election_name='Election2',
                choice_name ='number1',
                ))
            if castVote_status.code==4:
                print('-> Test "already voted" success!')
                logging.warning('A previous vote has been cast.')
        except grpc.RpcError as e:
            logging.error(e)

        try:
            print('\n【Test "GetResult" function】')
            GetResult_stub = voting_pb2_grpc.eVotingStub(channel)
            getResult = GetResult_stub.GetResult(voting_pb2.ElectionName(name='Election2'))
            if getResult.status:
                logging.warning('Non-existent election or The election is still ongoing. Election result is not available yet')
            else:
                print('-> Test "The list of choices and the ballot counts" success!')
                for i in range(len(getResult.count)):
                    print('choice name [{}] : {}'.format(getResult.count[i].choice_name, getResult.count[i].count))

            getResult = GetResult_stub.GetResult(voting_pb2.ElectionName(name='Election1'))
            if getResult.status==2:
                print('-> Test "Election result is not available yet" success!')
                logging.warning('The election is still ongoing. Election result is not available yet')
            
            getResult = GetResult_stub.GetResult(voting_pb2.ElectionName(name='Election3'))
            if getResult.status==1:
                print('-> Test "Non-existent election" success!')
                logging.warning('Non-existent election ')
            
        except grpc.RpcError as e:
            logging.error(e)

    

def test_server2():
    print('\n =========== Test Server2 ===========')
    with grpc.insecure_channel('localhost:50052') as channel:
        try:
            print('\n【Test "CreateElection" function】')
            #Election_stub = inner_pb2_grpc.eVotingReplicaStub(channel)
            Election_stub = voting_pb2_grpc.eVotingStub(channel)
            end_time = Timestamp()
            end_time.FromJsonString('2022-01-01T00:00:00Z')
            election_status = Election_stub.CreateElection(voting_pb2.Election(
                name='Election3',
                groups=['student'],
                choices=['number1','number2'],
                end_date=end_time,
                ))

            if election_status.code==0:
                print('-> Test "Election create" success!')
                logging.info('Election created successfully')

            election_status = Election_stub.CreateElection(voting_pb2.Election(
                name='Election1',
                groups=[],
                choices=[],
                end_date=end_time,
                ))
            if election_status.code==2:
                print('-> Test "Missing groups or choices" success!')
                logging.warning('Missing groups or choices specification')

        except grpc.RpcError as e:
            logging.error(e)


        try:
            print('\n【Test "CastVote" function】')
            CastVote_stub = voting_pb2_grpc.eVotingStub(channel)
            castVote_status = CastVote_stub.CastVote(voting_pb2.Vote(
                election_name='Election2',
                choice_name ='number1',
                ))
            if castVote_status.code==0:
                print('-> Test "successful vote" success!')
                logging.info('Successful vote')
            
            CastVote_stub = voting_pb2_grpc.eVotingStub(channel)
            castVote_status = CastVote_stub.CastVote(voting_pb2.Vote(
                election_name='Election1000',
                choice_name ='number1',
                ))
            if castVote_status.code==2:
                print('-> Test "Invalid election name" success!')
                logging.warning('Invalid election name')
           
            CastVote_stub = voting_pb2_grpc.eVotingStub(channel)
            castVote_status = CastVote_stub.CastVote(voting_pb2.Vote(
                election_name='Election1',
                choice_name ='number1',
               ))
            if castVote_status.code==3:
                print('-> Test "wrong group" success!')
                logging.warning('The voter’s group is not allowed in the election')
           
            CastVote_stub = voting_pb2_grpc.eVotingStub(channel)
            castVote_status = CastVote_stub.CastVote(voting_pb2.Vote(
                election_name='Election2',
                choice_name ='number1',
                ))
            if castVote_status.code==4:
                print('-> Test "already voted" success!')
                logging.warning('A previous vote has been cast.')
        except grpc.RpcError as e:
            logging.error(e)

        try:
            print('\n【Test "GetResult" function】')
            GetResult_stub = voting_pb2_grpc.eVotingStub(channel)
            getResult = GetResult_stub.GetResult(voting_pb2.ElectionName(name='Election2'))
            if getResult.status:
                logging.warning('Non-existent election or The election is still ongoing. Election result is not available yet')
            else:
                print('-> Test "The list of choices and the ballot counts" success!')
                for i in range(len(getResult.count)):
                    print('choice name [{}] : {}'.format(getResult.count[i].choice_name, getResult.count[i].count))

            getResult = GetResult_stub.GetResult(voting_pb2.ElectionName(name='Election1'))
            if getResult.status==2:
                print('-> Test "Election result is not available yet" success!')
                logging.warning('The election is still ongoing. Election result is not available yet')
            
            getResult = GetResult_stub.GetResult(voting_pb2.ElectionName(name='Election3'))
            if getResult.status==1:
                print('-> Test "Non-existent election" success!')
                logging.warning('Non-existent election ')
            
        except grpc.RpcError as e:
            logging.error(e)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_server1()
    test_server2()
    
    