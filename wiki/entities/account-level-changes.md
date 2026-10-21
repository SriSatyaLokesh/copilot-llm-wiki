# Account Level Changes

## Overview

Account Level Changes are Global Change Orders that update customer account metadata without affecting services or provisioning. These changes do not trigger service disruptions or pricing modifications.

## Key Facts

- **Scope**: Updates customer account metadata, not services (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **No Service Impact**: No effect on provisioning or service delivery (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Source of Truth**: Dynamics maintains authoritative account, contact, and billing address data (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)

## Supported Operations

- Change contact phone number
- Update billing address (domestic and foreign supported)
- Add / Remove billing contact
- Add / Remove technical contact
- Add / Remove local / IT contacts

## API Endpoints

### Update Contact Phone Number
```
PUT /customer/accounts/{accountId}/contacts/{contactId}/phone
Payload: { "phoneNumber": "+1-425-555-9023" }
```

### Update Billing Address
```
PUT /customer/accounts/{accountId}/billing-address
Payload: { "addressLine1": "...", "city": "...", "state": "...", "postalCode": "...", "country": "US" }
```

### Add Billing Contact
```
POST /customer/accounts/{accountId}/contacts/billing
```

### Add Technical Contact
```
POST /customer/accounts/{accountId}/contacts/technical
```

## Processing Flow
Portal UI → Portal Backend → CustomerMS/CADMS → Dynamics Account Update → Response returned to Portal


## Relationships
- **part-of**: [Global Change Order](wiki/entities/global-change-order.md)
- **depends-on**: [CXPBU CustomerMS](wiki/entities/cxpbu-customerms.md)
- **depends-on**: [CXPBU CADMS](wiki/entities/cxpbu-cadms.md)

## See Also
- [Global Change Order](wiki/entities/global-change-order.md)
- [Change Order Categories](wiki/concepts/change-order-categories.md)