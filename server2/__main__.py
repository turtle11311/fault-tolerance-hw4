#!/usr/bin/env python3

from server2.server2 import eVotingServer
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    srv = eVotingServer()
    srv.serve()