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


def restore_database(client, file_name: str) -> Dict[str, Any]:
    """
    Initiate a restore from a backup file.

    Args:
        client: Scheduler0 client instance
        file_name: Backup file name (e.g. db-20260212-114810.db). When S3 is
            configured this is the S3 object key; otherwise a local file path.

    Returns:
        Response indicating restore has been initiated (includes status and requestId).

    Example:
        >>> result = restore_database(client, "db-20260212-114810.db")
        >>> print(result["data"]["status"])
        restore initiated
    """
    body = {"filePath": file_name}
    return client._request("POST", "cluster/restore", body=body)

