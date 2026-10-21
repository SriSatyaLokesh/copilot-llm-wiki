# Static IP Changes

## Overview

Static IP Changes enable customers to view their assigned static IP addresses and request modifications through the portal. This category includes both viewing assigned IPs and requesting IP block changes.

## Key Facts

- **Data Sources**: IP assignment from Shazam, network inventory from NetBox (Source: [static-ip-global-change-orders](wiki/sources/static-ip-global-change-orders.md), 2026-10-21)
- **Scope**: View and request modification of assigned static IPs (Source: [static-ip-global-change-orders](wiki/sources/static-ip-global-change-orders.md), 2026-10-21)
- **Change Order Trigger**: IP modification requests generate Global Change Orders (Source: [static-ip-global-change-orders](wiki/sources/static-ip-global-change-orders.md), 2026-10-21)

## View Assigned Static IPs

### API Endpoint
```
GET /services/{serviceId}/static-ips
```

### Response Example
```json
{
  "serviceId": "BFI-12345",
  "ipBlocks": [
    {
      "blockType": "/29",
      "usableIps": [
        "192.168.10.2",
        "192.168.10.3",
        "192.168.10.4"
      ]
    }
  ]
}
```

### Flow
Portal UI → Portal Backend → OrderMS → Dynamics → Shazam → NetBox → Response returned through same chain

## Request Static IP Change

Generates a Global Change Order that flows through the standard GCO lifecycle.

### API Endpoint
```
POST /services/{serviceId}/ip-change-request
```

### Payload
```json
{
  "serviceId": "BFI-12345",
  "requestedBlockType": "/29",
  "justification": "Infrastructure expansion"
}
```

### Flow
Portal → Portal Backend → OrderMS → Create GCO → Submit to Dynamics → Dynamics Provisioning → Shazam → NetBox


## Relationships
- **part-of**: [Global Change Order](wiki/entities/global-change-order.md)
- **related-to**: [Static IP Global Change Orders](wiki/entities/static-ip-global-change-orders.md)

## See Also
- [Global Change Order](wiki/entities/global-change-order.md)
- [Change Order Categories](wiki/concepts/change-order-categories.md)
- [Shazam](wiki/entities/shazam.md)
- [NetBox](wiki/entities/netbox.md)