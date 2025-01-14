#!/usr/bin/env python3
from typing import Any, Callable
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.simcount import SimCounter
from modules.common.store import get_counter_value_store
from modules.devices.kostal_plenticore.config import KostalPlenticoreCounterSetup


class KostalPlenticoreCounter:
    def __init__(self,
                 device_id: int,
                 component_config: KostalPlenticoreCounterSetup) -> None:
        self.component_config = component_config
        self.store = get_counter_value_store(self.component_config.id)
        self.sim_counter = SimCounter(device_id, self.component_config.id, prefix="bezug")
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def get_values(self, reader: Callable[[int, ModbusDataType], Any]) -> CounterState:
        power_factor = reader(150, ModbusDataType.FLOAT_32)
        currents = [reader(register, ModbusDataType.FLOAT_32) for register in [222, 232, 242]]
        voltages = [reader(register, ModbusDataType.FLOAT_32) for register in [230, 240, 250]]
        powers = [reader(register, ModbusDataType.FLOAT_32) for register in [224, 234, 244]]
        power = reader(252, ModbusDataType.FLOAT_32)
        frequency = reader(220, ModbusDataType.FLOAT_32)

        return CounterState(
            powers=powers,
            currents=currents,
            voltages=voltages,
            power=power,
            power_factors=[power_factor]*3,
            frequency=frequency
        )

    def update_imported_exported(self, state: CounterState) -> CounterState:
        state.imported, state.exported = self.sim_counter.sim_count(state.power)
        return state

    def update(self, reader: Callable[[int, ModbusDataType], Any]):
        self.store.set(self.update_imported_exported(self.get_values(reader)))


component_descriptor = ComponentDescriptor(configuration_factory=KostalPlenticoreCounterSetup)
