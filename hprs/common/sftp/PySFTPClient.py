# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import paramiko
from hprs.common.crypto.AES256 import AES256
from hprs.common.sftp.PySFTPAuthException import PySFTPAuthException


class PySFTPClient(object):
    # class : PySFTPClient
    def __init__(self, host: str, port: int, username: str, password: str):
        try:
            self.transport = paramiko.Transport((host, port))
            self.transport.connect(username=AES256().decrypt(username), password=AES256().decrypt(password))
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        except paramiko.ssh_exception.AuthenticationException:
            raise PySFTPAuthException

    def open(self, filename, option="r", ) -> paramiko.SFTPFile:
        return self.sftp.open(filename, option)

    def rename(self, src, dst) -> None:
        self.sftp.rename(src, dst)

    def close(self) -> None:
        self.sftp.close()
        self.transport.close()

    def remove(self, filename) -> None:
        self.sftp.remove(filename)

    def is_exist(self, filename) -> bool:
        try:
            self.sftp.stat(filename)
            return True
        except FileNotFoundError:
            return False
