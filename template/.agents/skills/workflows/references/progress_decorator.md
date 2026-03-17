# Progress Tracking Decorator

Simplified decorator for tracking workflow step progress with automatic event recording.

## Overview

The `record_event_progress` decorator provides a cleaner alternative to the context manager approach for tracking progress in workflows. It automatically records start/complete/failed events for decorated functions.

## Implementation

```python
import functools
import mistralai_workflows as workflows

def record_event_progress(description: str):
    """Decorator that wraps a function with progress event recording.

    Args:
        description: Human-readable description shown in the workflow trace.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with workflows.record_event_progress(description):
                return func(*args, **kwargs)
        return wrapper
    return decorator
```

### Async Support

For async functions, use an async-aware version:

```python
import asyncio
import functools
import mistralai_workflows as workflows

def record_event_progress(description: str):
    """Decorator for both sync and async functions."""
    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                with workflows.record_event_progress(description):
                    return await func(*args, **kwargs)
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                with workflows.record_event_progress(description):
                    return func(*args, **kwargs)
            return sync_wrapper
    return decorator
```

## Usage

### Basic Usage

```python
@record_event_progress("Fetching user data")
async def fetch_user_data(user_id: str) -> UserData:
    return await user_service.get(user_id)

@record_event_progress("Processing payment")
async def process_payment(order: Order) -> PaymentResult:
    return await payment_gateway.charge(order.amount, order.payment_method)

@record_event_progress("Sending confirmation email")
async def send_confirmation(user: User, order: Order) -> None:
    await email_service.send_order_confirmation(user.email, order)
```

### In Workflow Classes

```python
@workflows.workflow.define(workflow_name="order-processing")
class OrderProcessingWorkflow:

    @workflows.workflow.entrypoint
    async def run(self, params: OrderParams) -> OrderResult:
        order = await self.validate_order(params)
        payment = await self.process_payment(order)
        await self.send_notifications(order, payment)
        return OrderResult(order_id=order.id, status="completed")

    @record_event_progress("Validating order details")
    async def validate_order(self, params: OrderParams) -> Order:
        return Order(...)

    @record_event_progress("Processing payment")
    async def process_payment(self, order: Order) -> PaymentResult:
        return PaymentResult(...)

    @record_event_progress("Sending notifications")
    async def send_notifications(self, order: Order, payment: PaymentResult) -> None:
        pass
```

## Comparison with Context Manager

### Context Manager Approach

```python
async def fetch_data(self, params):
    with workflows.record_event_progress("Fetching data"):
        result = await api.fetch(params.id)
        processed = process(result)
        return processed
```

### Decorator Approach

```python
@record_event_progress("Fetching data")
async def fetch_data(self, params):
    result = await api.fetch(params.id)
    processed = process(result)
    return processed
```

### When to Use Each

| Approach | Best For |
|----------|----------|
| **Decorator** | Entire function should be tracked as one unit |
| **Context Manager** | Track a specific section within a larger function |

## Trace Output

When viewing workflow traces, decorated functions appear as distinct events:

```
[00:00.000] Started: Fetching user data
[00:00.150] Completed: Fetching user data
[00:00.151] Started: Processing payment
[00:00.523] Completed: Processing payment
[00:00.524] Started: Sending confirmation email
[00:00.612] Completed: Sending confirmation email
```

Failed events include error information:

```
[00:00.151] Started: Processing payment
[00:00.523] Failed: Processing payment
            Error: PaymentDeclined: Insufficient funds
```

## Best Practices

1. **Use descriptive names**: "Fetching customer data" not "Step 1"
2. **Keep descriptions concise**: They appear in UI traces
3. **Use present participle**: "Fetching...", "Processing...", "Sending..."
4. **Don't nest decorators**: Use context managers for sub-sections if needed
5. **Apply to meaningful units**: Don't track trivial operations
