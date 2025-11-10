# Copyright 2025 Google LLC.
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge

import numpy as np
import scipy.io.wavfile
import pandas as pd
import matplotlib.pyplot as plt


FREQ = 8000 * 256

@cocotb.test()
async def test_bytebeat(dut):
    dut._log.info("Start")

    cocotb.start_soon(write_wavefile(dut))  # collect samples "in the background"

    # Set the clock to ~2048000hz (8000 * 256)
    clock = Clock(dut.clk, 488280, unit="ps")
    cocotb.start_soon(clock.start())

    dut.ena.value = 1 # enable project
    dut.rst_n.value = 0 # low to reset
    dut.ui_in.value = 0x75  # a=5 b=7
    dut.uio_in.value = 0xa3 # c=3 d=10
    await ClockCycles(dut.clk, 1)
    dut.rst_n.value = 1 # take out of reset
    await ClockCycles(dut.clk, 65536*256)
