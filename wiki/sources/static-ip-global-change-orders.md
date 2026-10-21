# Static IP Global Change Orders - Architecture & Process Documentation

## Source Metadata
- **Ingested**: 2026-04-17
- **Source URL**: https://docs.internal.net
- **Last Verified**: 2026-10-21
- **Volatility**: medium

## Key Takeaways

- **Static IP CIDR blocks cannot be resized or modified** once allocated—any block size change requires release and reallocation
- **8 supported change scenarios** ranging from Dynamic IP → Static IP to Static IP → Dynamic IP, with different automation levels and downtime risks
- **Zero downtime migration approach** allows customers to temporarily maintain both old and new IP blocks during migration
- **24–48 hour migration window** provided for customers to update firewall rules, NAT, DNS, and application endpoints
- **Post-migration cleanup is manual** - account representative verifies migration and requests old block release from NetBox
- **Technical constraints** prevent some original business requirements (retaining existing IPs during block upgrades, extracting individual IPs from blocks)
- BFI and BF Pro products support two static IP options: /30 (1 usable IP) and /29 (5 usable IPs)
- System architecture involves Portal, BU Customer MS, Order MS, Dynamics, Shazam, and NetBox

## Pages Created/Updated

- [Static IP Global Change Orders](wiki/entities/static-ip-global-change-orders.md) — Detailed feature documentation
- [CIDR Block Allocation](wiki/concepts/cidr-block-allocation.md) — Technical foundation
- [Static IP Change Scenarios](wiki/comparisons/static-ip-change-scenarios.md) — 8-scenario matrix with automation and risk
- [Zero Downtime Migration](wiki/concepts/zero-downtime-migration.md) — Migration approach and process
- [Static IP Products](wiki/entities/static-ip-products.md) — BFI and BF Pro offerings

## See Also
- [Static IP Changes](wiki/entities/static-ip-changes.md)
- [Global Change Order](wiki/entities/global-change-order.md)
- [Shazam](wiki/entities/shazam.md)
- [NetBox](wiki/entities/netbox.md)
