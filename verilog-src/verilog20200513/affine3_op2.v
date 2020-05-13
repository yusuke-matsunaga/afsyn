// affine3 2段目の加算器
// dataX_in: X番目のデータ入力
// data_out: データ出力
//
// IP Catalog で生成した PARALLEL_ADDER(16ビット入力 x 32) のモジュール名を
// add16_32 としている．
module affine3_op2(input [9:0]  data0_in,
		   input [9:0] 	 data1_in,
		   input [9:0] 	 data2_in,
		   input [9:0] 	 data3_in,
		   input [9:0] 	 data4_in,
		   input [9:0] 	 data5_in,
		   input [9:0] 	 data6_in,
		   input [9:0] 	 data7_in,
		   input [9:0] 	 data8_in,
		   input [9:0] 	 data9_in,
		   input [9:0] 	 data10_in,
		   input [9:0] 	 data11_in,
		   input [9:0] 	 data12_in,
		   input [9:0] 	 data13_in,
		   input [9:0] 	 data14_in,
		   input [9:0] 	 data15_in,
		   output [13:0] data_out);

   wire [13:0] tmp_out;
   add10_16 add1(.data0x(data0_in),
		 .data1x(data1_in),
		 .data2x(data2_in),
		 .data3x(data3_in),
		 .data4x(data4_in),
		 .data5x(data5_in),
		 .data6x(data6_in),
		 .data7x(data7_in),
		 .data8x(data8_in),
		 .data9x(data9_in),
		 .data10x(data10_in),
		 .data11x(data11_in),
		 .data12x(data12_in),
		 .data13x(data13_in),
		 .data14x(data14_in),
		 .data15x(data15_in),
		 .result(tmp_out));

   assign data_out = tmp_out;

endmodule
