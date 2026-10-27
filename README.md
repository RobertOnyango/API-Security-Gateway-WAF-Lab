# API Security Gateway & WAF Lab

## 1. Overview

This project demonstrates the design, implementation, and security testing of an Azure-hosted API environment.

The lab focuses on securing backend APIs through multiple layers of protection, including:

- Azure Application Gateway Web Application Firewall (WAF).
- Azure API Management (APIM).
- Azure Private Endpoints and Private DNS.
- Network segmentation and access controls.
- JWT authentication and API authorization.
- API security testing and attack simulation.
- Centralized security monitoring using Microsoft Sentinel.

The objective is to build a practical API security environment that demonstrates how requests are securely exposed, authenticated, routed, inspected, and delivered to backend applications.

## 2. Architecture Overview

The intended architecture uses Azure Application Gateway as the public entry point, with APIM managing API traffic and communicating privately with backend applications.

The environment consists of two backend services:

1. Patient Records API
2. Appointments API

### Intended Request Flow

<image>

Microsoft Sentinel and Log Analytics will provide centralized security monitoring and visibility. They are supporting services rather than components in the application request path.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Cloud Platform | Microsoft Azure |
| Network Infrastructure | Azure Virtual Network and Subnets |
| Public API Gateway | Azure Application Gateway WAF v2 |
| API Management | Azure API Management |
| Backend Hosting | Azure App Service |
| Private Connectivity | Azure Private Endpoints |
| Name Resolution | Azure Private DNS |
| Identity and Authentication | JWT |
| Security Monitoring | Microsoft Sentinel |
| Log Management | Azure Log Analytics |
| Security Testing | PowerShell, curl and API testing tools |
| Documentation | Markdown |

## 4. Repository Structure

```text
API-Security-Gateway-WAF-Lab/
│
├── 01-network-configuration/
├── 02-azure-app-services/
├── 03-azure-api-management/
├── 04-application-gateway/
├── 05-network-connections/
│
├── apis/
├── authentication/
├── evidence/
├── monitoring/
├── security-testing/
├── Tests/
│
└── README.md
```

Each directory contains documentation and implementation evidence for its respective component or security activity.

## 5. Implementation Progress

The project is being implemented incrementally, with each infrastructure component configured, documented, and verified before proceeding to the next stage.

| Component | Progress |
|---|---|
| Network configuration | Work started |
| Azure App Services | Work started |
| Azure API Management | Work started |
| Application Gateway WAF | Work started |
| Network connections | Work started |
| API backend registration and routing | Pending |
| Authentication and authorization | Pending |
| Security testing | Pending |
| Monitoring and Sentinel integration | Pending |

*Progress reflects work undertaken and documented so far; it does not imply that every component has passed end-to-end validation.*

## 6. Security Testing Objectives

Once the infrastructure and APIs are operational, the lab will be used to demonstrate practical API security testing.

The planned test cases include:

| Test Scenario | Expected Outcome |
|---|---|
| Valid JWT | Request proceeds |
| Missing JWT | Rejected by APIM |
| Invalid JWT | Rejected by APIM |
| Expired JWT | Rejected by APIM |
| Excessive requests | Rate limiting triggered |
| SQL injection payload | WAF/application defenses tested |
| Unauthorized patient-record access | Backend denies access |
| Direct public Web App access | Connection denied |
| Access to Appointments API | Correct API receives the request |

These are intended test cases, not results already obtained.

## 7. Expected Practical Demonstration

The final objective is to demonstrate the complete request lifecycle using VS Code and API testing tools.

The demonstration will involve:

1. Generating an authenticated API request.
2. Sending the request through the Application Gateway.
3. Observing APIM validate and route the request.
4. Receiving the correct response from the backend.
5. Modifying requests to simulate common attacks.
6. Observing the relevant security controls block or detect the activity.
7. Investigating the resulting security events in Microsoft Sentinel.

## 8. Project Approach

Implementation follows a progressive engineering approach:

1. Understand the technology and its security purpose.
2. Document the intended architecture and configuration.
3. Deploy and configure the Azure resource.
4. Establish the required network or service connection.
5. Validate connectivity and expected behavior.
6. Capture implementation evidence.
7. Document the completed configuration and findings.

The project will distinguish between planned configurations, implemented controls, and successfully validated security outcomes.

## 9. Project Outcome

The intended outcome is a working, documented API security environment that demonstrates practical experience in:

- Azure cloud infrastructure and networking.
- API gateway architecture.
- Web Application Firewall configuration.
- Private application connectivity.
- API authentication and authorization.
- Web and API attack simulation.
- Security monitoring and threat investigation.

This lab is designed as a practical cybersecurity engineering portfolio project, emphasizing implementation, validation, and security reasoning rather than infrastructure deployment alone.

<!-- Futher advancements: 

Security Testing: 
    - authentication tests
    - authorization tests
    - bola-tests
    - injection-tests
    - rate-limiting-tests

Monitoring and Log Analysis:
    - Log sources
    - Queries
--->