# Azure Application Gateways

## Overview

Azure Application Gateway WAF v2 provides the first layer of web protection in the Savannah API Security Gateway and WAF Lab. 

It acts as the internet-facing entry point for API traffic, inspecting incoming HTTP/HTTPS requests and protecting backend services against common web application attacks.

The Application Gateway uses the Web Application Firewall (WAF) capability to inspect requests against configured security rules, including protections against common attacks such as SQL injection and cross-site scripting (XSS).

It sits in front of Azure API Management (APIM), which provides the next layer of API-specific security controls.

---

## Configuration

### Basics 

| Property | Configuration |
|----|----|
| Application gateway name | appgw-savannah-security-poc
| Region | West US 3 |
| Tier | WAF V2 |
| Enable autoscaling | No |
| Instance Count | 1 |
| IP Address Type | IPv4 Only |
| HTTP2 | Enabled |
| FIPS | Disabled | 
| WAF Policy | savannah-L7-security |
| Virtual network | VNet-savannah-security-poc |
| Subnet | subnet-wafgw (10.0.1.0/24) |

---

### Frontend Tab

Defines how external clients connect to the Application Gateway. 

A **Public Frontend IP** is used because external API consumers must be able to reach the WAF from the internet.

| Property | Configuration |
|----|----|
| Frontend IP address type | Public |
| Public IPv4 address | (New) publicip-savannah-gw |

--- 

### Backend Tab

A backend pool is a collection of resources to which the Application Gateway forwards incoming traffic. 

For this setup. Application Gateway forwards traffic to Azure API Management (APIM), not directly to the two backend Web Apps.

Click on **Add a backend pool**.

| Property | Configuration |
|----|----|
| Name | backend-savannah-gw |
| Targets | 0 (Will be configured after the Azure API Management is done) |

The APIM endpoint will be added after APIM has been deployed and its network connectivity has been established.

---

### Configuration Tab

Application Gateway uses listeners and routing rules to determine how incoming requests are processed and forwarded.

A listener identifies the frontend IP, port and protocol on which the gateway receives traffic. A routing rule connects that listener to a backend pool and its associated backend settings.

| Property | Configuration |
|----|----|
| Rule Name | public-api-to-apim |
| Listener name | listener-public-api |
| Priority | 100 |
| Frontend IP | Public IPv4 |
| Protocol | 80 |
| Listener Type | Basic |
| Backend Type | Backend pools(s) |
| Backend pool | backend-savannah-gw |
| Backend settings name | savannah-api-rule |

---