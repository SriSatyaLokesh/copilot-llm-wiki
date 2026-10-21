# ETF Calculation

## Definition

Early Termination Fee (ETF) Calculation is the process of computing the financial penalty when a customer requests to disconnect a service while still under contract. CXPBU OrderMS calculates the ETF based on contract dates, service pricing, and remaining term.

## How It Works

### Trigger
- Customer requests service disconnection while under contract
- Service contract has not yet expired
- ETF eligibility verified

### Calculation Inputs

| Input | Source |
|-------|--------|
| Contract start date | Dynamics |
| Contract end date | Dynamics |
| Service price | CXPBU Catalog DB |
| Current date | System |

### Calculation Process

1. **OrderMS receives disconnection request** from Portal
2. **Contract data fetched** from Dynamics (start/end dates, terms)
3. **Service pricing retrieved** from Catalog DB
4. **ETF computed** based on:
   - Remaining contract period
   - Service monthly/annual price
   - Contract terms and conditions
5. **ETF displayed** to customer in Portal
6. **Customer decision**: Accept ETF or cancel request

### Calculation Formula (Typical)

```
Remaining Months = (Contract End Date - Current Date) / 30 days
ETF = Service Monthly Price × Remaining Months × (ETF Percentage Factor)
```

*Note: Exact formula may vary based on service type and contract terms.*

### Processing Flow

```
Portal
  ↓
Portal Backend
  ↓
OrderMS
  ↓
Fetch contract data from Dynamics
  ↓
Calculate ETF
  ↓
Display ETF to customer
```

### Post-ETF Acceptance

After customer accepts ETF:

1. Global Change Order created with disconnection request
2. Work Order created in Dynamics
3. Sales/Customer Care review required
4. Service provisioning initiated
5. Account marked for disconnection

**Workflow Status**: Still under definition

### Example Scenario

```
Service: BFI-12345
Contract Period: 60 months
Contract End Date: 2027-12-31
Current Date: 2026-04-17
Remaining Months: ~20 months
Monthly Price: $500
Estimated ETF: ~$5,000 (rough estimate, based on contract terms)
```

## Error Handling

| Error | Description |
|-------|-------------|
| Contract already expired | Cannot calculate ETF, service can be disconnected at any time |
| Service not found in Dynamics | Contract data retrieval failure |
| Pricing retrieval failure | Catalog DB unavailable |


## Relationships
- **implements**: [CXPBU OrderMS](wiki/entities/cxpbu-orderms.md)
- **part-of**: [Service Level Changes](wiki/entities/service-level-changes.md)

## See Also
- [Service Level Changes](wiki/entities/service-level-changes.md)
- [Pricing Logic & Rate Card Comparison](wiki/concepts/pricing-logic.md)
- [Global Change Order](wiki/entities/global-change-order.md)
- [CXPBU OrderMS](wiki/entities/cxpbu-orderms.md)