# Ziply Notification Platform

## Overview

Ziply Notification Platform is the email notification service for the Business Portal. It will be integrated to send customer notifications for account and service changes triggered through Global Change Orders.

## Key Facts

- **Role**: Email notification service (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Scope**: Customer communications for portal-initiated changes (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Status**: Integration planned, not yet enabled (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)
- **Triggered Events**: Contact phone updates, billing address changes, contact updates (Source: [global-change-orders](wiki/sources/global-change-orders.md), 2026-10-21)

## Trigger Events

- Contact phone updated
- Billing address changed
- Billing contact updated
- Technical contact updated
- Service configuration changed
- Service disconnection initiated

## Integration Status

- **Current**: Not yet enabled
- **Future**: Will send email notifications to affected customers and stakeholders


## Relationships
- **part-of**: [Participating Systems](wiki/comparisons/participating-systems.md)
- **related-to**: [Global Change Order](wiki/entities/global-change-order.md)

## See Also
- [Global Change Order](wiki/entities/global-change-order.md)
- [Account Level Changes](wiki/entities/account-level-changes.md)
- [Service Level Changes](wiki/entities/service-level-changes.md)