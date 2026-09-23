# Threat Model for `json_search()`

## 1. System Overview

The `json_search()` function recursively searches for a specified key in
JSON data returned by a network infrastructure monitoring API.

The input data may contain nested dictionaries and lists, including device
identifiers, internal network information, incident details, and
authentication secrets.

The function may be called by authenticated users with one of the following
roles:

| Role | Purpose |
|---|---|
| `admin` | System administration, configuration, and advanced troubleshooting |
| `operator` | Network monitoring and incident handling |
| `viewer` | Viewing general incident information |

## 2. Assets

The assets that require protection include:

| Asset | Sensitivity | Reason |
|---|---|---|
| `apiKey` | Critical | It contains an authentication secret or SNMP community string |
| `managementIpAddress` | Sensitive | It reveals an internal device management address |
| `issueSummary` | Internal | It describes an infrastructure incident |
| Device identifiers | Sensitive | They reveal information about internal network devices |
| JSON monitoring data | Internal | It may contain infrastructure and operational information |

## 3. Trust Boundaries

The following trust boundaries exist:

1. The caller sends a search key, JSON object, and role to `json_search()`.
2. The caller-provided role crosses the boundary between the user and the
   search function.
3. The JSON data crosses the boundary between the monitoring API and the
   search function.
4. Search results cross the boundary from the application to the caller.

The function must not trust the role blindly. The surrounding application
must authenticate the user and provide a trusted role before calling
`json_search()`.

The function is responsible for checking whether that role is authorized
to access the requested field.

## 4. STRIDE Threat Analysis

| ID | STRIDE Category | Threat | Security Impact | Mitigation |
|---|---|---|---|---|
| T-01 | Spoofing | A caller claims to have the `admin` role | Unauthorized access to protected data | The surrounding application must authenticate users and provide a trusted role |
| T-02 | Tampering | A caller supplies malformed or manipulated JSON data | Incorrect results or unexpected processing | Process only supported `dict` and `list` structures |
| T-03 | Repudiation | A caller denies requesting a sensitive field | Sensitive access cannot be traced | The surrounding application should log sensitive access attempts |
| T-04 | Information Disclosure | A `viewer` or `operator` requests `apiKey` | Authentication secrets may be exposed | Check the role against `POLICY` before returning results |
| T-05 | Denial of Service | Extremely large or deeply nested JSON consumes excessive resources | The function or application becomes unavailable | The surrounding application should limit input size and nesting depth |
| T-06 | Elevation of Privilege | A `viewer` accesses a field reserved for `admin` or `operator` | The caller gains permissions beyond the assigned role | Deny requests from roles not listed for the requested key |

## 5. Main Threats

### Information Disclosure

The original search function returns matching values without checking the
caller's role. As a result, an unauthorized caller may retrieve `apiKey`,
`managementIpAddress`, or other protected infrastructure information.

### Elevation of Privilege

Without role-based access control, a `viewer` can request the same protected
fields as an `admin`. This gives the viewer privileges beyond those assigned
by the access-control policy.

## 6. Assumptions and Scope

- User authentication is handled by the surrounding application.
- `json_search()` performs authorization based on the supplied role.
- The permissions in `policy.py` are the authoritative access-control rules.
- Logging, input-size limits, and user authentication are outside the scope
  of this function.