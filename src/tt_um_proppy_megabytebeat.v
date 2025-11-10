// Copyright 2025 Google LLC.
// SPDX-License-Identifier: Apache-2.0

`default_nettype none

module tt_um_proppy_megabytebeat (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);
   wire						rst = !rst_n;
   wire [3:0]					a = ui_in[3:0];
   wire						a_rdy[7:0];
   wire [3:0]					b = ui_in[7:4];
   wire						b_rdy[7:0];
   wire [3:0]					c = uio_in[3:0];
   wire						c_rdy[7:0];
   wire [3:0]					d = uio_in[7:4];
   wire						d_rdy[7:0];
   wire [7:0]					pcm[8];
   wire						pcm_vld[7:0];

   reg [8:0]					clk_8;
   always @(posedge clk) begin
      if (!rst_n) clk_8 <= 0;
      else begin
         clk_8 <= clk_8 + 1;
      end
   end

   bytebeat_the42melody bytebeat0(.clk(clk_8),
				  .reset(rst),
				  .bytebeat_the42melody__a_r(a),
				  .bytebeat_the42melody__a_r_vld(1'b1),
				  .bytebeat_the42melody__b_r(b),
				  .bytebeat_the42melody__b_r_vld(1'b1),
				  .bytebeat_the42melody__c_r(c),
				  .bytebeat_the42melody__c_r_vld(1'b1),
				  .bytebeat_the42melody__d_r(d),
				  .bytebeat_the42melody__d_r_vld(1'b1),
				  .bytebeat_the42melody__output_s_rdy(1'b1),
				  .bytebeat_the42melody__output_s(pcm[0]),
				  .bytebeat_the42melody__output_s_vld(pcm_vld[0]),
				  .bytebeat_the42melody__a_r_rdy(a_rdy[0]),
				  .bytebeat_the42melody__b_r_rdy(b_rdy[0]),
				  .bytebeat_the42melody__c_r_rdy(c_rdy[0]),
				  .bytebeat_the42melody__d_r_rdy(d_rdy[0]));
   bytebeat_sierpinskiharmony bytebeat7(.clk(clk_8),
				  .reset(rst),
				  .bytebeat_sierpinskiharmony__a_r(a),
				  .bytebeat_sierpinskiharmony__a_r_vld(1'b1),
				  .bytebeat_sierpinskiharmony__b_r(b),
				  .bytebeat_sierpinskiharmony__b_r_vld(1'b1),
				  .bytebeat_sierpinskiharmony__c_r(c),
				  .bytebeat_sierpinskiharmony__c_r_vld(1'b1),
				  .bytebeat_sierpinskiharmony__d_r(d),
				  .bytebeat_sierpinskiharmony__d_r_vld(1'b1),
				  .bytebeat_sierpinskiharmony__output_s_rdy(1'b1),
				  .bytebeat_sierpinskiharmony__output_s(pcm[7]),
				  .bytebeat_sierpinskiharmony__output_s_vld(pcm_vld[7]),
				  .bytebeat_sierpinskiharmony__a_r_rdy(a_rdy[7]),
				  .bytebeat_sierpinskiharmony__b_r_rdy(b_rdy[7]),
				  .bytebeat_sierpinskiharmony__c_r_rdy(c_rdy[7]),
				  .bytebeat_sierpinskiharmony__d_r_rdy(d_rdy[7]));
   

   generate
      for (genvar i = 0; i < 8; i++) begin : pwm_audio
	 pwm_audio pwm0(.clk(clk),
			.rst_n(rst_n),
			.sample(pcm[i]),
			.pwm(uo_out[i]));
      end
   endgenerate
   
   assign uio_oe = 8'b00000000;  // set uio as inputs.
   assign uio_out = 8'b00000000; // unused by keep yosys happy.

   generate
      for (genvar i = i; i < 7; i++) begin: unused
	 assign a_rdy[i] = 1'b0;
	 assign b_rdy[i] = 1'b0;
	 assign c_rdy[i] = 1'b0;
	 assign d_rdy[i] = 1'b0;
	 assign pcm_vld[i] = 1'b0;
      end
   endgenerate

   wire _unused = &{ena, 1'b0};

endmodule
