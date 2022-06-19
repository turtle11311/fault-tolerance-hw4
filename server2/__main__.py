#!/usr/bin/env python3

from server.server import eVotingServer
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    srv = eVotingServer("localhost:50002", ["localhost:50001"])
    srv.serve()