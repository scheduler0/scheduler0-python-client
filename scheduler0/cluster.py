"""
Raft cluster management operations for Scheduler0.

These endpoints operate on Raft cluster membership and are only meaningful when
self-hosting Scheduler0. They require a credential carrying the ``admin`` scope,
or Basic/peer authentication.

The membership and leadership operations return ``{"success": true, "data":
{"status": "..."}}``; the ``dump_*`` helpers return raw diagnostic payloads.
"""

from typing import Optional
from .client import Client


def remove_self_from_cluster(self: Client, account_id_override: Optional[str] = None) -> dict:
    """
    Remove this node from Raft membership and unregister it from etcd.

    POST /cluster/remove-self
    """
    return self._post("/cluster/remove-self", account_id_override=account_id_override)


def add_self_to_cluster(self: Client, account_id_override: Optional[str] = None) -> dict:
    """
    Ensure this node is registered in etcd and part of the Raft cluster.

    POST /cluster/add-self
    """
    return self._post("/cluster/add-self", account_id_override=account_id_override)


def force_rebuild_cluster(
    self: Client,
    seed_node_id: str,
    account_id_override: Optional[str] = None,
) -> dict:
    """
    Force a rebuild of the Raft cluster. Should only be called on the seed node.

    POST /cluster/force-rebuild?seedNodeId=

    Args:
        seed_node_id: Node ID of the seed node to rebuild around (required).
    """
    return self._post(
        "/cluster/force-rebuild",
        params={"seedNodeId": str(seed_node_id)},
        account_id_override=account_id_override,
    )


def reset_raft(self: Client, account_id_override: Optional[str] = None) -> dict:
    """
    Clear local Raft state on this node.

    POST /cluster/reset-raft

    The server sends its response and then exits its own process, so the
    connection is expected to drop immediately afterwards.
    """
    return self._post("/cluster/reset-raft", account_id_override=account_id_override)


def remove_cluster_node(
    self: Client,
    node_id: str,
    account_id_override: Optional[str] = None,
) -> dict:
    """
    Remove a node from the Raft cluster. Leader-only; returns 403 otherwise.

    POST /cluster/remove-node?nodeId=
    """
    return self._post(
        "/cluster/remove-node",
        params={"nodeId": str(node_id)},
        account_id_override=account_id_override,
    )


def add_cluster_node(
    self: Client,
    node_id: str,
    node_address: str,
    client_address: str,
    account_id_override: Optional[str] = None,
) -> dict:
    """
    Add a node to the Raft cluster. Leader-only; returns 403 otherwise.

    POST /cluster/add-node?nodeId=&nodeAddress=&clientAddress=

    All three query parameters are required by the server.
    """
    return self._post(
        "/cluster/add-node",
        params={
            "nodeId": str(node_id),
            "nodeAddress": node_address,
            "clientAddress": client_address,
        },
        account_id_override=account_id_override,
    )


def promote_cluster_node(
    self: Client,
    node_id: str,
    account_id_override: Optional[str] = None,
) -> dict:
    """
    Promote a non-voter node to voter. Leader-only; returns 403 otherwise.

    POST /cluster/promote-node?nodeId=
    """
    return self._post(
        "/cluster/promote-node",
        params={"nodeId": str(node_id)},
        account_id_override=account_id_override,
    )


def demote_cluster_node(
    self: Client,
    node_id: str,
    account_id_override: Optional[str] = None,
) -> dict:
    """
    Demote a voter node to non-voter. Leader-only; returns 403 otherwise.

    POST /cluster/demote-node?nodeId=
    """
    return self._post(
        "/cluster/demote-node",
        params={"nodeId": str(node_id)},
        account_id_override=account_id_override,
    )


def transfer_cluster_leadership(self: Client, account_id_override: Optional[str] = None) -> dict:
    """
    Transfer Raft leadership to another node. Leader-only; returns 403 otherwise.

    POST /cluster/transfer-leadership
    """
    return self._post("/cluster/transfer-leadership", account_id_override=account_id_override)


def list_cluster_nodes(self: Client, account_id_override: Optional[str] = None) -> dict:
    """
    List all nodes in the Raft cluster.

    GET /cluster/list-nodes
    """
    return self._get("/cluster/list-nodes", params=None, account_id_override=account_id_override)


def dump_schedule_queue(self: Client, account_id_override: Optional[str] = None) -> dict:
    """
    Dump the in-memory schedule queue (diagnostics).

    GET /cluster/dump/schedule-queue
    """
    return self._get(
        "/cluster/dump/schedule-queue", params=None, account_id_override=account_id_override
    )


def dump_job_executions_cache(self: Client, account_id_override: Optional[str] = None) -> dict:
    """
    Dump the job-executions cache, keyed by job id (diagnostics).

    GET /cluster/dump/job-executions-cache
    """
    return self._get(
        "/cluster/dump/job-executions-cache", params=None, account_id_override=account_id_override
    )


def dump_job_queues(self: Client, account_id_override: Optional[str] = None) -> dict:
    """
    Dump all job queues (diagnostics).

    GET /cluster/dump/job-queues
    """
    return self._get(
        "/cluster/dump/job-queues", params=None, account_id_override=account_id_override
    )


def dump_job_queue_versions(self: Client, account_id_override: Optional[str] = None) -> dict:
    """
    Dump all job queue versions (diagnostics).

    GET /cluster/dump/job-queue-versions
    """
    return self._get(
        "/cluster/dump/job-queue-versions", params=None, account_id_override=account_id_override
    )


# Attach methods to Client class
Client.remove_self_from_cluster = remove_self_from_cluster
Client.add_self_to_cluster = add_self_to_cluster
Client.force_rebuild_cluster = force_rebuild_cluster
Client.reset_raft = reset_raft
Client.remove_cluster_node = remove_cluster_node
Client.add_cluster_node = add_cluster_node
Client.promote_cluster_node = promote_cluster_node
Client.demote_cluster_node = demote_cluster_node
Client.transfer_cluster_leadership = transfer_cluster_leadership
Client.list_cluster_nodes = list_cluster_nodes
Client.dump_schedule_queue = dump_schedule_queue
Client.dump_job_executions_cache = dump_job_executions_cache
Client.dump_job_queues = dump_job_queues
Client.dump_job_queue_versions = dump_job_queue_versions
