from airflow.providers.sftp.hooks.sftp import SFTPHook
import os
from typing import List, Tuple
import logging

class SFTPSyncHook(SFTPHook):
    """Custom hook extending SFTPHook for recursive SFTP synchronization."""
    def __init__(self, ssh_conn_id: str):
        super().__init__(ssh_conn_id=ssh_conn_id)
        self.logger = logging.getLogger(__name__)

    def list_files_recursive(self, sftp, path: str = '.') -> List[Tuple[str, str]]:
        """List all files recursively with their relative paths."""
        files = []
        try:
            items = sftp.listdir_attr(path)
            for item in items:
                item_path = f"{path}/{item.filename}"
                if item.st_mode & 0o40000:  # Directory
                    files.extend(self.list_files_recursive(sftp, item_path))
                else:
                    relative_path = item_path.lstrip('/')
                    files.append((relative_path, item_path))
        except Exception as e:
            self.logger.error(f"Error listing files at {path}: {str(e)}")
            raise
        return files

    def ensure_directory(self, sftp, path: str):
        """Create directory structure if it doesn't exist."""
        try:
            sftp.stat(path)
        except IOError:
            parts = path.split('/')
            current = ''
            for part in parts:
                if part:
                    current = f"{current}/{part}" if current else part
                    try:
                        sftp.stat(current)
                    except IOError:
                        sftp.mkdir(current)

    def sync_file(self, source_sftp, target_sftp, target_hook: 'SFTPSyncHook', source_path: str, target_path: str):
        """Transfer a single file from source to target."""
        try:
            try:
                target_stat = target_sftp.stat(target_path)
                source_stat = source_sftp.stat(source_path)
                if target_stat.st_size == source_stat.st_size:
                    self.logger.info(f"Skipping {target_path} - already exists with same size")
                    return
            except IOError:
                pass

            target_hook.ensure_directory(target_sftp, os.path.dirname(target_path))

            temp_file = f"/tmp/{os.path.basename(source_path)}"
            self.logger.info(f"Downloading {source_path} to {temp_file}")
            source_sftp.get(source_path, temp_file)
            self.logger.info(f"Transferring {temp_file} to {target_path}")
            target_sftp.put(temp_file, target_path)
            os.remove(temp_file)
            self.logger.info(f"Transferred {source_path} to {target_path}")
        except Exception as e:
            self.logger.error(f"Error transferring {source_path}: {str(e)}")
            raise

    def sync(self, target_hook: 'SFTPSyncHook'):
        """Sync all files from source to target SFTP server."""
        try:
            with self.get_conn() as source_sftp, target_hook.get_conn() as target_sftp:
                files = self.list_files_recursive(source_sftp)
                for relative_path, full_path in files:
                    self.logger.info('Begin syncing')
                    self.sync_file(
                        source_sftp,
                        target_sftp,
                        target_hook,
                        full_path,
                        relative_path
                    )
        except Exception as e:
            self.logger.error(f"Sync failed: {str(e)}")
            raise
