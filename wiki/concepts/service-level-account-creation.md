# Service-Level Account Creation

## Definition

Service-Level Account Creation is the process by which SubmitOrder API creates individual Dynamics accounts for each unique service location (Address ID) identified in a multi-location quote. These accounts represent the service endpoint at that location and serve as the hub for contact mapping and billing.

## How It Works

### Trigger

For each unique **Address ID** found in quote line items, a new service-level account is created.

### Account Creation Process

**For each Address ID:**

1. **Determine Account Details**
   - Account Name: Generated using defined naming logic (format TBD with business)
   - Email: Inherited from parent/primary account
   - Phone: Inherited from parent/primary account
   - Billing Address: Inherited from primary account
   - **Service Address: Specific to Address ID** (location-specific)

2. **Create in Dynamics**
   - Call Dynamics Account creation API
   - Populate all fields above
   - Receive: Unique Account ID from Dynamics

3. **Link Primary Contact**
   - Identify primary contact from parent account
   - Create role-based account-contact mapping
   - Map to newly created service account
   - Receive: Mapping confirmation from Dynamics

### Data Inheritance Model

| Data | Source | Behavior |
|------|--------|----------|
| Account Name | Generated | Unique name per location |
| Email | Parent Account | Inherited |
| Phone | Parent Account | Inherited |
| Billing Address | Parent Account | Inherited |
| Service Address | Address ID | Location-specific |
| Primary Contact | Parent Account | Linked with role |

### Example: Multi-Location Quote

**Parent Account:**
- Name: Acme Corp
- Email: billing@acme.com
- Phone: (206) 555-0100
- Billing Address: 123 Main St, Seattle, WA
- Primary Contact: John Doe

**Quote with 2 Locations:**

**Location 1 (Seattle):**
```
Address ID: ADDR-SEA-01
Service Address: 500 Pike St, Seattle, WA

Service Account Created:
  Name: Acme Corp - Seattle (generated)
  Email: billing@acme.com (inherited)
  Phone: (206) 555-0100 (inherited)
  Billing Address: 123 Main St, Seattle, WA (inherited)
  Service Address: 500 Pike St, Seattle, WA (location-specific)
  Primary Contact: John Doe (linked with role)
  Account ID: ACC-SEA-001 (Dynamics generated)
```

**Location 2 (Portland):**
```
Address ID: ADDR-PDX-01
Service Address: 1000 SW Alder St, Portland, OR

Service Account Created:
  Name: Acme Corp - Portland (generated)
  Email: billing@acme.com (inherited)
  Phone: (206) 555-0100 (inherited)
  Billing Address: 123 Main St, Seattle, WA (inherited)
  Service Address: 1000 SW Alder St, Portland, OR (location-specific)
  Primary Contact: John Doe (linked with role)
  Account ID: ACC-PDX-001 (Dynamics generated)
```

## Benefits

✅ **Location Separation**: Each service location has independent account
✅ **Billing Hierarchy**: Service accounts linked to parent account
✅ **Contact Consistency**: Primary contact available at all locations
✅ **Address Specificity**: Service address correctly captured per location


## Relationships
- **implements**: [SubmitOrder API](wiki/entities/submitorder-api.md)
- **depends-on**: [Dynamics](wiki/entities/dynamics.md)

## See Also
- [Order Creation Flow](wiki/concepts/order-creation-flow.md)
- [SubmitOrder API](wiki/entities/submitorder-api.md)
- [Quote to Order Transformation](wiki/concepts/quote-to-order-transformation.md)
- [Dynamics](wiki/entities/dynamics.md)