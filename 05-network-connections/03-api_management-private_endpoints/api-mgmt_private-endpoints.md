# APIM to Patient Records API Connection

## 1. Overview

This connection configures Azure API Management (APIM) to securely communicate with the Patient Records backend App Service through its Private Endpoint.

---

## 2. Connection Architecture

| Component | Configuration |
|---|---|
| Source | `apimgmt-savannah-security-poc` |
| Source Network | `vnet-savannah-security-poc` |
| Destination-1 | `savannah-poc-patients-api` (IP `10.0.4.4`) |
| Destination-2 | `savannah-poc-appointments-api` (IP `10.0.4.5`) |
| Private Endpoint-1 | `patients-api-endpoint` |
| Private Endpoint-2 | `appointments-api-endpoint` |
| Connection Method | Private Endpoint |

---

## 3. Backend Configuration

This section documents the backend configuration in APIM, including the backend URL, connection protocol, and settings required for APIM to communicate with the backend APIs through their Private Endpoint.

Navigate to the **Overview page** of the two App Services to obtain their respective **Default Domain** values.

Navigation *apimgmt-savannah-security-poc->APIs->Backend*

#### Appointments API APP service

| Property | Configuration |
|---|---|
| Backend Name | backend-savannah-poc-appointments |
| Backend Hosting Type | Azure resource |
| Runtime URL | https://savannah-poc-appointments-api-d3gngwb9azhtgah6.westus3-01.azurewebsites.net |
| Authentication | Pending |

#### Patients API APP Service

| Property | Configuration |
|---|---|
| Backend Name | backend-savannah-poc-patients |
| Backend Hosting Type | Azure resource |
| Runtime URL | https://savannah-poc-patients-api-gbdgejawhcaqesde.westus3-01.azurewebsites.net |
| Authentication | Pending |

---

## 4. Connectivity Testing

Connectivity between APIM and the Patient Records API will be validated after backend registration.

| Test | Expected Result | Status |
|---|---|---|
| Backend hostname resolution | Resolves to `10.0.4.4` | Pending |
| APIM-to-backend connectivity | Successful response | Pending |
| API request through APIM | Expected HTTP response | Pending |

---

## 5. Implementation Status

- [ ] Backend registered in APIM.
- [ ] Backend URL configured.
- [ ] API routing configured.
- [ ] Backend connectivity tested.
- [ ] API request successfully processed through APIM.

---

## 6. Evidence

---

Azure configuration screenshots and connectivity test results will be added as implementation progresses.

## 7. Implementation Notes

Document any configuration decisions, connectivity issues, and resolutions encountered during implementation.

---