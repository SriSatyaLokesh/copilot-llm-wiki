# Quote to Order Transformation

## Definition

Quote to Order Transformation is the process by which SubmitOrder API converts quote line items (commercial offerings with pricing) into order line items (billable service items) compatible with Dynamics Sales Orders.

## How It Works

### Source: Quote Line Items (from Salesforce)

Quote line items contain:
- **Address ID** — Service location identifier
- **Product Code** — Service/product identifier
- **Quantity** — Number of units
- **Unit Price** — Price per unit
- **Discount Code** (if applicable)

### Transformation Rules

1. **Product Code Mapping**
   - Quote product code → Order product code
   - Validation ensures product exists in catalog
   
2. **Quantity Preservation**
   - Quote quantity → Order quantity (unchanged)
   
3. **Pricing Calculation**
   - Unit price × Quantity = Line item total
   - Final calculated price used (discount codes NOT sent to Dynamics)
   - Monthly Recurring Charges (MRC) and Non-Recurring Charges (NRC) calculated separately

4. **Address ID Grouping**
   - Group all line items by Address ID
   - Each Address ID creates one independent order

5. **Order Line Item Payload Construction**
   - Create API-compatible payload for Dynamics
   - Format: Product code, quantity, unit price, total

### Example Transformation

**Quote (Salesforce):**
```
Quote ID: Q-123
Address ID: ADDR-456
Line 1: Product=BFI-10M, Qty=1, Price=$100/mo
Line 2: Product=STATIC-IP-5, Qty=1, Price=$20/mo
Line 3: Product=INSTALL-FEE, Qty=1, Price=$500
```

**Transformed Order (for Dynamics):**
```
Order ID: (Generated)
Account ID: ACC-789 (created per Address)
Quote ID: Q-123
Address ID: ADDR-456
Order Line Items:
  - BFI-10M: Qty=1, Price=$100/mo (MRC)
  - STATIC-IP-5: Qty=1, Price=$20/mo (MRC)
  - INSTALL-FEE: Qty=1, Price=$500 (NRC)
Total MRC: $120/mo
Total NRC: $500
Order Status: Pending
```

### Discount Handling

- **Quote Level**: May contain discount codes
- **Order Level**: Final calculated prices ONLY
- **Discount Codes**: NOT transmitted to Dynamics
- **Pricing**: Already applied; order reflects net price

### Multi-Location Quote Example

**Quote:**
```
Quote ID: Q-999
Address 1 (Seattle): 2 line items
Address 2 (Portland): 3 line items
```

**Results in Two Orders:**
```
Order 1: Address 1 with 2 line items
Order 2: Address 2 with 3 line items
(Both grouped under Quote ID Q-999)
```

## Responsibilities

- **SubmitOrder API**: Executes transformation
- **Order MS**: Provides transformation logic
- **Validation**: Ensures all products exist and are valid

## Output

- **Order Line Items**: Payload-ready format
- **Order Grouping**: By Address ID
- **Status**: Ready for Dynamics submission


## Relationships
- **implements**: [SubmitOrder API](wiki/entities/submitorder-api.md)
- **depends-on**: [CXPBU OrderMS](wiki/entities/cxpbu-orderms.md)

## See Also
- [Order Creation Flow](wiki/concepts/order-creation-flow.md)
- [SubmitOrder API](wiki/entities/submitorder-api.md)
- [Service-Level Account Creation](wiki/concepts/service-level-account-creation.md)