import os
import sys

from conformance.uesp_runtime import ProviderSimulator, Runtime, SimulatedCrash

runtime_path, provider_path = sys.argv[1:3]
provider = ProviderSimulator(provider_path)
runtime = Runtime(runtime_path, provider)
execution = "tenant.example/process-crash-001"
epoch = runtime.acquire_owner(execution)
try:
    runtime.dispatch(
        execution,
        "write-order",
        "attempt-process-crash",
        "tenant.example:process-crash-001:write-order",
        {"order_id": "order-process-crash", "version": 1},
        "E1",
        epoch,
        crash_after_effect=True,
    )
except SimulatedCrash:
    # Abrupt process termination: no finally block or graceful shutdown.
    os._exit(73)

raise SystemExit("fault injection failed: runtime did not crash")
