# Participating Systems

## Summary Table

The Business Portal Global Change Order system integrates with multiple backend systems and microservices to provide a cohesive customer experience. Each system plays a distinct role in the order processing pipeline.

| System | Type | Responsibility | Integration |
|--------|------|-----------------|-------------|
| **Portal UI** | Frontend | Customer interface for submitting change requests | Primary entry point |
| **Portal Backend** | API Gateway | API gateway and request routing for portal requests | Request aggregation |
| **CXPBU CustomerMS** | Microservice | Customer account APIs and account data management | Account access |
| **CXPBU CADMS** | Microservice | Customer account data persistence and coordination | Data storage |
| **CXPBU OrderMS** | Microservice | Order orchestration, rate card pricing, ETF calculation | Order processing |
| **Dynamics** | ERP System | Order orchestration system of record; source of truth for accounts, contracts, contacts | Central hub |
| **Salesforce** | CRM | Quotation integration for sales-reviewed price decreases | Sales coordination |
| **Shazam** | Network System | Network provisioning system for IP address assignment | IP provisioning |
| **NetBox** | IPAM | Network IP address management and inventory tracking | Network inventory |
| **CXPBU Catalog DB** | Database | Product catalog and rate card pricing data | Pricing source |
| **Billing Microservice (MyAccount)** | Microservice | Billing data APIs and account balance information | Billing info |
| **Ziply Notification Platform** | Notification Service | Email notifications for account and service changes | Customer notifications |

## Integration Flows

### Account Level Change Flow
```
Portal → Portal Backend → CustomerMS/CADMS → Dynamics → Response to Portal
```

### Static IP Change Flow
```
Portal → Portal Backend → OrderMS → Dynamics → Shazam → NetBox → Dynamics → Portal
```

### Service Level Change Flow
```
Portal → Portal Backend → OrderMS → Dynamics
  ├── (Price Increase) → Automatic Execution → Provisioning
  └── (Price Decrease) → Salesforce/Work Order → Sales Review → Execution
```

## System Categories

### Portal Layer
- Portal UI
- Portal Backend

### Middleware Layer (CXPBU)
- CustomerMS
- CADMS
- OrderMS
- Catalog DB
- Billing Microservice

### Backend Systems
- Dynamics (ERP)
- Salesforce (CRM)
- Shazam (Network Provisioning)
- NetBox (IPAM)
- Ziply Notification Platform

## Data Flow Responsibility

| Data | Producer | Consumer | Authority |
|------|----------|----------|-----------|
| Account Information | Dynamics | All systems | Dynamics |
| Contact Data | Dynamics | All systems | Dynamics |
| IP Assignments | Shazam | Portal, NetBox | Shazam |
| Network Inventory | NetBox | Portal, Shazam | NetBox |
| Rate Cards | Catalog DB | OrderMS, Portal | Catalog DB |
| Contract Terms | Dynamics | OrderMS, Portal | Dynamics |
| Order Status | Dynamics | Portal, all systems | Dynamics |

## See Also
- [Global Change Order](wiki/entities/global-change-order.md)
- [GCO Lifecycle](wiki/concepts/gco-lifecycle.md)
- [CXPBU OrderMS](wiki/entities/cxpbu-orderms.md)
- [CXPBU CustomerMS](wiki/entities/cxpbu-customerms.md)
- [CXPBU CADMS](wiki/entities/cxpbu-cadms.md)
- [Dynamics](wiki/entities/dynamics.md)
