# Commercial Portal

## Overview

Commercial Portal is the web-based user interface where customers initiate order placement and manage their commercial services. It serves as the entry point for the SubmitOrder API workflow.

## Key Facts

- **Role**: Customer-facing commercial ordering interface (Source: [submitorder-api](wiki/sources/submitorder-api.md), 2026-10-21)
- **Trigger Action**: User clicks "Place Order" button (Source: [submitorder-api](wiki/sources/submitorder-api.md), 2026-10-21)
- **Integrations**: Calls Business Backend, displays order status (Source: [submitorder-api](wiki/sources/submitorder-api.md), 2026-10-21)
- **Features**: Quote management, multi-location ordering, order confirmation (Source: [submitorder-api](wiki/sources/submitorder-api.md), 2026-10-21)
- **Status Display**: Shows order IDs, order numbers, creation status per location (Source: [submitorder-api](wiki/sources/submitorder-api.md), 2026-10-21)

## Primary Workflows

### Order Placement
1. Customer reviews multi-location quote
2. Customer clicks "Place Order"
3. Portal sends request to Business Backend
4. Business Backend routes to Order MS (SubmitOrder API)
5. Portal displays success/failure status per location

## Integration Points

- **Input**: Customer actions (Place Order, View Quote)
- **Calls**: Business Backend
- **Receives**: SubmitOrder API response with order details


## Relationships
- **depends-on**: [Business Backend](wiki/entities/business-backend.md)
- **implements**: [Portal Authorization & Roles](wiki/concepts/portal-authorization-roles.md)
- **related-to**: [Global Change Order](wiki/entities/global-change-order.md)

## See Also
- [SubmitOrder API](wiki/entities/submitorder-api.md)
- [Business Backend](wiki/entities/business-backend.md)
- [Order Creation Flow](wiki/concepts/order-creation-flow.md)