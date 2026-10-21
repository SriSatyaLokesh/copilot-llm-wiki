# NetBox

## Overview

NetBox is the Network IPAM (IP Address Management) system responsible for maintaining the authoritative network inventory and IP allocation records. It works in conjunction with Shazam to ensure IP assignments are accurately tracked and managed.

## Key Facts

- **Role**: Network IPAM (IP Address Management) (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Scope**: Network inventory, IP allocation records (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Data**: IP blocks, network configuration, allocation tracking (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Integration**: Receives provisioning updates from Shazam, maintains inventory records (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)

## Integration Points

- **Input**: Shazam (provisioning updates)
- **Coordination**: Works with Shazam for IP assignment
- **Output**: Inventory data, allocation confirmations

## Data Ownership

| Data | Owner |
|------|-------|
| Network Inventory | NetBox |


## Relationships
- **part-of**: [Participating Systems](wiki/comparisons/participating-systems.md)
- **related-to**: [Shazam](wiki/entities/shazam.md)

## See Also
- [Shazam](wiki/entities/shazam.md)
- [Static IP Changes](wiki/entities/static-ip-changes.md)
- [Dynamics](wiki/entities/dynamics.md)