# SubmitOrder API - Technical Documentation

## Source Metadata
- **Ingested**: 2026-04-17
- **Source URL**: https://docs.internal.net
- **Last Verified**: 2026-10-21
- **Volatility**: medium

## Key Takeaways

- **SubmitOrder API** converts commercial quotes into one or more Dynamics Sales Orders using a single-location-per-order model
- **Owned by Order MS**, called by Business Backend when user clicks "Place Order" in Commercial Portal
- **Multi-location quotes** create one order per Address ID, grouped logically by Quote ID
- **Creates service-level accounts** per Address ID (location) with account-contact mapping
- **Transforms quote line items** to order line items with product mapping, quantity, and pricing
- **Orders created in Pending status** with MRC/NRC financials (final calculated prices, no discount codes)
- **Atomic per location** - failures handled independently; partial success supported
- **Future enhancement**: Transition to background job execution for asynchronous processing
- **No rollback automation** across Salesforce and Dynamics; failures are logged and retriable
- Out of scope: Commit Order, Pre-field scheduling, Technician scheduling, Order view APIs

## Pages Created/Updated

- [SubmitOrder API](wiki/entities/submitorder-api.md) — Core API specification
- [Order Creation Flow](wiki/concepts/order-creation-flow.md) — Step-by-step processing
- [Quote to Order Transformation](wiki/concepts/quote-to-order-transformation.md) — Line item mapping
- [Commercial Portal](wiki/entities/commercial-portal.md) — Portal interface
- [Service-Level Account Creation](wiki/concepts/service-level-account-creation.md) — Account model

## See Also
- [CXPBU OrderMS](wiki/entities/cxpbu-orderms.md)
- [Business Backend](wiki/entities/business-backend.md)
- [Dynamics](wiki/entities/dynamics.md)
