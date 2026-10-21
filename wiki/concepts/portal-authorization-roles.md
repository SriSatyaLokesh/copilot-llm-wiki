# Portal Authorization & Roles

## Definition

Portal Authorization & Roles is the access control mechanism that determines which operations customers can perform in the Business Portal based on their assigned role. Role-based permissions enforce business rules and prevent unauthorized modifications to accounts and services.

## How It Works

### Role-Based Access Control (RBAC)

Portal user permissions are strictly governed by assigned roles. The system enforces these permissions at the API level to prevent unauthorized operations.

### User Roles

| Role | Permissions | Scope |
|------|-------------|-------|
| **Account Owner** | All account and service changes | Full access to all account modifications, service changes, contact updates, IP changes |
| **Account Admin** | Account and contact updates | Restricted to account metadata changes (contacts, addresses); no service or IP modifications |
| **Standard User** | Limited service operations | Restricted to read-only access and basic service inquiries; no modifications |

### Supported Operations by Role

#### Account Owner
- ✅ Change contact phone numbers
- ✅ Update billing address
- ✅ Add/remove billing contacts
- ✅ Add/remove technical contacts
- ✅ Add/remove local/IT contacts
- ✅ View assigned static IPs
- ✅ Request static IP changes
- ✅ Modify service add-ons
- ✅ Upgrade/downgrade services
- ✅ Request service disconnection

#### Account Admin
- ✅ Change contact phone numbers
- ✅ Update billing address
- ✅ Add/remove billing contacts
- ✅ Add/remove technical contacts
- ✅ Add/remove local/IT contacts
- ❌ View assigned static IPs (no access)
- ❌ Request IP changes (no access)
- ❌ Modify service add-ons (no access)
- ❌ Upgrade/downgrade services (no access)
- ❌ Request disconnection (no access)

#### Standard User
- ✅ View account information (read-only)
- ✅ View assigned static IPs (read-only)
- ✅ View service configurations (read-only)
- ❌ Make any modifications

### Authorization Enforcement

1. **Portal Frontend**: Disables unavailable options based on user role
2. **Portal Backend**: Validates user permissions before accepting requests
3. **API Gateway**: Enforces authorization at API level
4. **Middleware**: Re-validates permissions before processing Global Change Orders
5. **Dynamics**: Final authority for contract and account data

### Permission Validation Flow

```
User submits request
  ↓
Portal Frontend checks role permissions
  ↓
Portal Backend validates authorization
  ↓
API Gateway enforces permissions
  ↓
Middleware validates permissions again
  ↓
Request processed (if authorized) or rejected (if unauthorized)
```

## Security Best Practices

- **Principle of Least Privilege**: Users assigned minimal required permissions
- **Role Hierarchy**: Standard User < Account Admin < Account Owner
- **Multi-layer Validation**: Permissions checked at every system boundary
- **Audit Trail**: All operations logged with requesting user and role
- **Token-based Access**: API authentication via session tokens with embedded role info


## Relationships
- **part-of**: [Commercial Portal](wiki/entities/commercial-portal.md)
- **related-to**: [Global Change Order](wiki/entities/global-change-order.md)

## See Also
- [Global Change Order](wiki/entities/global-change-order.md)
- [Account Level Changes](wiki/entities/account-level-changes.md)
- [Service Level Changes](wiki/entities/service-level-changes.md)