# CXPBU CustomerMS

## Overview

CXPBU CustomerMS is a microservice responsible for managing customer account APIs. It provides access to customer account information and serves as part of the middleware layer between the Portal and backend data systems.

## Key Facts

- **Responsibility**: Customer account APIs (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Scope**: Account information management and retrieval (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Integration**: Acts as intermediary between Portal Backend and CXPBU CADMS / Dynamics (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Use Cases**: Account metadata updates, contact management, account lookups (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)

## Integration Points

- **Input**: Portal Backend
- **Data Store**: Works with CXPBU CADMS and Dynamics
- **Output**: Account data responses, confirmation of updates


## Relationships
- **part-of**: [Participating Systems](wiki/comparisons/participating-systems.md)
- **related-to**: [CXPBU CADMS](wiki/entities/cxpbu-cadms.md)

## See Also
- [CXPBU CADMS](wiki/entities/cxpbu-cadms.md)
- [CXPBU OrderMS](wiki/entities/cxpbu-orderms.md)
- [Account Level Changes](wiki/entities/account-level-changes.md)