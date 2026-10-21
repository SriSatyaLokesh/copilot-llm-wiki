# Pricing Logic & Rate Card Comparison

## Definition

Pricing Logic & Rate Card Comparison is the process by which the Business Portal evaluates the financial impact of customer-initiated service changes. CXPBU OrderMS compares current pricing with the authoritative rate card to determine whether changes are automatically approved or require sales intervention.

## How It Works

### Pricing Data Sources

| Source | Data |
|--------|------|
| CXPBU Catalog DB | Current rate cards, product catalog, pricing rules |
| Dynamics | Contract terms, service history, customer account data |
| OrderMS | Pricing calculation logic, comparison algorithms |

### Price Increase (Automated)
- **Trigger**: Customer requests a service change that increases monthly or one-time costs
- **Processing**: Fully automated
- **Approval**: Standard validation only
- **Flow**: Portal → OrderMS → Dynamics → Order Execution
- **Action**: Change immediately submitted for provisioning
- **Customer Impact**: Higher pricing displayed in portal, accepted by customer

### Price Decrease (Sales Review Required)
- **Trigger**: Customer requests a service change that decreases costs
- **Processing**: Requires human sales review
- **Approval**: Sales team intervention mandatory
- **Flow**: Portal → OrderMS → Dynamics → Create Work Order → Sales Team Engagement
- **Sales Participants**: 
  - Account Manager
  - Account Executive
  - Retention team
- **Outcome**: Sales team reviews and approves/denies price reduction

### No Price Impact
- **Trigger**: Account metadata or non-billable service changes
- **Processing**: Automatic validation
- **Approval**: Standard validation only
- **Examples**: Contact updates, add-on modifications with no price change

## Rate Card Evaluation

The rate card is maintained in CXPBU Catalog DB and consulted for every service-related change:

1. Customer requests service modification
2. OrderMS fetches current rate card from Catalog DB
3. New pricing calculated based on change request
4. Pricing compared with current billing
5. Decision logic applied (increase = auto, decrease = sales review, same = auto)
6. Result passed to Dynamics for processing

## Service Upgrade vs. Downgrade

### Upgrade (Typically Price Increase)
- Service tier increased
- Feature additions
- Usually automated approval

### Downgrade (Typically Price Decrease)
- Service tier decreased
- Feature removals
- Requires sales review to prevent revenue loss

## Contract Term Considerations

When modifying services under contract:
- **Primary Service Contract**: Unchanged by month-to-month add-on modifications
- **Contracted Service Changes**: Subject to rate card comparison and potential ETF calculation
- **Remaining Term**: Affects pricing calculations and ETF amounts


## Relationships
- **implements**: [CXPBU OrderMS](wiki/entities/cxpbu-orderms.md)
- **depends-on**: [CXPBU Catalog DB](wiki/entities/cxpbu-catalog-db.md)

## See Also
- [Service Level Changes](wiki/entities/service-level-changes.md)
- [ETF Calculation](wiki/concepts/etf-calculation.md)
- [CXPBU OrderMS](wiki/entities/cxpbu-orderms.md)
- [Global Change Order](wiki/entities/global-change-order.md)