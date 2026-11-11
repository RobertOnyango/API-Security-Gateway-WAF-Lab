Register both backends in APIM	APIM recognizes both backend services
Configure API routing	APIM forwards requests to the correct backend
Configure authentication	Unauthorized requests are rejected
Configure rate limiting	Excessive requests are restricted


# API Implementation — Patient Records and Appointments

## 1. Overview

This section contains the implementation of two independent Python Flask REST APIs:

1. **Patient Records API** — exposes patient record information and supports patient creation.
2. **Appointments API** — exposes appointment information associated with patients.

The APIs are developed independently, with their own application entry points, routes, services, and repositories. Both use an in-memory data store for demonstration purposes.

The objective is to build functional backend APIs, implement identity-based authentication and application-level authorization, and prepare them for deployment to Azure App Services.

The APIs will subsequently be exposed through Azure API Management (APIM), which provides a centralized API gateway and an additional security enforcement layer.

## 2. API Architecture and Project Structure

Both applications follow the same layered architecture:

```text
API/
│
├── app.py
│
├── routes/
│   └── ...
│
├── services/
│   └── ...
│
└── repositories/
    └── ...
```

| Component | Responsibility |
|---|---|
| `app.py` | Initializes the Flask application, registers Blueprints, and exposes the health endpoint. |
| `routes/` | Defines HTTP endpoints, receives requests, validates request structure, and returns HTTP responses. |
| `services/` | Contains application and business logic, separating request handling from data access. |
| `repositories/` | Handles data retrieval and modification. Currently uses in-memory Python data structures. |

### Health Endpoints

Each API exposes a health endpoint:

```http
GET /health
```

The endpoint confirms that the Flask application is running and identifies the relevant service.

Example response:

```json
{
  "status": "healthy",
  "service": "patient-records-api"
}
```

The Appointments API returns its corresponding service identifier.

### Current API Endpoints

**Patient Records API**

| Method | Endpoint | Description |
|---|---|---|
| GET | `/patients` | Retrieves the patient collection. |
| GET | `/patients/{patient_id}` | Retrieves an individual patient by ID. |
| POST | `/patients` | Creates a patient record. |
| GET | `/health` | Checks application health. |

**Appointments API**

| Method | Endpoint | Description |
|---|---|---|
| GET | `/appointments` | Retrieves the appointment collection. |
| GET | `/appointments/{appointment_id}` | Retrieves an individual appointment by ID. |
| GET | `/health` | Checks application health. |

The initial implementation of both APIs was reviewed and their existing endpoints tested locally.

### Local and Postman Testing

The APIs are first executed locally using Flask. Their endpoints are tested using Postman to verify:

- Successful HTTP requests and responses.
- Retrieval of collections and individual records.
- Patient creation through the POST endpoint.
- Appropriate HTTP status codes, including `200`, `201`, `400`, and `404`.
- Retrieval of a newly created patient during the running application session.

Postman is also used later to simulate authenticated API consumers and test Entra ID access tokens.

## 3. Data Model and Storage

The APIs currently use synthetic demonstration data stored in Python lists of dictionaries within their respective repository modules.

**Patient Records example:**

```python
{
    "id": 1,
    "name": "Alex Morgan",
    "date_of_birth": "1985-04-12"
}
```

**Appointment example:**

```python
{
    "id": 1,
    "patient_id": 1,
    "date": "2026-11-10T09:00:00Z",
    "status": "scheduled"
}
```

The `patient_id` field associates an appointment with a patient record.

This implementation deliberately avoids introducing a database at this stage. Data is held in application memory and is therefore not durable: records created during execution are lost when the application process restarts.

All records are synthetic. No real patient information is used.

## 4. Identity and Access Management — Microsoft Entra ID

Authentication and authorization are implemented using Microsoft Entra ID.

The design separates the identity of the consuming client application from the identities of the protected APIs.

Three Entra ID application registrations form the identity architecture.

### 4.1 Application Registrations

| Application registration | Purpose |
|---|---|
| Savannah Patient Records API | Represents the Patient Records resource API. Exposes delegated permissions and defines application roles. |
| Savannah Appointments API | Represents the Appointments resource API. Will expose its own delegated permissions and define the roles required by that API. |
| Savannah API Test Client | Represents the consuming client application, such as a future doctor-facing portal. Postman uses this registration to simulate the client during development and testing. |

**Resource API registrations**

Each API has its own application identity and audience. This allows Entra ID to issue access tokens specifically intended for the API being called.

The Patient Records API registration has been configured with:

- An Application ID URI.
- An exposed delegated permission scope: `access_as_user`.
- An enabled `Doctor` application role.
- An enabled `Administrator` application role.

