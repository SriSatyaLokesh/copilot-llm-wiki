# GCO Lifecycle

## Definition

The Global Change Order (GCO) Lifecycle is a 7-state workflow that governs the processing of all customer-initiated account and service modifications through the Business Portal. Each state represents a distinct phase of validation, evaluation, and execution.

## How It Works

The lifecycle flows sequentially through the following states:

### 1. Initiated
- **Trigger**: Customer submits a change request from the portal
- **System**: Portal UI captures request
- **Action**: Request created and logged

### 2. Validated
- **Trigger**: Middleware processes the request
- **System**: CXPBU middleware services (CustomerMS, OrderMS)
- **Action**: Request validated against business rules, data validation, service eligibility
- **Outcome**: Pass/Fail validation

### 3. Pricing Evaluated
- **Trigger**: For service-related changes, pricing comparison executes
- **System**: CXPBU OrderMS
- **Action**: Current rate card fetched from Catalog DB, pricing impact calculated
- **Outcome**: Pricing impact determined (increase, decrease, no change)

### 4. Submitted
- **Trigger**: Validated and priced request is ready for execution
- **System**: CXPBU OrderMS → Dynamics
- **Action**: Global Change Order submitted to Dynamics for orchestration
- **Outcome**: GCO recorded in Dynamics with status and details

### 5. Processing
- **Trigger**: Dynamics begins orchestration
- **System**: Dynamics orchestration engine, provisioning systems (Shazam, NetBox)
- **Action**: Order execution, service provisioning, network configuration
- **Outcome**: Changes applied to backend systems

### 6. Completed
- **Trigger**: All orchestration and provisioning complete
- **System**: Portal, Dynamics, backend systems
- **Action**: Change successfully applied; customer notification sent (when Ziply integration enabled)
- **Outcome**: Change visible in customer portal

### 7. Rejected
- **Trigger**: Validation or business rule failure at any stage
- **System**: CXPBU middleware or Dynamics
- **Action**: Request rejected with error details; customer notified
- **Outcome**: Change not applied; customer can retry with corrections

## GCO Object Structure

```json
{
  "changeOrderId": "GCO-902341",
  "accountId": "ACC-10091",
  "serviceId": "BFI-12345",
  "changeType": "SERVICE_CHANGE",
  "requestedBy": "portal-user",
  "requestTimestamp": "2026-03-16T11:20:00Z",
  "pricingImpact": "INCREASE",
  "requiresSalesReview": false,
  "status": "SUBMITTED"
}
```


## Relationships
- **implements**: [Global Change Order](wiki/entities/global-change-order.md)
- **depends-on**: [Dynamics](wiki/entities/dynamics.md)

## See Also
- [Global Change Order](wiki/entities/global-change-order.md)
- [Change Order Categories](wiki/concepts/change-order-categories.md)
- [Pricing Logic & Rate Card Comparison](wiki/concepts/pricing-logic.md)