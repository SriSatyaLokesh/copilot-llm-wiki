# Order Creation Flow

## Definition

Order Creation Flow is the step-by-step process executed by the SubmitOrder API to convert a commercial quote into one or more Dynamics Sales Orders. The flow validates contracts, closes sales artifacts, creates accounts, and transforms quote line items into orders.

## How It Works

### Step 1: Fetch Quote Line Items
- Order MS retrieves all quote line items from Salesforce using Quote ID
- Line items contain: Address ID, product details, quantity, pricing
- Groups items by Address ID for later order creation

### Step 2: Contract Validation
- Verify contract exists in Salesforce
- Confirm contract is signed
- Block processing if contract is not signed

### Step 3: Close Sales Artifacts
**Salesforce updates:**
- Mark Opportunity = Won
- Mark Quote = Closed

**Dynamics updates:**
- Mark Opportunity = Won
- Mark Quote = Closed

*(Executed BEFORE order creation)*

### Step 4: Account & Contact Creation (Per Address ID)
For each unique Address ID found in quote line items:

**Account Creation in Dynamics:**
- Create new service-level account
- Populate: Account Name, Email, Phone, Billing Address, Service Address
- Receive: Account ID from Dynamics

**Contact Linking:**
- Link primary contact from parent account
- Create role-based account-contact mapping
- Receive: Mapping confirmation

### Step 5: Quote Line Item → Order Line Item Transformation
- Map product codes from quote line items
- Preserve quantities and unit prices
- Group by Address ID
- Build order line item payloads compatible with Dynamics API

### Step 6: Order Payload Construction (Per Address ID)
**Order Header:**
- Quote ID
- Account Number (service account from Step 4)
- Parent Account Number
- Order Type
- Order Channel (Commercial Portal)
- Initial Status: Pending

**Financials:**
- Monthly Recurring Charges (MRC)
- Non-Recurring Charges (NRC)
- Final calculated prices only (no discount codes)

**Line Items:**
- Attach transformed order line items
- Single Address ID per order

### Step 7: Submit to Dynamics
- Call Dynamics Create Sales Order API
- One order per Address ID
- Receive: Order ID, Order Number, Status

### Step 8: Return Response
- Status: SUCCESS / PARTIAL_SUCCESS / FAILURE
- Include: Quote ID, Order IDs, Order Numbers, Account IDs

## Atomicity Model

- **Per-Location Atomic**: Each Address ID order creation is independent
- **Partial Success Supported**: One location failure doesn't block others
- **No Automatic Rollback**: Failures across systems are not rolled back automatically
- **Failures Logged & Retriable**: Failed orders can be retried

## Timeline

```
User Click "Place Order"
  ↓ (seconds)
Fetch Quote Items from Salesforce
  ↓ (seconds)
Validate Contract
  ↓ (seconds)
Close Salesforce & Dynamics Artifacts
  ↓ (seconds)
Create Service Accounts (parallel per Address)
  ↓ (seconds)
Transform Quote → Order Line Items
  ↓ (seconds)
Submit Orders to Dynamics (parallel per Address)
  ↓ (seconds)
Return Response to Business Backend
  ↓ (milliseconds)
Portal displays results
```


## Relationships
- **implements**: [SubmitOrder API](wiki/entities/submitorder-api.md)
- **depends-on**: [Dynamics](wiki/entities/dynamics.md)
- **related-to**: [Service-Level Account Creation](wiki/concepts/service-level-account-creation.md)

## See Also
- [SubmitOrder API](wiki/entities/submitorder-api.md)
- [Quote to Order Transformation](wiki/concepts/quote-to-order-transformation.md)
- [Service-Level Account Creation](wiki/concepts/service-level-account-creation.md)
- [Commercial Portal](wiki/entities/commercial-portal.md)