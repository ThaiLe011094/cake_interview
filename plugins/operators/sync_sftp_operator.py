def sync_sftp_files(**kwargs):
    from hooks.sftp_hook import SFTPSyncHook

    source_hook = SFTPSyncHook(ssh_conn_id='source_sftp_conn')
    target_hook = SFTPSyncHook(ssh_conn_id='target_sftp_conn')
    source_hook.sync(target_hook)
