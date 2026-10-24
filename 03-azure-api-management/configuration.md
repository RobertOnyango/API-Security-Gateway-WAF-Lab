# Azure API Management Services (APIM)

## Overview

Azure API Management (APIM) provides the API gateway layer between the Application Gateway WAF and the backend applications.

It manages API exposure, request routing, authentication policies and traffic control for the Patient Records and Appointments APIs.

APIM will be responsible for enforcing controls such as:
- JWT token validation.
- Rate limiting and throttling.
- API subscription and access management.
- Request and response transformations.
- API versioning.
- Routing requests to the correct backend.

---

## Configuration

| Property | Configuration |
|----|----|
| Region | West US 3 |
| Name | apimgmt-savannah-security-poc |
| Pricing Tier | Developer |
| Connectivity Type | Virtual Network |
| Virtual Network Type | Internal |
| Virtual Network | VNet-savannah-security-security-poc |
| Subnets | subnet-apimgmt |

---

## Security Responsibilities

API Management  will be configured to enforce API-level security controls, including:

- JWT token validation.
- Request throttling and rate limiting.
- API request and response policies.
- Backend routing and access control.

Backend applications remain responsible for application-level authorization and resource ownership validation.

---

## Implementation Notes

The following configurations will be completed during subsequent implementation stages:

Private DNS configuration and validation.

Application Gateway integration.

Backend API registration and routing.

JWT validation policies.

Rate limiting policies.

Network Security Group rules.

API logging and Microsoft Sentinel integration.