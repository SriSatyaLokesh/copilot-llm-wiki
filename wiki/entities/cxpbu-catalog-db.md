# CXPBU Catalog DB

## Overview

CXPBU Catalog DB is the centralized product catalog and rate card pricing database for the Business Portal. It maintains the authoritative source of truth for all service offerings, product configurations, and pricing information used throughout the order orchestration and Global Change Order processing systems.

## Key Facts

- **Role**: Product catalog and pricing authority (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Scope**: Product definitions, SKU mappings, rate cards, pricing rules, promotional codes (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Owned By**: CXPBU platform (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Accessed By**: OrderMS (pricing calculations), Portal (product display), Service Level Changes (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Data Authority**: Source of truth for all pricing evaluations (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Rate Card Usage**: Consulted for every service change request to determine pricing impact (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Update Mechanism**: TBD (likely batch updates from business systems) (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)

## Integration Points

- **Input**: Business pricing updates, product configuration changes
- **Consumed By**:
  - CXPBU OrderMS (rate card comparison, pricing calculations)
  - Portal (product display, pricing presentation)
  - Change Order Processing (pricing impact determination)
- **Output**: Rate cards, product definitions, pricing rules

## Pricing Evaluation Process

When a customer initiates a service change, OrderMS follows this flow:

1. **Fetch current rate card** from Catalog DB for requested service
2. **Compare pricing** between current and requested configuration
3. **Determine pricing impact**:
   - Price increase → Automated approval
   - Price decrease → Sales review required
   - No change → Standard approval
4. **Pass result** to Dynamics for order orchestration


## Relationships
- **part-of**: [Participating Systems](wiki/comparisons/participating-systems.md)
- **related-to**: [CXPBU OrderMS](wiki/entities/cxpbu-orderms.md)

## See Also
- [CXPBU OrderMS](wiki/entities/cxpbu-orderms.md)
- [Pricing Logic & Rate Card Comparison](wiki/concepts/pricing-logic.md)
- [Service Level Changes](wiki/entities/service-level-changes.md)
- [Participating Systems](wiki/comparisons/participating-systems.md)