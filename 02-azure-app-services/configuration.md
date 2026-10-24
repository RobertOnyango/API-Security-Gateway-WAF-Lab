# Azure App Servive Deployment

## Purpose

Azure App Service provides the managed hosting environment for the two APIs developed in this project: **Patient Records API** and **Appointments API**.

The APIs are hosted within one Python application but exposed through separate API paths and subsequently published independently through Azure API Management.

---

## Design Decision

A single App Service is used to host both APIs to minimise infrastructure complexity and cost in this proof of concept.

This does not provide application-level isolation between the two APIs. Separate applications or hosting plans may be considered for production environments requiring stronger isolation.

---

## Configuration

### App Service Plan

Provision an **App Service Plan** to define the set of resources that the web app will run.

| Property | Configuration |
|----|----|
| Name | app-plan-savannah-security-poc |
| Operating System | Linux |
| Region | West US 3 |
| Pricing Plan | Basic |

### Azure Web App

After successful deployment, proceed to provision the **Azure Web App** via **App Services** with the following configurations:

### Basics Tab

| Property | Configuration | Notes |
|----|----|----|
| Name | savannah-poc-patients-api | Must be globally unique |
| Publish | Code | Simpler for this demo |
| Runtime Stack | Python 3.14 |
| Operating System | Linux | Matches the App Service Plan |
| Region | West US 3 |
| Pricing Plan | Linux Plan (West US 3) | app-plan-savannah-security-poc |

- No database is required
- Continous deployment: Disable

### Networking Tab

| Property | Configuration | Notes |
|----|----|----|
| Enable Public Access | Off | Web Apps should only communicate with internal trusted systems |
| Enable virtual network intergration | On | Allows configuration for internal communiction |
| Virtual Network | VNet-savannah-security-poc (rg-savannah-security-poc) |
| Inbound Access (Enable Private Endpoints) | On |
| Inbound Access (Private endpoint name) | patients-api-endpoint |
| Inbound Access (Inbound Subnet) | appointments-api-endpoint |
| Inbound Access (DNS) | Azure Private DNS Zone |
| Outbound Access (Enable VNet integration) | On
| Outbound Access (Outbound subnet) | subnet-apis |


- Monitor & Secure: Leave defaults

**NOTE**: Use the same configurations for the appointments Web Service, only changing the following entries: 
- Basics Tab - Name: savannah-poc-appointments-api
- Networking Tab - Inbound Access (Private endpoint name): appointments-api-endpoint

---