The Appointments API will receive its corresponding API registration and permission configuration.

**Client application registration**

`Savannah API Test Client` represents the application consuming the APIs.

In a real deployment, this could be a doctor-facing portal, for example `savannahdochome.com`, where a doctor signs in through a browser.

For this project, Postman acts as the test client. It uses the client application's registration to request access tokens for the protected APIs.

The client registration is separate from the API registrations because the client and the resource API have different responsibilities.

### 4.2 Scopes and Application Roles

Scopes and application roles serve different purposes.

| Configuration | Purpose | Example |
|---|---|---|
| Delegated scope | Defines what an authorized client can request from an API on behalf of a signed-in user. | `access_as_user` |
| Application role | Defines the user's role and the level of access associated with that role. | `Doctor`, `Administrator` |

The client requests the delegated permission exposed by the resource API.

The application role is assigned to the user or group through the API's Enterprise Application service principal.

When the relevant role is assigned, Entra ID can include it in the access token's `roles` claim.

The delegated scope and application role are separate authorization dimensions. Having the scope does not automatically make a user a Doctor or Administrator.

### 4.3 Demonstration Users and Authorization Model

The following synthetic identities demonstrate role-based and object-level authorization.

| User | Application role | Authorized patient access |
|---|---|---|
| Dr. John | Doctor | Patient 1 |
| Dr. Mary | Doctor | Patient 2 |
| Admin Peter | Administrator | Administrative access to all patient records |

The authorization model distinguishes between having permission to use an API and being authorized to access a particular resource.

For example:

- Dr. John can retrieve Patient 1.
- Dr. John cannot retrieve Patient 2.
- Dr. Mary can retrieve Patient 2.
- Dr. Mary cannot retrieve Patient 1.
- Admin Peter has administrative access according to the defined application permissions.

The same principle applies to appointments: a doctor must be authorized to access the patient associated with the requested appointment.

These assignments are demonstration data and will be enforced by the Flask application.

## 5. Authentication and Token Issuance Flow

The implementation uses OAuth 2.0 Authorization Code Flow with PKCE for the client application, alongside OpenID Connect for user authentication.

The ID token and access token are separate artifacts issued by Microsoft Entra ID. One does not convert into the other.

### 5.1 ID Token vs. Access Token

| Token | Protocol | Intended recipient | Purpose |
|---|---|---|---|
| ID Token | OpenID Connect | Client application | Establishes the signed-in user's identity and authentication context. |
| Access Token | OAuth 2.0 | Resource API | Authorizes the client to access a particular API using the granted permissions. |

The ID token allows the client application to establish who has signed in.

The access token is sent to the backend API to authorize API requests. It contains claims relevant to the API, including user identity and granted permissions where applicable.

The backend does not use the ID token as a bearer token for API access.

### 5.2 Login and Token Issuance Flow

The following describes the intended flow using a doctor-facing portal and the Postman test client.

**Step 1 — User sign-in**

The doctor opens the client application and initiates sign-in.

The client redirects the user to Microsoft Entra ID's authorization endpoint using Authorization Code Flow with PKCE.

The authorization request includes the required OpenID Connect scopes, such as:

- `openid`
- `profile`

It also requests the delegated permission exposed by the target API, for example:

```text
api://<PATIENT_RECORDS_API_CLIENT_ID>/access_as_user
```

**Step 2 — Authentication and authorization**

Entra ID authenticates the user and evaluates the requested permissions, consent, tenant configuration, and applicable user role assignments.

**Step 3 — Authorization code**

Following successful authentication, Entra ID redirects the client with an authorization code.

**Step 4 — Token exchange**

The client exchanges the authorization code at Entra ID's token endpoint.

**Step 5 — Token issuance**

Entra ID returns the applicable tokens:

- **ID Token:** provides identity and authentication context to the client application.
- **Access Token:** grants access to the requested resource API, subject to the permissions and authorization applicable to the request.
- **Refresh Token:** may also be issued to support subsequent token renewal, depending on the client configuration and requested permissions.

The ID token and access token are separate signed tokens with different purposes and audiences.

**Step 6 — API request**

The client attaches the access token to the HTTP request:

```http
Authorization: Bearer <access_token>
```

The access token is intended for the API, not the frontend application.

### 5.3 Access Token Claims

The API access token contains claims used during authentication and authorization.

| Claim | Purpose |
|---|---|
| `aud` | Identifies the resource API for which the token was issued. |
| `iss` | Identifies the token issuer. |
| `tid` | Identifies the Entra tenant. |
| `oid` | Identifies the user within the tenant. |
| `scp` | Contains delegated scopes granted to the client. |
| `roles` | Contains applicable application role claims. |
| `exp` | Defines token expiration. |
| `nbf` | Defines when the token becomes valid. |

