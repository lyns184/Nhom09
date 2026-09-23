# Security Requirements for `json_search()`

## 1. Access-Control Requirements

### SR-01: Role-based authorization

The function shall accept a role through the following interface:

```python
json_search(key, input_object, role=None)
```

Before returning a protected value, the function shall check whether the provided role is listed for that key in `POLICY`.

### SR-02: Protection of `apiKey`

Only the `admin` role shall be allowed to read `apiKey`.

| Role | Expected result |
|---|---|
| `admin` | Matching values are returned |
| `operator` | An empty list is returned |
| `viewer` | An empty list is returned |

### SR-03: Protection of `managementIpAddress`

Only the `admin` and `operator` roles shall be allowed to read `managementIpAddress`.

| Role | Expected result |
|---|---|
| `admin` | Matching values are returned |
| `operator` | Matching values are returned |
| `viewer` | An empty list is returned |

### SR-04: Access to `issueSummary`

The `admin`, `operator`, and `viewer` roles shall be allowed to read `issueSummary`.

### SR-05: Unauthorized roles

If a role is not included in the permission list for a protected key, the function shall return an empty list.

### SR-06: Missing or unknown roles

If the caller provides no role or an unknown role for a protected key, the function shall return an empty list.

### SR-07: Recursive authorization

The same access-control decision shall apply at every recursion level, including values stored inside nested dictionaries and lists.

### SR-08: No partial disclosure

When access is denied, the function shall not return partial values, metadata, or information indicating the location of the protected field.

## 2. Functional Security Requirements

### SR-09: Complete recursive search

For an authorized request, the function shall aggregate all matching values from nested dictionaries and lists without dropping results from recursive calls.

### SR-10: Safe not-found behavior

If the requested key does not exist, the function shall return an empty list.

### SR-11: Consistent return type

The function shall always return a list, regardless of whether the search is authorized, denied, successful, or unsuccessful.

### SR-12: Policy consistency

The function shall use the permissions defined in `policy.py` as the authoritative access-control policy. Access rules shall not be duplicated with hard-coded role checks inside the search logic.

## 3. Required Security Tests

The test suite shall verify at least the following cases:

1. `admin` can read `apiKey`.
2. `operator` cannot read `apiKey`.
3. `viewer` cannot read `apiKey`.
4. `operator` can read `managementIpAddress`.
5. `viewer` cannot read `managementIpAddress`.
6. `viewer` can read `issueSummary`.
7. A missing role cannot read a protected field.
8. An unknown role cannot read a protected field.