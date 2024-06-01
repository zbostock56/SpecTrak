import paramiko
import socket
import tempfile
import os

class FileIO:
    def __init__(
        self, username: str, password: str,
        private_key_path: str, remote_path: str,
        server_ip: str, server_port: int,
        local_path: str) -> None:
        """Creates an instance of the FileIO class.

        Args:
            username (str): username of the remote server.
            password (str): password of the remote server
            private_key_path (str): path to private key locally
            remote_path (str): file path of remote file to access
            server_ip (str): ip of server
            server_port (int): port to access
            local_path (str): file path to local file
        """
        self.username = username
        self.password = password
        self.private_key_path = private_key_path
        self.remote_path = remote_path
        self.remote_file_handle = None
        self.local_path = local_path
        self.local_file_handle = None
        self.server_ip = server_ip
        self.server_port = server_port
        self.temp_file_handle = None
        self.sftp_session = None
        self.ssh_session = None

    def _ping_check(self, timeout: int) -> bool:
        """Checks to see if server is online.

        Args:
            timeout (int): how long to wait for server to respond.

        Returns:
            bool: True if reponse, false otherwise.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            try:
                sock.connect((self.server_ip, self.server_port))
                return True
            except (socket.timeout, socket.error):
                return False

    def _get_remote_file_handle(self):
        """Gets a remote file handle for the remote file.
        """
        # Check to make sure the server is online
        if self._ping_check(2) is False:
            print(f"ERR: Server ping timeout! Server unavailable...")
            return

        self.ssh_session = paramiko.SSHClient()
        self.ssh_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if self.private_key_path is None:
                self.ssh_session.connect(
                    hostname=self.server_ip,
                    username=self.username,
                    password=self.password,
                    port=self.server_port
                )
            else:
                private_key = paramiko.RSAKey.from_private_key_file(
                    os.path.abspath(self.private_key_path)
                )
                self.ssh_session.connect(
                    hostname=self.server_ip,
                    username=self.username,
                    pkey=private_key,
                    port=self.server_port
                )

            self.sftp_session = self.ssh_session.open_sftp()
            self.remote_file_handle = self.sftp_session.open(
                self.remote_path, "r"
                )
            return
        except paramiko.AuthenticationException:
            print("Authentication failed, please verify your credentials")
            self._close_sessions()
        except paramiko.SSHException as sshException:
            print(f"Unable to establish SSH connection: {sshException}")
            self._close_sessions()
        except paramiko.BadHostKeyException as badHostKeyException:
            print(f"Unable to verify server's host key: {badHostKeyException}")
            self._close_sessions()
        except Exception as e:
            print(f"Operation error: {e}")
            self._close_sessions()

    def _close_remote_file_handle(self):
        """Closes remote file handle.
        """
        self.remote_file_handle.close()

    def _get_local_file_handle(self):
        """Gets a file handle to the local file.
        """
        try:
            self.local_file_handle = open(self.local_path, "r")
        except Exception as e:
            print(f"Local operation error: {e}")

    def _close_local_file_handle(self):
        """Closes local file handle.
        """
        try:
            self.local_file_handle.close()
        except Exception as e:
            print(f"Local operation error: {e}")


    def _get_temp_file_handle(self):
        """Gets temporary file handle.
        """
        try:
            self.temp_file_handle = tempfile.NamedTemporaryFile(
                delete=False,
                delete_on_close=True
                )
        except Exception as e:
            print(f"Temporary file error: {e}")

    def _close_temp_file_handle(self):
        """Closes temporary file.
        """
        try:
            self.temp_file_handle.close()
        except Exception as e:
            print(f"Temporary file error: {e}")

    def _close_sessions(self):
        """Helper function to close the remote connections.
        """
        if self.sftp_session is not None:
                self.sftp_session.close()
        if self.ssh_session is not None:
            self.ssh_session.close()
