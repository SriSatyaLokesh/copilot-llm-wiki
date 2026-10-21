# Static IP Change Scenarios

## Summary Table

The Business Portal supports 8 distinct static IP change scenarios, each with specific system behavior, automation level, and downtime risk. These scenarios address the major customer needs for IP configuration changes while acknowledging CIDR block technical constraints.

| Scenario | Current State | Target State | System Behavior | Automation | Downtime Risk |
|----------|---------------|--------------|-----------------|-----------|---------------|
| **1** | Dynamic IP | Static IP 1 | Allocate new /30 block | Automated | None |
| **2** | Dynamic IP | Static IP 5 | Allocate new /29 block | Automated | None |
| **3** | Static IP 1 | Static IP 5 (Immediate) | Release /30, allocate /29 | Automated | Possible |
| **4** | Static IP 1 | Static IP 5 (Zero Downtime) | Allocate /29, keep /30 temporarily | Partial | None |
| **5** | Static IP 5 | Static IP 1 (Immediate) | Release /29, allocate /30 | Automated | Possible |
| **6** | Static IP 5 | Static IP 1 (Zero Downtime) | Allocate /30, keep /29 temporarily | Partial | None |
| **7** | Static IP 1 | Dynamic IP | Release /30 block | Automated | Possible |
| **8** | Static IP 5 | Dynamic IP | Release /29 block | Automated | Possible |

## Scenario Details

### Scenarios 1-2: Dynamic IP → Static IP (New Allocation)
- **Behavior**: Allocate new static IP block
- **Automation**: Fully automated
- **Downtime Risk**: None (new allocation, no existing IPs to migrate)
- **Timeline**: Quick
- **Complexity**: Simple

### Scenarios 3 & 5: Static IP Block Upgrade/Downgrade (Immediate)
- **Behavior**: Release old block, allocate new block immediately
- **Automation**: Fully automated
- **Downtime Risk**: Possible (customer must quickly update network config)
- **Timeline**: Fast but risky for customer
- **Complexity**: Medium
- **When to Use**: Customer prefers speed over safety; minimal network dependencies

### Scenarios 4 & 6: Static IP Block Upgrade/Downgrade (Zero Downtime)
- **Behavior**: Allocate new block, keep old block temporarily
- **Automation**: Partial (allocation automated, cleanup manual)
- **Downtime Risk**: None (dual-block coexistence)
- **Timeline**: Extended (24-48 hour migration window)
- **Complexity**: Medium-High (customer coordination required)
- **When to Use**: Service continuity critical; customer has dependencies on existing IPs
- **See**: [Zero Downtime Migration](wiki/concepts/zero-downtime-migration.md)

### Scenarios 7-8: Static IP → Dynamic IP (Removal)
- **Behavior**: Release static IP block entirely
- **Automation**: Fully automated
- **Downtime Risk**: Possible (customer must remove static IP dependency)
- **Timeline**: Quick
- **Complexity**: Simple

## Unsupported Scenarios

The following scenarios **cannot be supported** due to CIDR block technical constraints:

| Requested Behavior | Reason Not Supported |
|--------------------|---------------------|
| Keep existing IP when upgrading /30 → /29 | CIDR blocks cannot be resized; must release and reallocate |
| Keep 1 IP when downgrading /29 → /30 | Individual IPs cannot be extracted from CIDR blocks |
| Add IPs to existing block | Requires block replacement; IPs cannot be added incrementally |

## Decision Matrix: Which Scenario?

**Question 1**: Is customer changing from Dynamic to Static?
- **Yes** → Use Scenario 1 or 2 (depends on desired IP count)
- **No** → Continue to Question 2

**Question 2**: Is customer removing Static IP entirely?
- **Yes** → Use Scenario 7 or 8 (depends on current block size)
- **No** → Continue to Question 3

**Question 3**: Does customer prioritize speed or service continuity?
- **Speed** → Use Scenario 3 or 5 (Immediate)
- **Continuity** → Use Scenario 4 or 6 (Zero Downtime)

**Question 4**: Is customer upgrading or downgrading block size?
- **Upgrading (/30 → /29)** → Scenario 3 (immediate) or 4 (zero downtime)
- **Downgrading (/29 → /30)** → Scenario 5 (immediate) or 6 (zero downtime)

## Portal Experience

Portal will likely:
- Detect current state
- Present available scenarios
- Allow customer to choose immediate vs. zero downtime (if applicable)
- Display both blocks during zero downtime migration
- Show countdown timer for migration window

## See Also
- [Static IP Global Change Orders](wiki/entities/static-ip-global-change-orders.md)
- [Zero Downtime Migration](wiki/concepts/zero-downtime-migration.md)
- [CIDR Block Allocation](wiki/concepts/cidr-block-allocation.md)
- [Static IP Products](wiki/entities/static-ip-products.md)
