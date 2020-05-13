// デバイス名: 5CEFA7F31C7N

// 入力の重み付け係数を作る回路
//
// data_in: 6ビットのデータ入力
// inv_in:  0 - 通常入力
//          1 - マイナス(実際にはビット反転)
// data_out: 6ビットのデータ出力
module w_gen6(input [5:0]  data_in,
	     input 	  inv_in,
	     output [5:0] data_out);
   assign data_out = inv_in ? ~data_in : data_in;
endmodule

// 6ビット入力 x 16 の加算器
// 結果は 10 ビット
module add6_16(input [5:0]  data0x,
	       input [5:0]  data1x,
	       input [5:0]  data2x,
	       input [5:0]  data3x,
	       input [5:0]  data4x,
	       input [5:0]  data5x,
	       input [5:0]  data6x,
	       input [5:0]  data7x,
	       input [5:0]  data8x,
	       input [5:0]  data9x,
	       input [5:0]  data10x,
	       input [5:0]  data11x,
	       input [5:0]  data12x,
	       input [5:0]  data13x,
	       input [5:0]  data14x,
	       input [5:0]  data15x,
	       output [9:0] result);

   wire [9:0] in0 = {{4{data0x[8] }}, data0x};
   wire [9:0] in1 = {{4{data1x[8] }}, data1x};
   wire [9:0] in2 = {{4{data2x[8] }}, data2x};
   wire [9:0] in3 = {{4{data3x[8] }}, data3x};
   wire [9:0] in4 = {{4{data4x[8] }}, data4x};
   wire [9:0] in5 = {{4{data5x[8] }}, data5x};
   wire [9:0] in6 = {{4{data6x[8] }}, data6x};
   wire [9:0] in7 = {{4{data7x[8] }}, data7x};
   wire [9:0] in8 = {{4{data8x[8] }}, data8x};
   wire [9:0] in9 = {{4{data9x[8] }}, data9x};
   wire [9:0] in10 = {{4{data10x[8] }}, data10x};
   wire [9:0] in11 = {{4{data11x[8] }}, data11x};
   wire [9:0] in12 = {{4{data12x[8] }}, data12x};
   wire [9:0] in13 = {{4{data13x[8] }}, data13x};
   wire [9:0] in14 = {{4{data14x[8] }}, data14x};
   wire [9:0] in15 = {{4{data15x[8] }}, data15x};

   assign result = in0 + in1 + in2 + in3 + in4 + in5 + in6 + in7 +
		   in8 + in9 + in10 + in11 + in12 + in13 + in14 + in15;

endmodule // add9_32

// affine3 1段目の加算器
// dataX_in: X番目のデータ入力
// invX_in:  X番目の重みコントロール
// data_out: データ出力
module affine3_op1(input [5:0]   data0_in,
		   input 	 inv0_in,
		   input [5:0] 	 data1_in,
		   input 	 inv1_in,
		   input [5:0] 	 data2_in,
		   input 	 inv2_in,
		   input [5:0] 	 data3_in,
		   input 	 inv3_in,
		   input [5:0] 	 data4_in,
		   input 	 inv4_in,
		   input [5:0] 	 data5_in,
		   input 	 inv5_in,
		   input [5:0] 	 data6_in,
		   input 	 inv6_in,
		   input [5:0] 	 data7_in,
		   input 	 inv7_in,
		   input [5:0] 	 data8_in,
		   input 	 inv8_in,
		   input [5:0] 	 data9_in,
		   input 	 inv9_in,
		   input [5:0] 	 data10_in,
		   input 	 inv10_in,
		   input [5:0] 	 data11_in,
		   input 	 inv11_in,
		   input [5:0] 	 data12_in,
		   input 	 inv12_in,
		   input [5:0] 	 data13_in,
		   input 	 inv13_in,
		   input [5:0] 	 data14_in,
		   input 	 inv14_in,
		   input [5:0] 	 data15_in,
		   input 	 inv15_in,
		   output [9:0] data_out);

   wire [5:0] 		 tmp_in0;
   wire [5:0] 		 tmp_in1;
   wire [5:0] 		 tmp_in2;
   wire [5:0] 		 tmp_in3;
   wire [5:0] 		 tmp_in4;
   wire [5:0] 		 tmp_in5;
   wire [5:0] 		 tmp_in6;
   wire [5:0] 		 tmp_in7;
   wire [5:0] 		 tmp_in8;
   wire [5:0] 		 tmp_in9;
   wire [5:0] 		 tmp_in10;
   wire [5:0] 		 tmp_in11;
   wire [5:0] 		 tmp_in12;
   wire [5:0] 		 tmp_in13;
   wire [5:0] 		 tmp_in14;
   wire [5:0] 		 tmp_in15;
   wire [9:0] 		 tmp_out;

   w_gen6 w0(.data_in(data0_in), .inv_in(inv0_in), .data_out(tmp_in0));
   w_gen6 w1(.data_in(data1_in), .inv_in(inv1_in), .data_out(tmp_in1));
   w_gen6 w2(.data_in(data2_in), .inv_in(inv2_in), .data_out(tmp_in2));
   w_gen6 w3(.data_in(data3_in), .inv_in(inv3_in), .data_out(tmp_in3));
   w_gen6 w4(.data_in(data4_in), .inv_in(inv4_in), .data_out(tmp_in4));
   w_gen6 w5(.data_in(data5_in), .inv_in(inv5_in), .data_out(tmp_in5));
   w_gen6 w6(.data_in(data6_in), .inv_in(inv6_in), .data_out(tmp_in6));
   w_gen6 w7(.data_in(data7_in), .inv_in(inv7_in), .data_out(tmp_in7));
   w_gen6 w8(.data_in(data8_in), .inv_in(inv8_in), .data_out(tmp_in8));
   w_gen6 w9(.data_in(data9_in), .inv_in(inv9_in), .data_out(tmp_in9));
   w_gen6 w10(.data_in(data10_in), .inv_in(inv10_in), .data_out(tmp_in10));
   w_gen6 w11(.data_in(data11_in), .inv_in(inv11_in), .data_out(tmp_in11));
   w_gen6 w12(.data_in(data12_in), .inv_in(inv12_in), .data_out(tmp_in12));
   w_gen6 w13(.data_in(data13_in), .inv_in(inv13_in), .data_out(tmp_in13));
   w_gen6 w14(.data_in(data14_in), .inv_in(inv14_in), .data_out(tmp_in14));
   w_gen6 w15(.data_in(data15_in), .inv_in(inv15_in), .data_out(tmp_in15));

   add6_16 add1(.data0x(tmp_in0),
		.data1x(tmp_in1),
		.data2x(tmp_in2),
		.data3x(tmp_in3),
		.data4x(tmp_in4),
		.data5x(tmp_in5),
		.data6x(tmp_in6),
		.data7x(tmp_in7),
		.data8x(tmp_in8),
		.data9x(tmp_in9),
		.data10x(tmp_in10),
		.data11x(tmp_in11),
		.data12x(tmp_in12),
		.data13x(tmp_in13),
		.data14x(tmp_in14),
		.data15x(tmp_in15),
		.result(tmp_out));

   assign data_out = tmp_out;

endmodule
