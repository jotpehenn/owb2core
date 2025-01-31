from typing import Counter
from unittest.mock import Mock

import pytest

from control import data
from control.bat import Bat
from control.chargepoint import Chargepoint, ChargepointData, Config, Get, Set
from control.counter_all import CounterAll
from control.pv import Pv


def hierarchy_standard() -> CounterAll:
    # counter0
    #        |
    #        - cp3
    #        - cp4
    #        - cp5
    #        - inverter1
    #        - bat2
    # counter6
    c = CounterAll()
    c.data.get.hierarchy = [{"id": 0, "type": "counter",
                             "children": [
                                 {"id": 3, "type": "cp", "children": []},
                                 {"id": 4, "type": "cp", "children": []},
                                 {"id": 5, "type": "cp", "children": []},
                                 {"id": 1, "type": "inverter", "children": []},
                                 {"id": 2, "type": "bat", "children": []}]},
                            {"id": 6, "type": "counter", "children": []}]
    return c


def hierarchy_hybrid() -> CounterAll:
    # counter0
    #        |
    #        - cp3
    #        - cp4
    #        - cp5
    #        - inverter1
    #                  |
    #                  - bat2
    # counter6
    c = CounterAll()
    c.data.get.hierarchy = [{"id": 0, "type": "counter",
                             "children": [
                                 {"id": 3, "type": "cp", "children": []},
                                 {"id": 4, "type": "cp", "children": []},
                                 {"id": 5, "type": "cp", "children": []},
                                 {"id": 1, "type": "inverter",
                                  "children": [
                                      {"id": 2, "type": "bat", "children": []}]}]},
                            {"id": 6, "type": "counter", "children": []}]
    return c


def hierarchy_nested() -> CounterAll:
    # counter0
    #        |
    #        - cp3
    #        - counter6
    #                  |
    #                   - cp4
    #                   - cp5
    #        - inverter1
    #        - bat2
    c = CounterAll()
    c.data.get.hierarchy = [{"id": 0, "type": "counter",
                             "children": [
                                 {"id": 3, "type": "cp", "children": []},
                                 {"id": 6, "type": "counter",
                                  "children": [
                                      {"id": 4, "type": "cp", "children": []},
                                      {"id": 5, "type": "cp", "children": []}]},
                                 {"id": 1, "type": "inverter", "children": []},
                                 {"id": 2, "type": "bat", "children": []}]}]
    return c


@pytest.fixture()
def data_() -> None:
    data.data_init(Mock())
    data.data.cp_data = {
        "cp3": Mock(spec=Chargepoint, data=Mock(spec=ChargepointData,
                                                config=Mock(spec=Config, phase_1=1),
                                                get=Mock(spec=Get, currents=[30, 0, 0], power=6900),
                                                set=Mock(spec=Set))),
        "cp4": Mock(spec=Chargepoint, data=Mock(spec=ChargepointData,
                                                config=Mock(spec=Config, phase_1=2),
                                                get=Mock(spec=Get, currents=[0, 15, 15], power=6900),
                                                set=Mock(spec=Set))),
        "cp5": Mock(spec=Chargepoint, data=Mock(spec=ChargepointData,
                                                config=Mock(spec=Config, phase_1=3),
                                                get=Mock(spec=Get, currents=[10]*3, power=6900),
                                                set=Mock(spec=Set)))}
    data.data.bat_data.update({"bat2": Mock(spec=Bat, data={"get": {"power": -5000}})})
    data.data.pv_data.update({"pv1": Mock(spec=Pv, data={"get": {"power": -10000}})})
    data.data.counter_data.update({
        "counter0": Mock(spec=Counter, data={"get": {"currents": [40]*3, "power": 6200}}),
        "counter6": Mock(spec=Counter, data={"get": {"currents": [25, 10, 25], "power": 13800}})})
