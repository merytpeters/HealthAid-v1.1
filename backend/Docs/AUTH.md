# HealthAid Authentication Structure

## User Hierarchy Overview

The HealthAid application will implement a multi-tenant authentication system supporting different user types and access levels.

### System Level
- **App Admin** - Global system administrator with full platform access

### Organization Level (Care Homes)
- **Organization Admin** - Manages the care home organization, staff, and residents
- **Staff** - Care home employees who manage patient care and records
- **Users/Patients** - Residents or patients receiving care within the organization

### Individual Level
- **Individual** - Self-managing users who handle their own health data

## Authentication Method
The system will use JWT-based authentication with role-based access control (RBAC) to ensure proper data isolation and permission management across all user types.

## Multi-Tenant Architecture
Each organization operates independently with isolated data, while individual users maintain their own separate health records and management capabilities.
Each staff can belong to multiple organizations
