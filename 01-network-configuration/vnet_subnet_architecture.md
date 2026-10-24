# Azure Virtual Network Architecture

## Overview

The solution uses a single Azure Virtual Network to provide private connectivity between the API gateway, API management layer and backend application services.

**VNet**: Vnet-savannah-security-poc
**Address Space**: 10.0.0.0/16
**Region**: West US 3

---

## Subnet Design

| Subnet | Address Prefix | Purpose |
|-----|-----|-----|
| subnet-wafgw | 10.0.1.0/24 | Application Gateway WAF v2 |
| subnet-apimgmt | 10.0.2.0/24 | API Management Service v2 (vNet injection) |
| subnet-apis | 10.0.3.0/24 | App Services outbound connection |
| subnet-private-endpoints | 10.0.4.0/24 | Private endpoints for backend Web APIs inbound traffic|

---

