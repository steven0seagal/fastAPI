# Domain: Diagnostics Laboratory

This repository uses a simplified diagnostics lab/LIS domain to keep examples realistic.

## Core Entities

- **Patient**: person receiving tests.
- **Test Catalog Item**: a test definition (code, name, unit, reference range).
- **Lab Order**: a request for one or more tests for a patient.
- **Test Request**: a single requested test that belongs to an order (one per catalog item).
- **Sample**: a collected specimen linked to an order.
- **Test Result**: the measured value for a test request.

## Statuses

### LabOrder.status

- `new`: order created, no results yet
- `in_progress`: at least one result exists
- `completed`: all non-cancelled test requests are resulted
- `cancelled`: order should not progress further

### TestRequest.status

- `requested`: created as part of an order
- `resulted`: a result was submitted
- `cancelled`: a test request was cancelled

### Sample.status

- `collected`: collected but not received by the lab
- `received`: accepted by the lab
- `rejected`: rejected (container leak, wrong specimen type, etc.)

## Workflows (Happy Path)

1. Create a patient
2. Seed or create catalog items (tests)
3. Create an order with a list of test codes
4. Optionally create a sample for the order
5. Submit results for each test request
6. Celery task computes interpretation and updates order status

## Where This Shows Up In Code

- Models: `diagnostics_lab/db/models/`
- Routes: `diagnostics_lab/api/routes/`
- Celery roll-up: `diagnostics_lab/tasks.py`
