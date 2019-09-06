import pysftp as sftp
import get_templates


def get_set_files_from_server(remote_path, conn_string):
    cnopts = sftp.CnOpts()
    cnopts.hostkeys = None
    s = sftp.Connection(host=conn_string['host'],
                        username=conn_string['username'],
                        password=conn_string['password'],
                        port=conn_string['port'],
                        cnopts=cnopts)
    # Switch to a remote directoryself._sftp.chdir(remotepath)
    s.cwd(remote_path)
    # Obtain structure of the remote directory '/var/www/vhosts'
    directory_structure = s.listdir_attr()
    files_from_server = [file.filename
                             for file in directory_structure
                             if str(file.filename).isdigit() is True]
    return files_from_server


def remove_files_from_server(files_to_remove, remote_path, conn_string):
    cnopts = sftp.CnOpts()
    cnopts.hostkeys = None
    s = sftp.Connection(host=conn_string['host'],
                        username=conn_string['username'],
                        password=conn_string['password'],
                        port=conn_string['port'],
                        cnopts=cnopts)
    for file_name in files_to_remove:
        s.remove(remote_path + file_name)
    s.close()


dc1 = {'sftp_conn_string': {'host': '',
                            'username': '',
                            'password': '',
                            'port': 22},
       'remote_files_path': ''}
dc2 = {'sftp_conn_string': {'host': '',
                            'username': '',
                            'password': '',
                            'port': 22},
       'remote_files_path': ''}
dcs = {'dc1': dc1, 'dc2': dc2}

set_of_templates = set(get_templates.set_of_files)
set_of_files_attr_from_server = set(get_set_files_from_server(dcs['dc1']['remote_files_path'],
                                                              dcs['dc1']['sftp_conn_string']))
set_of_files_to_remove = set(set_of_files_attr_from_server.difference(set_of_templates))

for key, value in dcs.items():
    remove_files_from_server(set_of_files_to_remove,
                             dcs[key]['remote_files_path'],
                             dcs[key]['sftp_conn_string'])
