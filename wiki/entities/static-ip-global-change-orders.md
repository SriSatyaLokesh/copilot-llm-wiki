# Static IP Global Change Orders

## Overview

Static IP Global Change Orders enable customers to modify their IP configuration (from Dynamic to Static, or between Static block sizes) after service activation. The feature allows BFI and BF Pro customers to adjust their static IP allocation while managing the technical constraints of CIDR block allocation—specifically, that blocks cannot be resized once allocated.

## Key Facts

- **CIDR Block Model**: Static IPs allocated in CIDR blocks (/30 = 1 usable IP, /29 = 5 usable IPs) (Source: [static-ip-global-change-orders](wiki/sources/static-ip-global-change-orders.md), 2026-10-21)
- **Technical Constraint**: CIDR blocks cannot be resized; block size changes require release + reallocation (Source: [static-ip-global-change-orders](wiki/sources/static-ip-global-change-orders.md), 2026-10-21)
- **Change Scenarios**: 8 supported scenarios (Dynamic→Static, Static IP 1↔5, Static→Dynamic) with varying automation levels (Source: [static-ip-global-change-orders](wiki/sources/static-ip-global-change-orders.md), 2026-10-21)
- **Zero Downtime Migration**: Customers can temporarily maintain both old and new blocks during migration (Source: [static-ip-global-change-orders](wiki/sources/static-ip-global-change-orders.md), 2026-10-21)
- **Migration Window**: 24–48 hours provided for customers to update their network configuration (Source: [static-ip-global-change-orders](wiki/sources/static-ip-global-change-orders.md), 2026-10-21)
- **Post-Migration Cleanup**: Manual process requiring account representative verification before old block release (Source: [static-ip-global-change-orders](wiki/sources/static-ip-global-change-orders.md), 2026-10-21)
- **System Architecture**: Portal UI/Backend, BU Customer MS, Order MS, Dynamics, Shazam, NetBox (Source: [static-ip-global-change-orders](wiki/sources/static-ip-global-change-orders.md), 2026-10-21)
- **Services Supported**: BFI (Business Fiber Internet) and BF Pro (Business Fiber Pro) (Source: [static-ip-global-change-orders](wiki/sources/static-ip-global-change-orders.md), 2026-10-21)

## Change Scenario Categories

### New Allocations (No Downtime Risk)
- Dynamic IP → Static IP 1 (/30)
- Dynamic IP → Static IP 5 (/29)

### Block Upgrades/Downgrades (Potential Downtime)
- Static IP 1 → Static IP 5 (Immediate or Zero Downtime)
- Static IP 5 → Static IP 1 (Immediate or Zero Downtime)

### Complete Removal (Potential Downtime)
- Static IP 1 → Dynamic IP
- Static IP 5 → Dynamic IP

## Unsupported Business Requirements

Due to CIDR block technical constraints, the following are **not supported**:
- Retain existing IP when upgrading /30 → /29 (CIDR blocks cannot be resized)
- Extract single IP from larger block (not supported in IPAM)
- Add additional IPs to existing block without reallocation

## System Configuration Retrieval

When customers access the portal to view their IP configuration:
```
Portal UI → Portal Backend → BU Customer MS → Shazam → NetBox
```

System retrieves current IP block, usable IPs, and configuration type.


## Relationships
- **implements**: [CIDR Block Allocation](wiki/concepts/cidr-block-allocation.md)
- **implements**: [Zero Downtime Migration](wiki/concepts/zero-downtime-migration.md)
- **depends-on**: [Shazam](wiki/entities/shazam.md)
- **depends-on**: [NetBox](wiki/entities/netbox.md)

## See Also
- [CIDR Block Allocation](wiki/concepts/cidr-block-allocation.md)
- [Static IP Change Scenarios](wiki/comparisons/static-ip-change-scenarios.md)
- [Zero Downtime Migration](wiki/concepts/zero-downtime-migration.md)
- [Static IP Products](wiki/entities/static-ip-products.md)
- [Static IP Changes](wiki/entities/static-ip-changes.md)
- [Global Change Order](wiki/entities/global-change-order.md)