// 2段目の加算器
// dataX_in: X番目のデータ入力
// data_out: データ出力
//
// IP Catalog で生成した PARALLEL_ADDER のモジュール名を add32_2
// としている．
module op2(input [8:0]  data0_in,
	   input [8:0]  data1_in,
	   input [8:0]  data2_in,
	   input [8:0]  data3_in,
	   input [8:0]  data4_in,
	   input [8:0]  data5_in,
	   input [8:0]  data6_in,
	   input [8:0]  data7_in,
	   input [8:0]  data8_in,
	   input [8:0]  data9_in,
	   input [8:0]  data10_in,
	   input [8:0]  data11_in,
	   input [8:0]  data12_in,
	   input [8:0]  data13_in,
	   input [8:0]  data14_in,
	   input [8:0]  data15_in,
	   input [8:0]  data16_in,
	   input [8:0]  data17_in,
	   input [8:0]  data18_in,
	   input [8:0]  data19_in,
	   input [8:0]  data20_in,
	   input [8:0]  data21_in,
	   input [8:0]  data22_in,
	   input [8:0]  data23_in,
	   input [8:0]  data24_in,
	   input [8:0]  data25_in,
	   input [8:0]  data26_in,
	   input [8:0]  data27_in,
	   input [8:0]  data28_in,
	   input [8:0]  data29_in,
	   input [8:0]  data30_in,
	   input [8:0]  data31_in,
	   output [8:0] data_out);

   wire [13:0] 		 tmp_out;

   add32_2 add32(.data0x(data0_in),
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
		 .data16x(data16_in),
		 .data17x(data17_in),
		 .data18x(data18_in),
		 .data19x(data19_in),
		 .data20x(data20_in),
		 .data21x(data21_in),
		 .data22x(data22_in),
		 .data23x(data23_in),
		 .data24x(data24_in),
		 .data25x(data25_in),
		 .data26x(data26_in),
		 .data27x(data27_in),
		 .data28x(data28_in),
		 .data29x(data29_in),
		 .data30x(data30_in),
		 .data31x(data31_in),
		 .result(tmp_out));
   // 出力は3ビットシフトした上で結果を9ビットにトリミングしている．
   // 最終的にはさらに上位2ビットを落としている．
   assign data_out = tmp_out[11:3];

endmodule
