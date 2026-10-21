# Shazam

## Overview

Shazam is the network provisioning system responsible for IP address assignment and network service provisioning. It maintains the authoritative record of IP assignments for customers and coordinates with NetBox for network inventory management.

## Key Facts

- **Role**: Network provisioning system (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Scope**: IP address assignment, service provisioning (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Data**: IP blocks, assignment status (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Integration**: Receives provisioning instructions from Dynamics, coordinates with NetBox (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)

## Integration Points

- **Input**: Dynamics (provisioning orders)
- **Coordination**: Works with NetBox for inventory management
- **Output**: IP assignment confirmations, provisioning status

## Data Ownership

| Data | Owner |
|------|-------|
| IP Assignment | Shazam |


## Relationships
- **part-of**: [Participating Systems](wiki/comparisons/participating-systems.md)
- **related-to**: [NetBox](wiki/entities/netbox.md)

## See Also
- [NetBox](wiki/entities/netbox.md)
- [Static IP Changes](wiki/entities/static-ip-changes.md)
- [Dynamics](wiki/entities/dynamics.md)