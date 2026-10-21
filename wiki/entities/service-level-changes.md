# Service Level Changes

## Overview

Service Level Changes are Global Change Orders that affect existing service configurations and pricing. These changes may require sales review depending on pricing impact and contract status.

## Key Facts

- **Scope**: Modify service configurations, pricing, and contract terms (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Pricing Impact**: Automatic for price increases; sales review required for price decreases (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Contract Handling**: Changes to contracted services trigger pricing comparison and potential ETF calculation (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Pricing Source**: CXPBU Catalog DB maintains rate cards; OrderMS executes pricing calculations (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)

## Supported Operations

| Operation | Description |
|-----------|-------------|
| Modify month-to-month add-ons | Change add-on products without affecting primary service |
| Upgrade service | Increase service tier |
| Downgrade service | Decrease service tier |
| Disconnect service | Service termination (may trigger ETF) |

## Month-to-Month Add-On Changes

Example workflow:
- Primary Service: BFI (60-month term, 30 months remaining)
- Customer changes: Dynamic IP → Static IP
- Behavior: Add-on modified, primary service contract unchanged

Flow: Portal → Portal Backend → OrderMS → Validate add-on eligibility → Create Global Change Order → Submit to Dynamics

## Service Changes Under Contract

When modifying contracted services, pricing must be compared against the current rate card.

### Case 1 — Price Increase
- **Processing**: Fully automated
- **Flow**: Portal → OrderMS → Dynamics → Order Execution

### Case 2 — Price Decrease
- **Processing**: Requires sales intervention
- **Flow**: Portal → OrderMS → Submit to Dynamics → Create Work Order → Sales team engagement
- **Sales Participants**: Account Manager, Account Executive, Retention team


## Relationships
- **part-of**: [Global Change Order](wiki/entities/global-change-order.md)
- **implements**: [Pricing Logic & Rate Card Comparison](wiki/concepts/pricing-logic.md)
- **implements**: [ETF Calculation](wiki/concepts/etf-calculation.md)

## See Also
- [Global Change Order](wiki/entities/global-change-order.md)
- [Pricing Logic & Rate Card Comparison](wiki/concepts/pricing-logic.md)
- [ETF Calculation](wiki/concepts/etf-calculation.md)
- [Change Order Categories](wiki/concepts/change-order-categories.md)