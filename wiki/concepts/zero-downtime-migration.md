# Zero Downtime Migration

## Definition

Zero Downtime Migration is an approach to IP block changes that allows customers to maintain service continuity by temporarily hosting both old and new IP blocks during a transition period. Instead of immediately releasing the old block, customers are given time to update their network configuration before the old block is removed.

## How It Works

### Traditional Immediate Replacement (Potential Downtime)
```
Release Old Block → Allocate New Block
(Service may be interrupted if customer hasn't migrated)
```

### Zero Downtime Migration Process

1. **Customer requests IP change** (e.g., /30 → /29 upgrade)
2. **New block allocated** while old block remains active
3. **Customer receives both blocks** during migration window
4. **Migration window**: 24–48 hours provided
5. **Customer updates configuration**:
   - Firewall rules
   - NAT configurations
   - DNS records
   - Application endpoints
6. **Verification**: Account representative confirms migration
7. **Old block released** after verification

### Timeline Example

```
Time 0: Customer requests Static IP 1 → Static IP 5
  - Old Block: 192.168.1.0/30 (active)
  - New Block: Not yet allocated

Time 1 minute: New block allocated
  - Old Block: 192.168.1.0/30 (active)
  - New Block: 192.168.2.0/29 (active - customer now has both)

Time 24-48 hours: Customer updates network config
  - Updates firewall rules to use new block
  - Updates DNS/application endpoints
  - Tests connectivity

Time 48+ hours: Account rep verifies migration
  - Confirms customer using new block
  - Request NetBox to release old block

Time 48+ hours: Old block released
  - Old Block: 192.168.1.0/30 (released back to pool)
  - New Block: 192.168.2.0/29 (permanent assignment)
```

## Migration Window

**Typical Duration**: 24–48 hours

**Purpose**: Provide customers sufficient time to:
- Update firewall configurations
- Reconfigure NAT rules
- Update DNS records
- Migrate application endpoints
- Test connectivity with new block

## Portal Display During Migration

Portal may display both active blocks during migration:

```
Current Static IP Configuration

Temporary Block (Old)
192.168.1.0/30

New Block
192.168.2.0/29
```

UI behavior finalized with business team.

## Post-Migration Cleanup

**Currently**: Manual process

**Steps**:
1. Account representative monitors migration
2. Representative verifies customer using new block
3. Representative submits request to NetBox
4. NetBox releases old block to IP pool

**Future Enhancement**: Automated cleanup possible with migration tracking.

## Applicable Scenarios

Zero downtime migration available for:
- Static IP 1 → Static IP 5 (upgrade)
- Static IP 5 → Static IP 1 (downgrade)
- Other block size transitions

## Benefits

✅ **Service Continuity**: No interruption to customer connectivity
✅ **Controlled Transition**: Customers manage migration at their pace
✅ **Risk Mitigation**: Avoids forced configuration changes
✅ **Testing Window**: Time to validate new IP configuration

## Immediate Replacement Alternative

Customers can opt for immediate block replacement if acceptable:
- Old block released immediately
- New block allocated and active
- Risk: Potential service interruption during customer migration


## Relationships
- **implements**: [Static IP Global Change Orders](wiki/entities/static-ip-global-change-orders.md)
- **related-to**: [CIDR Block Allocation](wiki/concepts/cidr-block-allocation.md)

## See Also
- [Static IP Global Change Orders](wiki/entities/static-ip-global-change-orders.md)
- [CIDR Block Allocation](wiki/concepts/cidr-block-allocation.md)
- [Static IP Change Scenarios](wiki/comparisons/static-ip-change-scenarios.md)