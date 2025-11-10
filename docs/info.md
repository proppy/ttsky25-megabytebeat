<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

The main module accept parameters from 4x 4-bit parameters buses and generate PWM audio signal on each output pins according to the following bytebeat formulas:

| Pin     | Formula |
| --------| --------|
| `out0`  | `t*({a,b}&t>>{c,d})` |
| `out1`  | `t|t%{a,b}|t%(1+{c,d})` |
| `out2`  | ` t*(t>>9|t>>13)&16` |
| `out4`  | TBA |
| `out5`  | TBA |
| `out6`  | TBA |
| `out7`  | `t*a&(t>>b)|t*3&(t*c>>d)` |


## How to test

- Connect a speaker to the pin you want to "play".
- Tweak parameters pins using binary rotary switches.

## External hardware

- [Rotaty switches](https://akizukidenshi.com/catalog/g/g102276/) w/ 16 positions.
- Speakers or [TinyTapeout Audio PMOD](https://github.com/MichaelBell/tt-audio-pmod) if you want to hear `out7`.