The implementation will use the combination of `tid` and `oid` as the stable user identity for authorization mapping.

The actual issuer, audience, and token version will be confirmed by inspecting an Entra-issued access token before configuring the validators.

## 6. JWT Validation and Defense in Depth

A central security decision is to implement **independent JWT validation at both Azure API Management and the Flask backend APIs**.

The two validation boundaries provide defense in depth.

APIM validates incoming access tokens at the gateway. Flask independently validates the original token before using its claims for application authorization.

The backend does not simply trust that a request passed through APIM.

### 6.1 JWT Signature Validation and JWKS

Microsoft Entra ID signs access tokens using its private signing keys.

The corresponding public signing keys are published through Microsoft's OpenID Connect metadata and JSON Web Key Set (JWKS) endpoint.

Flask will use PyJWT and its JWKS support to:

1. Retrieve the tenant's OpenID Connect configuration.
2. Discover the published JWKS endpoint.
3. Retrieve the public signing keys.
4. Identify the correct signing key using the JWT header's `kid`.
5. Verify the token's cryptographic signature.
6. Validate the issuer, audience, expiration, not-before time, and required tenant and permission claims.

The application will use cached signing keys with appropriate refresh handling to accommodate Entra ID signing-key rotation.

The issuer must match the expected Entra tenant and token version. The audience must match the specific API receiving the request.

The APIs will not implement their own cryptographic signing or signature-verification algorithms.

### 6.2 First Validation Boundary — Azure API Management

APIM validates the access token before forwarding the request to the backend.

Its responsibilities include:

- Verifying the JWT signature against trusted Entra signing keys.
- Validating the issuer.
- Validating the audience.
- Checking token lifetime.
- Enforcing required delegated scopes and applicable API-level role requirements.
- Rejecting invalid or unauthorized requests before they reach Flask.

Requests that fail gateway validation are rejected at APIM.

### 6.3 Second Validation Boundary — Flask Backend

After APIM accepts the request, it forwards the original Bearer access token to the relevant Flask API.

Flask independently performs JWT validation using the Entra public signing keys and the API's own validation configuration.

It verifies:

- Cryptographic signature.
- Expected issuer.
- API-specific audience.
- Expiration and not-before claims.
- Expected tenant.
- Required scope and role claims, where applicable.

Only after successful validation does Flask establish the authenticated user identity and proceed with application authorization.

This ensures that backend authentication does not depend solely on APIM's validation decision.

### 6.4 Application and Object-Level Authorization

JWT validation establishes that the access token is authentic and intended for the API. It does not establish that the user is entitled to access every record.

Flask therefore performs the application-specific authorization checks.

The authorization sequence is:

1. **Authentication:** Validate the access token and establish the user's identity.
2. **Scope authorization:** Confirm that the token has the delegated permission required by the endpoint.
3. **Role authorization:** Confirm that the user has the required application role.
4. **Object-level authorization:** Check whether the authenticated user is permitted to access the requested patient or appointment.
5. **Business logic:** Execute the requested operation only after the required checks succeed.

For example, a Doctor may have the `Doctor` role and the required API scope, but that does not automatically authorize access to every patient.

The Flask application must check the doctor's patient assignment before returning the requested record.

A valid token with insufficient permissions results in `403 Forbidden`. A missing or invalid token results in `401 Unauthorized`.

## 7. Why Azure API Management Is Used Alongside JWT Validation

JWT validation establishes whether a request carries an authentic and appropriately authorized access token. APIM provides a broader API management and gateway security layer.

It is not simply another JWT library or a replacement for the backend authentication logic.

APIM provides the following capabilities:

| Capability | Purpose |
|---|---|
| Centralized gateway | Provides a controlled entry point to the backend APIs. |
| JWT validation | Enforces token validation before requests reach the backend. |
| Subscription management | Allows APIs to be exposed through products and controlled client subscriptions. |
| Rate limiting and quotas | Restricts excessive request rates and consumption. |
| Routing and backend management | Directs requests to the appropriate private App Service backend. |
| API policies | Applies centralized request and response controls, transformations, and restrictions. |
| API versioning and products | Supports controlled API exposure and lifecycle management. |
| Monitoring and analytics | Provides visibility into API consumption, errors, and traffic patterns. |

APIM also provides a foundation for managing additional APIs and clients without implementing every gateway-level control independently in each Flask application.

**APIM is not being introduced solely to scale the APIs.** Its primary purpose here is centralized API exposure, governance, traffic management, and security enforcement. Its tier and configuration also determine its capacity and scaling options.

