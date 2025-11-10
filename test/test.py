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
                   dut.tt_um_proppy_megabytebeat0.bytebeat0.bytebeat_the42melody__output_s.value.to_unsigned(),
                   dut.tt_um_proppy_megabytebeat0.bytebeat3.bytebeat_atunetoshare__output_s.value.to_unsigned(),
                   dut.tt_um_proppy_megabytebeat0.bytebeat7.bytebeat_sierpinskiharmony__output_s.value.to_unsigned())
        except ValueError:
            pass  # ignore invalid samples


async def write_wavefile(dut):
    """Write a wavefile corresponding to the outputs."""
    samples = [s async for s in collect_samples(dut, 65536*4*256)]
    df = pd.DataFrame.from_records(samples, columns=['t', 'pcm0', 'pcm3', 'pcm7'], index=['t'])
    df.plot()
    plt.savefig('tb_pcm.png')
    scipy.io.wavfile.write('tb_pcm0.wav', 8000, df['pcm0'][:].to_numpy(dtype=np.uint8))
    scipy.io.wavfile.write('tb_pcm3.wav', 8000, df['pcm3'][:].to_numpy(dtype=np.uint8))    
    scipy.io.wavfile.write('tb_pcm7.wav', 8000, df['pcm7'][:].to_numpy(dtype=np.uint8))


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
