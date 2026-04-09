#!/usr/bin/env python3

"""
Minimal Modbus RTU serial slave for bench testing.

Configuration is environment-driven so the script can run in different
machines without code edits.
"""

import asyncio
import logging
import os
from typing import Tuple

from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.framer import FramerType
from pymodbus.server import StartAsyncSerialServer


logging.basicConfig(level=logging.ERROR)


def _env_str(name: str, default: str) -> str:
    return os.getenv(name, default).strip() or default


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name, str(default)).strip()
    try:
        return int(raw)
    except ValueError:
        return default


def _env_float(name: str, default: float) -> float:
    raw = os.getenv(name, str(default)).strip()
    try:
        return float(raw)
    except ValueError:
        return default


def load_runtime() -> Tuple[str, int, float, int, float]:
    """Load runtime options from environment."""
    serial_port = _env_str("MODBUS_SERIAL_PORT", "COM6")
    baudrate = _env_int("MODBUS_SERIAL_BAUDRATE", 115200)
    timeout = _env_float("MODBUS_SERIAL_TIMEOUT", 1.0)
    slave_id = _env_int("MODBUS_SLAVE_ID", 1)
    print_interval = _env_float("MODBUS_PRINT_INTERVAL", 0.5)
    return serial_port, baudrate, timeout, slave_id, print_interval


def build_context(slave_id: int) -> ModbusServerContext:
    """Build test datastore for a single slave id."""
    store = {
        slave_id: ModbusSlaveContext(
            di=ModbusSequentialDataBlock(0, [0] * 100),
            co=ModbusSequentialDataBlock(0, [0] * 100),
            hr=ModbusSequentialDataBlock(0, [0] * 100),
            ir=ModbusSequentialDataBlock(0, [0] * 100),
        )
    }
    return ModbusServerContext(slaves=store, single=False)


def build_identity() -> ModbusDeviceIdentification:
    """Build Modbus server identity fields."""
    identity = ModbusDeviceIdentification()
    identity.VendorName = "IndustrialEdgeModbus"
    identity.ProductCode = "IEM"
    identity.VendorUrl = "https://example.com/industrial-edge-modbus"
    identity.ProductName = "RTU Serial Test Server"
    identity.ModelName = "pymodbus serial slave"
    return identity


async def print_holding_registers(
    context: ModbusServerContext,
    slave_id: int,
    interval: float,
) -> None:
    """Print first five holding registers repeatedly."""
    spinner = ["|", "/", "-", "\\"]
    idx = 0
    while True:
        values = context[slave_id].getValues(3, 0, count=5)
        payload = " ".join(str(value) for value in values)
        print(f"HR[0:5] {payload}  {spinner[idx]}", end="\r")
        idx = (idx + 1) % len(spinner)
        await asyncio.sleep(interval)


async def run_server() -> None:
    serial_port, baudrate, timeout, slave_id, print_interval = load_runtime()
    context = build_context(slave_id=slave_id)
    identity = build_identity()

    print(
        "Starting Modbus RTU serial server "
        f"(port={serial_port}, baudrate={baudrate}, timeout={timeout}, slave_id={slave_id})"
    )
    asyncio.create_task(
        print_holding_registers(context, slave_id=slave_id, interval=print_interval)
    )
    await StartAsyncSerialServer(
        context,
        identity=identity,
        framer=FramerType.RTU,
        port=serial_port,
        baudrate=baudrate,
        timeout=timeout,
    )


if __name__ == "__main__":
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("\nServer stopped")
