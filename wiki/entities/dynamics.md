# Dynamics

## Overview

Dynamics is the order orchestration system of record for the Business Portal. It maintains authoritative customer account data, service contracts, and executes orchestration for Global Change Orders. Dynamics is the central authority for account, contact, and billing address information.

## Key Facts

- **Role**: Order orchestration system of record (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Scope**: Customer accounts, service contracts, change orders, order execution (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Data Authority**: Source of truth for account information, contacts, billing addresses, and contract data (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Integration**: Hub for all Global Change Order processing and service provisioning (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)

## Integration Points

- **Inbound**: Global Change Orders from OrderMS, Portal Backend requests
- **Outbound**: Contract data, account data, order status updates
- **Provisioning**: Coordinates with Shazam and NetBox for network provisioning
- **Notifications**: Future integration with Ziply Notification Platform

## Data Ownership

| Data | Owner |
|------|-------|
| Account | Dynamics |
| Contacts | Dynamics |
| Billing Address | Dynamics |


## Relationships
- **part-of**: [Participating Systems](wiki/comparisons/participating-systems.md)
- **related-to**: [GCO Lifecycle](wiki/concepts/gco-lifecycle.md)

## See Also
- [Global Change Order](wiki/entities/global-change-order.md)
- [CXPBU OrderMS](wiki/entities/cxpbu-orderms.md)
- [Shazam](wiki/entities/shazam.md)
- [NetBox](wiki/entities/netbox.md)