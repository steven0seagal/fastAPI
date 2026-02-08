# API Walkthrough

Base URL (Docker): `http://localhost:8000`

## 1) Get a token

```bash
curl -sS -X POST \
  -d 'username=admin@lab.local' \
  -d 'password=admin123' \
  http://localhost:8000/auth/token
```

Export the token:

```bash
TOKEN="..."
```

## 2) List test catalog

```bash
curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/catalog/tests
```

## 3) Create a patient

```bash
curl -sS -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"external_id":"MRN-001","first_name":"Jan","last_name":"Kowalski"}' \
  http://localhost:8000/patients
```

## 4) Create an order

```bash
curl -sS -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"patient_id":1,"test_codes":["HGB","WBC"],"notes":"Routine"}' \
  http://localhost:8000/orders
```

## 5) Submit a result

Find a `test_request_id` from the order response, then:

```bash
curl -sS -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"value": 10.5, "unit": "g/dL"}' \
  http://localhost:8000/orders/test-requests/1/result
```

Celery will compute `interpretation` and update the order status asynchronously.
