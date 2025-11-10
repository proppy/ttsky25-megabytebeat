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


async def collect_samples(dut, count):
    for i in range(count):
        await RisingEdge(dut.clk) # wait for first clock edge
        try:
            yield (i,
                   dut.uo_out[0].value ? 255 : 0,
                   dut.uo_out[7].value ? 255 : 0)
        except ValueError:
            pass  # ignore invalid samples


async def write_wavefile(dut):
    """Write a wavefile corresponding to the outputs."""
    samples = [s async for s in collect_samples(dut, 65536*4)]
    df = pd.DataFrame.from_records(samples, columns=['t', 'out0', 'out7'], index=['t'])
    df.plot()
    plt.savefig('tb.png')
    scipy.io.wavfile.write('tb_out0.wav', 8000, df['out0'][:].to_numpy(dtype=np.uint8))
    scipy.io.wavfile.write('tb_out7.wav', 8000, df['out7'][:].to_numpy(dtype=np.uint8))    


@cocotb.test()
async def test_bytebeat(dut):
    dut._log.info("Start")

    cocotb.start_soon(write_wavefile(dut))  # collect samples "in the background"

    # Set the clock to 8000hz
    clock = Clock(dut.clk, (1.0/FREQ), unit="sec")
    cocotb.start_soon(clock.start())

    dut.ena.value = 1 # enable project
    dut.rst_n.value = 0 # low to reset
    dut.ui_in.value = 0x75  # a=5 b=7
    dut.uio_in.value = 0xa3 # c=3 d=10
    await ClockCycles(dut.clk, 1)
    dut.rst_n.value = 1 # take out of reset
    await ClockCycles(dut.clk, 65536)
    dut.rst_n.value = 0 # low to reset
    dut.ui_in.value = 0x63  # a=3 b=6
    dut.uio_in.value = 0x92 # c=2 d=9
    await ClockCycles(dut.clk, 1)
    dut.rst_n.value = 1 # take out of reset
    await ClockCycles(dut.clk, 65536)
    dut.rst_n.value = 0 # low to reset
    dut.ui_in.value = 0x57  # a=7 b=5
    dut.uio_in.value = 0x3a # c=10 d=3
    await ClockCycles(dut.clk, 1)
    dut.rst_n.value = 1 # take out of reset
    await ClockCycles(dut.clk, 65536)
    dut.rst_n.value = 0 # low to reset
    dut.ui_in.value = 0x36  # a=6 b=3
    dut.uio_in.value = 0x29 # c=9 d=2
    await ClockCycles(dut.clk, 1)
    dut.rst_n.value = 1 # take out of reset
    await ClockCycles(dut.clk, 65536)
