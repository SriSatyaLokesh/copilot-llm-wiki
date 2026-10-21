# SubmitOrder API

## Overview

SubmitOrder API is a microservice API owned by Order MS that converts commercial quotes into Dynamics Sales Orders. The API implements a single-location-per-order model where each unique Address ID in a multi-location quote generates one independent sales order, grouped logically by Quote ID.

## Key Facts

- **Owned By**: Order MS (Source: [submitorder-api](wiki/sources/submitorder-api.md), 2026-10-21)
- **Called By**: Business Backend (Source: [submitorder-api](wiki/sources/submitorder-api.md), 2026-10-21)
- **Trigger**: User clicks "Place Order" in Commercial Portal (Source: [submitorder-api](wiki/sources/submitorder-api.md), 2026-10-21)
- **Model**: Single-location per order (one order per Address ID) (Source: [submitorder-api](wiki/sources/submitorder-api.md), 2026-10-21)
- **Multi-Location Handling**: Creates multiple orders, groups by Quote ID (Source: [submitorder-api](wiki/sources/submitorder-api.md), 2026-10-21)
- **Downstream Systems**: Salesforce (Quote, Opportunity), Dynamics (Account, Contact, Sales Order) (Source: [submitorder-api](wiki/sources/submitorder-api.md), 2026-10-21)
- **Processing**: Currently synchronous; future enhancement to async background job (Source: [submitorder-api](wiki/sources/submitorder-api.md), 2026-10-21)
- **Order Status**: Created in Pending status with complete MRC/NRC financials (Source: [submitorder-api](wiki/sources/submitorder-api.md), 2026-10-21)
- **Atomicity**: Per-location atomic; failures in one location don't block others (Source: [submitorder-api](wiki/sources/submitorder-api.md), 2026-10-21)
- **Response**: SUCCESS / PARTIAL_SUCCESS / FAILURE (Source: [submitorder-api](wiki/sources/submitorder-api.md), 2026-10-21)

## Processing Flow

1. **Fetch Quote Line Items** from Salesforce using Quote ID
2. **Validate Contract** exists and is signed
3. **Close Sales Artifacts** in Salesforce and Dynamics (mark Opportunity Won, Quote Closed)
4. **Create Service-Level Accounts** per Address ID in Dynamics
5. **Link Primary Contact** to each service account with role-based mapping
6. **Transform Quote Line Items** to Order Line Items (map product codes, quantities, pricing)
7. **Construct Order Payload** with headers, line items, MRC/NRC financials
8. **Submit to Dynamics** using Create Sales Order API
9. **Return Response** with Order IDs, Order Numbers, Account IDs, and status

## Input Contract

| Field | Description |
|-------|-------------|
| quoteId | Quote ID for grouping orders |
| primaryAccountNumber | Parent/primary account number |
| orderType | Commercial order type |
| initiatedBy | User placing the order |
| source | Commercial Portal |

## Output Contract

| Field | Description |
|-------|-------------|
| quoteId | Quote ID used for grouping |
| orders[] | List of created orders |
| orders[].orderId | Dynamics Order ID |
| orders[].orderNumber | Dynamics Order Number |
| orders[].accountId | Service account ID |
| status | SUCCESS / PARTIAL_SUCCESS / FAILURE |

## Limitations

- No automatic rollback across Salesforce and Dynamics
- Failures logged and retriable
- Out of scope: Commit Order, Pre-field, Technician Scheduling, Order view APIs

## Future Enhancement

Transition to **background job execution** for asynchronous processing with job status tracking.


## Relationships
- **part-of**: [CXPBU OrderMS](wiki/entities/cxpbu-orderms.md)
- **depends-on**: [Business Backend](wiki/entities/business-backend.md)
- **depends-on**: [Dynamics](wiki/entities/dynamics.md)
- **implements**: [Order Creation Flow](wiki/concepts/order-creation-flow.md)
- **implements**: [Quote to Order Transformation](wiki/concepts/quote-to-order-transformation.md)

## See Also
- [CXPBU OrderMS](wiki/entities/cxpbu-orderms.md)
- [Order Creation Flow](wiki/concepts/order-creation-flow.md)
- [Quote to Order Transformation](wiki/concepts/quote-to-order-transformation.md)
- [Commercial Portal](wiki/entities/commercial-portal.md)
- [Dynamics](wiki/entities/dynamics.md)