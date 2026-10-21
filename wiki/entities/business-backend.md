# Business Backend

## Overview

Business Backend is the API layer that receives requests from the Commercial Portal and routes them to Order MS for processing. It acts as the intermediary between the customer-facing portal and the order orchestration microservices.

## Key Facts

- **Role**: Request aggregation and routing layer (Source: [submitorder-api](wiki/sources/submitorder-api.md), 2026-10-21)
- **Responsibilities**: Authentication, request validation, order routing (Source: [submitorder-api](wiki/sources/submitorder-api.md), 2026-10-21)
- **Called By**: Commercial Portal (Source: [submitorder-api](wiki/sources/submitorder-api.md), 2026-10-21)
- **Calls**: Order MS (SubmitOrder API) (Source: [submitorder-api](wiki/sources/submitorder-api.md), 2026-10-21)
- **Functions**: Extract Quote ID, Primary Account Number, Order Type from portal requests (Source: [submitorder-api](wiki/sources/submitorder-api.md), 2026-10-21)

## Request Processing

1. Receives Place Order request from Commercial Portal
2. Extracts quote and account information
3. Calls Order MS with SubmitOrder API
4. Receives order creation response
5. Returns status to Commercial Portal

## Integration Points

- **Input**: Commercial Portal requests
- **Output**: SubmitOrder API calls
- **Response Handling**: Receives order success/failure status, relays to portal


## Relationships
- **part-of**: [Commercial Portal](wiki/entities/commercial-portal.md)
- **depends-on**: [Commercial Portal](wiki/entities/commercial-portal.md)
- **depends-on**: [CXPBU OrderMS](wiki/entities/cxpbu-orderms.md)

## See Also
- [Commercial Portal](wiki/entities/commercial-portal.md)
- [SubmitOrder API](wiki/entities/submitorder-api.md)
- [Order Creation Flow](wiki/concepts/order-creation-flow.md)