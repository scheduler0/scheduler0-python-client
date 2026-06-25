"""
Backup and restore operations for Scheduler0.

These are self-hosting cluster endpoints and require Basic Authentication.
"""

from typing import Optional
from .client import Client


def backup_database(self: Client, account_id_override: Optional[str] = None) -> dict:
    """
    Initiate an automatic timestamped database backup.

    POST /cluster/backup

    Returns:
        Response indicating the backup has been initiated.

    Example:
        >>> result = client.backup_database()
        >>> print(result["data"]["status"])
        backup initiated
    """
    return self._post("/cluster/backup", account_id_override=account_id_override)


def restore_database(
    self: Client,
    file_name: str,
    account_id_override: Optional[str] = None,
) -> dict:
    """
    Initiate a restore from a backup file.

    POST /cluster/restore

    Args:
        file_name: Backup file name (e.g. db-20260212-114810.db). When S3 is
            configured this is the S3 object key; otherwise a local file path.

    Returns:
        Response indicating the restore has been initiated (includes status and requestId).

    Example:
        >>> result = client.restore_database("db-20260212-114810.db")
        >>> print(result["data"]["status"])
        restore initiated
    """
    body = {"filePath": file_name}
    return self._post("/cluster/restore", body, account_id_override=account_id_override)


# Attach methods to Client class
Client.backup_database = backup_database
Client.restore_database = restore_database
