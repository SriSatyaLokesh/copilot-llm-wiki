# CXPBU CADMS

## Overview

CXPBU CADMS (Customer Account Data Management System) is a microservice responsible for managing and persisting customer account data. It serves as a data intermediary between the Portal Backend and Dynamics, ensuring data consistency and providing access to customer account information.

## Key Facts

- **Responsibility**: Customer account data management (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Scope**: Data persistence, retrieval, and update coordination (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Integration**: Works with CustomerMS and Dynamics (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Data Ownership**: Coordinates with Dynamics (system of record for accounts and contacts) (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)

## Integration Points

- **Input**: CustomerMS, Portal Backend requests
- **Data Store**: Interfaces with Dynamics (source of truth)
- **Output**: Account data responses, update confirmations


## Relationships
- **part-of**: [Participating Systems](wiki/comparisons/participating-systems.md)
- **related-to**: [CXPBU CustomerMS](wiki/entities/cxpbu-customerms.md)

## See Also
- [CXPBU CustomerMS](wiki/entities/cxpbu-customerms.md)
- [CXPBU OrderMS](wiki/entities/cxpbu-orderms.md)
- [Dynamics](wiki/entities/dynamics.md)
- [Account Level Changes](wiki/entities/account-level-changes.md)