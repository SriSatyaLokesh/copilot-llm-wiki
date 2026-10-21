# CIDR Block Allocation

## Definition

CIDR Block Allocation is the fundamental networking model used to assign static IP addresses to BFI and BF Pro customers. CIDR (Classless Inter-Domain Routing) blocks define contiguous ranges of IP addresses reserved for a specific service, with some addresses reserved for networking infrastructure (gateway, broadcast, network address).

## How It Works

### Block Sizes Supported

| Option | CIDR Block | Total IPs | Reserved | Usable IPs |
|--------|-----------|-----------|----------|-----------|
| Static IP 1 | /30 | 4 | 3 (network, gateway, broadcast) | 1 |
| Static IP 5 | /29 | 8 | 3 (network, gateway, broadcast) | 5 |

### Example: /30 Block

```
Block: 192.168.10.0/30

192.168.10.0  → Network Address (reserved)
192.168.10.1  → Gateway (reserved)
192.168.10.2  → Customer Usable
192.168.10.3  → Broadcast (reserved)
```

Result: **1 usable IP** for customer

### Example: /29 Block

```
Block: 192.168.20.0/29

192.168.20.0  → Network Address (reserved)
192.168.20.1  → Gateway (reserved)
192.168.20.2 → Customer Usable
192.168.20.3 → Customer Usable
192.168.20.4 → Customer Usable
192.168.20.5 → Customer Usable
192.168.20.6 → Customer Usable
192.168.20.7  → Broadcast (reserved)
```

Result: **5 usable IPs** for customer

## Technical Constraints

**Critical Limitation**: CIDR blocks **cannot be resized once allocated**.

This means:
- A /30 block cannot be expanded to /29
- A /29 block cannot be reduced to /30
- Individual IPs cannot be extracted from a block
- Blocks cannot be partially modified

### Implication for Static IP Changes

Any change in block size requires:
1. **Release** the existing block (return to IP pool)
2. **Allocate** a new block (request new size from IP pool)

This creates potential service interruption if not handled carefully.

## Managed by Systems

- **NetBox**: IP allocation tracking and inventory
- **Shazam**: IP assignment to customer services


## Relationships
- **implements**: [Static IP Global Change Orders](wiki/entities/static-ip-global-change-orders.md)
- **depends-on**: [NetBox](wiki/entities/netbox.md)

## See Also
- [Static IP Global Change Orders](wiki/entities/static-ip-global-change-orders.md)
- [Static IP Products](wiki/entities/static-ip-products.md)
- [Zero Downtime Migration](wiki/concepts/zero-downtime-migration.md)
- [NetBox](wiki/entities/netbox.md)
- [Shazam](wiki/entities/shazam.md)