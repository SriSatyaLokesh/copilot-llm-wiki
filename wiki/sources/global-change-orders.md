# Global Change Orders - Engineering Architecture & Technical Documentation

## Source Metadata
- **Ingested**: 2026-04-17
- **Source URL**: https://docs.internal.net
- **Last Verified**: 2026-10-21
- **Volatility**: medium

## Key Takeaways

- **Global Change Orders (GCO)** enable customers to modify account information, contacts, service configuration, and IP assignments through the portal
- Portal modifications on active accounts/services generate GCO requests submitted to Dynamics (order orchestration system)
- CXPBU microservices middleware performs validation, pricing calculation, and orchestration
- Three change categories: account-level (contact/address updates), static IP changes, and service-level changes (add-ons, upgrades, disconnects)
- GCO lifecycle includes 7 states: Initiated → Validated → Pricing Evaluated → Submitted → Processing → Completed/Rejected
- OrderMS handles rate card pricing comparison and Early Termination Fee (ETF) calculation for service disconnections
- Ziply Notification Platform integration planned for email notifications (not yet enabled)
- Portal user permissions enforce role-based authorization (Account Owner, Account Admin, Standard User)

## Pages Created/Updated

- [Global Change Order](wiki/entities/global-change-order.md) — Core feature
- [Account Level Changes](wiki/entities/account-level-changes.md) — Change category
- [Static IP Changes](wiki/entities/static-ip-changes.md) — Change category
- [Service Level Changes](wiki/entities/service-level-changes.md) — Change category
- [GCO Lifecycle](wiki/concepts/gco-lifecycle.md) — 7-state workflow
- [Change Order Categories](wiki/concepts/change-order-categories.md) — Category overview
- [Pricing Logic & Rate Card Comparison](wiki/concepts/pricing-logic.md) — Price evaluation
- [ETF Calculation](wiki/concepts/etf-calculation.md) — Early termination fees
- [Participating Systems](wiki/comparisons/participating-systems.md) — System architecture table
- [CXPBU OrderMS](wiki/entities/cxpbu-orderms.md) — Microservice
- [CXPBU CustomerMS](wiki/entities/cxpbu-customerms.md) — Microservice
- [CXPBU CADMS](wiki/entities/cxpbu-cadms.md) — Microservice
- [Dynamics](wiki/entities/dynamics.md) — Order orchestration system
- [Shazam](wiki/entities/shazam.md) — Network provisioning
- [NetBox](wiki/entities/netbox.md) — Network IPAM
- [Ziply Notification Platform](wiki/entities/ziply-notification-platform.md) — Notification service
- [Portal Authorization & Roles](wiki/concepts/portal-authorization-roles.md) — User permissions

## See Also
- [Global Change Order](wiki/entities/global-change-order.md)
- [Change Order Categories](wiki/concepts/change-order-categories.md)
- [Participating Systems](wiki/comparisons/participating-systems.md)
