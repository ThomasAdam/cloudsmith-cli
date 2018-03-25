"""API - entitlements endpoints."""
from __future__ import absolute_import, print_function, unicode_literals

import cloudsmith_api

from .. import ratelimits
from ..pagination import PageInfo
from .exceptions import catch_raise_api_exception
from .init import get_api_client


def get_entitlements_api():
    """Get the entitlements API client."""
    return get_api_client(cloudsmith_api.EntitlementsApi)


def list_entitlements(owner, repo, page, page_size, show_tokens):
    """Get a list of entitlements on a repository."""
    client = get_entitlements_api()

    with catch_raise_api_exception():
        data, _, headers = client.entitlements_list_with_http_info(
            owner=owner,
            repo=repo,
            page=page,
            page_size=page_size,
            show_tokens=show_tokens
        )

    ratelimits.maybe_rate_limit(client, headers)
    page_info = PageInfo.from_headers(headers)
    entitlements = [ent.to_dict() for ent in data]
    return entitlements, page_info


def create_entitlement(owner, repo, name, token, show_tokens):
    """Create an entitlement in a repository."""
    client = get_entitlements_api()

    data = {}
    if name is not None:
        data['name'] = name

    if token is not None:
        data['token'] = token

    with catch_raise_api_exception():
        data, _, headers = client.entitlements_create_with_http_info(
            owner=owner,
            repo=repo,
            data=data,
            show_tokens=show_tokens
        )

    ratelimits.maybe_rate_limit(client, headers)
    return data.to_dict()


def delete_entitlement(owner, repo, slug_perm):
    """Delete an entitlement from a repository."""
    client = get_entitlements_api()

    with catch_raise_api_exception():
        _, _, headers = client.entitlements_delete_with_http_info(
            owner=owner,
            repo=repo,
            slug_perm=slug_perm
        )

    ratelimits.maybe_rate_limit(client, headers)


def update_entitlement(owner, repo, slug_perm, name, token, show_tokens):
    """Update an entitlement in a repository."""
    client = get_entitlements_api()

    data = {}
    if name is not None:
        data['name'] = name

    if token is not None:
        data['token'] = token

    with catch_raise_api_exception():
        data, _, headers = client.entitlements_partial_update_with_http_info(
            owner=owner,
            repo=repo,
            slug_perm=slug_perm,
            data=data,
            show_tokens=show_tokens
        )

    ratelimits.maybe_rate_limit(client, headers)
    return data.to_dict()


def refresh_entitlement(owner, repo, slug_perm, show_tokens):
    """Refresh an entitlement in a repository."""
    client = get_entitlements_api()

    with catch_raise_api_exception():
        data, _, headers = client.entitlements_refresh_with_http_info(
            owner=owner,
            repo=repo,
            slug_perm=slug_perm,
            show_tokens=show_tokens
        )

    ratelimits.maybe_rate_limit(client, headers)
    return data.to_dict()


def sync_entitlements(owner, repo, source, show_tokens):
    """Sync entitlements from another repository."""
    client = get_entitlements_api()

    with catch_raise_api_exception():
        data, _, headers = client.entitlements_sync_with_http_info(
            owner=owner,
            repo=repo,
            data={
                'source': source,
            },
            show_tokens=show_tokens
        )

    ratelimits.maybe_rate_limit(client, headers)
    page_info = PageInfo.from_headers(headers)
    entitlements = [ent.to_dict() for ent in data.tokens]
    return entitlements, page_info
