"""
Backup and restore operations for Scheduler0.
"""

from typing import Dict, Any


def backup_database(client) -> Dict[str, Any]:
    """
    Initiate an automatic timestamped backup.

    Args:
        client: Scheduler0 client instance

    Returns:
        Response indicating backup has been initiated

    Example:
        >>> result = backup_database(client)
        >>> print(result["data"]["status"])
        backup initiated
    """
    return client._request("POST", "cluster/backup")


def backup_database_to_file(client, dest_path: str) -> Dict[str, Any]:
    """
    Initiate a backup to a specific file path.

    Args:
        client: Scheduler0 client instance
        dest_path: Destination path for the backup file

    Returns:
        Response indicating backup to file has been initiated

    Example:
        >>> result = backup_database_to_file(client, "/path/to/backup.db")
        >>> print(result["data"]["status"])
        backup to file initiated
    """
    body = {"destPath": dest_path}
    return client._request("POST", "cluster/backup-to-file", body=body)


def restore_database(client, backup_path: str) -> Dict[str, Any]:
    """
    Initiate a restore from a backup file.

    Args:
        client: Scheduler0 client instance
        backup_path: Path to the backup file to restore from

    Returns:
        Response indicating restore has been initiated

    Example:
        >>> result = restore_database(client, "/path/to/backup.db")
        >>> print(result["data"]["status"])
        restore initiated
    """
    body = {"backupPath": backup_path}
    return client._request("POST", "cluster/restore", body=body)


def get_backup_restore_progress(client) -> Dict[str, Any]:
    """
    Get the current backup/restore progress.

    Args:
        client: Scheduler0 client instance

    Returns:
        Progress information including status, progress percentage, and message

    Example:
        >>> progress = get_backup_restore_progress(client)
        >>> print(f"{progress['data']['status']}: {progress['data']['progress']}%")
        in-progress: 45%
        >>> print(progress['data']['message'])
        Backing up: 4500/10000 rows (45.0%)
    """
    return client._request("GET", "cluster/backup-restore-progress")

