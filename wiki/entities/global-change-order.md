# Global Change Order

## Overview

Global Change Orders (GCO) are a core feature of the Business Portal that enable customers to modify their account information, service configurations, contacts, and IP assignments through the customer portal interface. Any modification initiated on an active account or service generates a GCO request, which is submitted to Dynamics for order orchestration.

## Key Facts

- **Scope**: Covers account metadata changes, static IP modifications, and service-level changes (upgrades, downgrades, add-ons, disconnections) (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Workflow**: Initiated by customer via portal → Validated by middleware → Pricing evaluated → Submitted to Dynamics → Processing → Completed or Rejected (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Systems Involved**: Portal UI/Backend, CXPBU microservices (OrderMS, CustomerMS, CADMS), Dynamics, Shazam, NetBox, Catalog DB (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Pricing Integration**: OrderMS compares current pricing with rate cards; price increases are automated, price decreases require sales review (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **ETF Calculation**: Early Termination Fees calculated for service disconnections during contract period (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Authorization**: Role-based permissions control which operations customers can perform (Account Owner, Account Admin, Standard User) (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)

## Lifecycle States

1. **Initiated** - Customer submits request from portal
2. **Validated** - Middleware validates request
3. **Pricing Evaluated** - Rate card comparison executed
4. **Submitted** - Change order submitted to Dynamics
5. **Processing** - Dynamics executing orchestration
6. **Completed** - Change successfully applied
7. **Rejected** - Request rejected due to validation or business rule


## Relationships
- **implements**: [GCO Lifecycle](wiki/concepts/gco-lifecycle.md)
- **related-to**: [Change Order Categories](wiki/concepts/change-order-categories.md)
- **depends-on**: [Dynamics](wiki/entities/dynamics.md)

## See Also
- [GCO Lifecycle](wiki/concepts/gco-lifecycle.md)
- [Change Order Categories](wiki/concepts/change-order-categories.md)
- [Pricing Logic & Rate Card Comparison](wiki/concepts/pricing-logic.md)
- [Participating Systems](wiki/comparisons/participating-systems.md)