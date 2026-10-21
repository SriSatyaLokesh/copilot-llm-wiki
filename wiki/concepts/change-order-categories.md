# Change Order Categories

## Definition

Global Change Orders are categorized into three distinct types based on scope and impact: Account Level Changes, Static IP Changes, and Service Level Changes. This categorization determines validation rules, pricing impact, and required approvals.

## How It Works

### Account Level Changes
- **Scope**: Customer account metadata updates
- **Impact**: No service or pricing impact
- **Pricing**: No pricing changes
- **Approval**: Standard validation only
- **Examples**: Contact phone update, billing address change, add/remove contacts
- **See**: [Account Level Changes](wiki/entities/account-level-changes.md)

### Static IP Changes
- **Scope**: IP address visibility and modification requests
- **Impact**: May affect network configuration and service
- **Pricing**: Variable (depends on IP block changes)
- **Approval**: Standard validation + IP eligibility check
- **Examples**: View assigned IPs, request IP block change
- **Data Sources**: Shazam (assignments), NetBox (inventory)
- **See**: [Static IP Changes](wiki/entities/static-ip-changes.md)

### Service Level Changes
- **Scope**: Service configuration, tiers, add-ons, and disconnections
- **Impact**: Direct pricing and contract impact
- **Pricing**: Complex evaluation (may require sales review)
- **Approval**: Validation + pricing evaluation + potential sales review
- **Examples**: Add-on modifications, service upgrades/downgrades, service disconnection, ETF calculation
- **See**: [Service Level Changes](wiki/entities/service-level-changes.md)

## Category Comparison Table

| Aspect | Account Level | Static IP | Service Level |
|--------|---------------|-----------|---------------|
| **Service Impact** | None | Possible | Direct |
| **Pricing Impact** | None | Variable | Direct |
| **Data Systems** | CADMS, Dynamics | Shazam, NetBox | OrderMS, Catalog DB |
| **Approval Level** | Standard | IP validation | Sales review (price decrease) |
| **Typical Duration** | Immediate | Short | Variable |


## Relationships
- **related-to**: [Global Change Order](wiki/entities/global-change-order.md)

## See Also
- [Global Change Order](wiki/entities/global-change-order.md)
- [GCO Lifecycle](wiki/concepts/gco-lifecycle.md)
- [Account Level Changes](wiki/entities/account-level-changes.md)
- [Static IP Changes](wiki/entities/static-ip-changes.md)
- [Service Level Changes](wiki/entities/service-level-changes.md)