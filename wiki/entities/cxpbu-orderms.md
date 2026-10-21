# CXPBU OrderMS

## Overview

CXPBU OrderMS is a critical microservice within the CXPBU platform responsible for order orchestration, pricing evaluation, and financial calculations. It serves as the middleware between the Portal and Dynamics, handling validation, rate card comparison, and Early Termination Fee (ETF) calculations.

## Key Facts

- **Responsibility**: Order orchestration, rate card pricing comparison, ETF calculation (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Pricing Source**: Integrates with CXPBU Catalog DB for current rate cards (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Change Order Creation**: Creates Global Change Orders based on customer requests (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **ETF Calculation**: Computes Early Termination Fees for service disconnections under contract (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Dynamics Integration**: Submits validated and priced orders to Dynamics for final orchestration (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)

## Core Functions

1. **Rate Card Comparison** - Evaluates pricing impact of service changes
2. **ETF Calculation** - Computes fees for early service termination
3. **Add-On Validation** - Validates eligibility of add-on changes
4. **Order Submission** - Submits Global Change Orders to Dynamics

## Integration Points

- **Input**: Portal Backend, customer service requests
- **Catalog Source**: CXPBU Catalog DB (rate cards, product catalog)
- **Contract Data**: Dynamics (contract terms, dates)
- **Output**: Dynamics (Global Change Orders)


## Relationships
- **part-of**: [Participating Systems](wiki/comparisons/participating-systems.md)
- **depends-on**: [CXPBU Catalog DB](wiki/entities/cxpbu-catalog-db.md)
- **implements**: [Pricing Logic & Rate Card Comparison](wiki/concepts/pricing-logic.md)
- **implements**: [ETF Calculation](wiki/concepts/etf-calculation.md)

## See Also
- [CXPBU CustomerMS](wiki/entities/cxpbu-customerms.md)
- [CXPBU CADMS](wiki/entities/cxpbu-cadms.md)
- [Global Change Order](wiki/entities/global-change-order.md)
- [Pricing Logic & Rate Card Comparison](wiki/concepts/pricing-logic.md)