The resulting security architecture is:

```text
Client Application / Postman
          |
          | Entra ID Access Token
          v
Azure Application Gateway WAF
          |
          v
Azure API Management
          |
          | First JWT validation
          | Gateway policies and subscription controls
          v
Private Azure App Service
          |
          | Original Bearer access token
          v
Flask API
          |
          | Second independent JWT validation
          | Scope and role checks
          | Object-level authorization
          v
Service Layer
          |
          v
Repository Layer
          |
          v
In-memory Application Data
```

The App Services are accessed through Private Endpoints and are not intended to expose public API endpoints. Network restrictions and private connectivity complement, rather than replace, the authentication and authorization controls.

## 8. Security Controls to Be Implemented

The initial API review identified the following gaps in the application code.

| Security control | Initial implementation position | Intended implementation |
|---|---|---|
| Authentication | Not implemented | Entra ID JWT validation in APIM and Flask |
| Role-based authorization | Not implemented | Doctor and Administrator role checks |
| Object-level authorization | Not implemented | Patient and appointment assignment checks |
| Input validation | Basic Patient POST validation | Consistent request validation |
| Error handling | Basic 400 and 404 responses | Controlled and consistent error responses |
| Security audit logging | Not established | Security-relevant authentication, authorization, and application events |
| Persistent storage | Not implemented | Remains outside the current demonstration scope |

The security implementation will also include:

- Protection against Broken Object Level Authorization (BOLA).
- Controlled handling of missing, malformed, expired, or invalid tokens.
- Appropriate handling of unauthorized and forbidden requests.
- Avoidance of sensitive information and access tokens in application logs.
- Separation of authentication, authorization, business logic, and data access.

## 9. Testing and Verification

Testing will progress from individual API functionality to end-to-end security validation.

| Testing stage | Verification objective |
|---|---|
| Local Flask testing | Confirm application startup, health endpoints, and API functionality. |
| Postman functional testing | Verify GET and POST operations and expected HTTP responses. |
| Entra authentication testing | Obtain access tokens using the registered client application. |
| JWT validation testing | Test valid, expired, malformed, incorrectly signed, and wrong-audience tokens. |
| Scope and role testing | Verify required delegated permissions and application roles. |
| Object-level authorization testing | Verify that doctors cannot access unassigned patients or appointments. |
| APIM testing | Confirm that gateway policies reject invalid requests before backend execution. |
| End-to-end testing | Verify the complete request path through the gateway to the private backend. |

Expected authorization outcomes include:

| Scenario | Expected result |
|---|---|
| Unauthenticated request | 401 Unauthorized |
| Invalid or expired access token | 401 Unauthorized |
| Incorrect API audience | 401 Unauthorized |
| Missing required permission | 403 Forbidden |
| Doctor accesses an assigned patient | 200 OK |
| Doctor accesses another doctor's patient | 403 Forbidden |
| Administrator accesses an authorized record | 200 OK |
| Requested record does not exist | 404 Not Found |

## 10. Azure Deployment Preparation

Both Flask applications are designed to be independently deployable to Azure App Services.

The deployment targets are:

| API | Azure App Service |
|---|---|
| Patient Records API | `savannah-poc-patients-api` |
| Appointments API | `savannah-poc-appointments-api` |

The applications will be deployed after the implementation and security configuration stages are complete.

The deployment will retain the intended private backend architecture:

- HTTPS-only App Service configuration.
- Private Endpoint connectivity.
- Private DNS resolution.
- APIM backend integration.
- APIM-to-App Service connectivity.
- Independent backend JWT validation.

Actual deployment and deployed-endpoint DAST testing are subsequent stages; the existence of the App Services does not mean the Flask applications have already been deployed.

## 11. Implementation Scope and Limitations

The current implementation deliberately focuses on two functional APIs and their security architecture.

The following are outside the scope of this section:

- Frontend or doctor-facing portal development.
- Real hospital or patient data.
- Production relational database implementation.
- Kubernetes or container orchestration.
- Additional microservices or messaging infrastructure.
- On-Behalf-Of (OBO) token exchange.
- AI-based functionality.

Postman represents the consuming client during development and testing. A production frontend can be introduced independently without changing the fundamental distinction between the client application registration and the protected API registrations.

The in-memory repositories are demonstration implementations and are not intended for production persistence or concurrent multi-instance workloads.

---

**Implementation objective:** Deliver two independently deployable Flask APIs with a clear application architecture, Entra ID-based authentication, independent JWT validation at APIM and Flask, and application-level role and object authorization. The APIs will then be integrated through APIM and deployed to their private Azure App Service environments.

