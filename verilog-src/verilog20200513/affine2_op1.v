// デバイス名: 5CEFA7F31C7N

// 入力の重み付け係数を作る回路
//
// data_in: 4ビットのデータ入力
// inv_in:  0 - 通常入力
//          1 - マイナス(実際にはビット反転)
// data_out: 4ビットのデータ出力
module w_gen(input [3:0]  data_in,
	     input 	  inv_in,
	     output [3:0] data_out);
   assign data_out = inv_in ? ~data_in : data_in;
endmodule

// 4ビット入力 x 16 の加算器
// 結果は 8 ビット
module add4_16(input [3:0]  data0x,
	       input [3:0]  data1x,
	       input [3:0]  data2x,
	       input [3:0]  data3x,
	       input [3:0]  data4x,
	       input [3:0]  data5x,
	       input [3:0]  data6x,
	       input [3:0]  data7x,
	       input [3:0]  data8x,
	       input [3:0]  data9x,
	       input [3:0]  data10x,
	       input [3:0]  data11x,
	       input [3:0]  data12x,
	       input [3:0]  data13x,
	       input [3:0]  data14x,
	       input [3:0]  data15x,
	       output [7:0] result);

   wire [7:0] in0 = {{4{data0x[3] }}, data0x};
   wire [7:0] in1 = {{4{data1x[3] }}, data1x};
   wire [7:0] in2 = {{4{data2x[3] }}, data2x};
   wire [7:0] in3 = {{4{data3x[3] }}, data3x};
   wire [7:0] in4 = {{4{data4x[3] }}, data4x};
   wire [7:0] in5 = {{4{data5x[3] }}, data5x};
   wire [7:0] in6 = {{4{data6x[3] }}, data6x};
   wire [7:0] in7 = {{4{data7x[3] }}, data7x};
   wire [7:0] in8 = {{4{data8x[3] }}, data8x};
   wire [7:0] in9 = {{4{data9x[3] }}, data9x};
   wire [7:0] in10 = {{4{data10x[3] }}, data10x};
   wire [7:0] in11 = {{4{data11x[3] }}, data11x};
   wire [7:0] in12 = {{4{data12x[3] }}, data12x};
   wire [7:0] in13 = {{4{data13x[3] }}, data13x};
   wire [7:0] in14 = {{4{data14x[3] }}, data14x};
   wire [7:0] in15 = {{4{data15x[3] }}, data15x};

   assign result = in0 + in1 + in2 + in3 + in4 + in5 + in6 + in7 +
		   in8 + in9 + in10 + in11 + in12 + in13 + in14 + in15;

endmodule // add4_16

// affine2 1段目の加算器
// dataX_in: X番目のデータ入力
// invX_in:  X番目の重みコントロール
// data_out: データ出力
module affine2_op1(input [3:0]  data0_in,
		   input 	inv0_in,
		   input [3:0] 	data1_in,
		   input 	inv1_in,
		   input [3:0] 	data2_in,
		   input 	inv2_in,
		   input [3:0] 	data3_in,
		   input 	inv3_in,
		   input [3:0] 	data4_in,
		   input 	inv4_in,
		   input [3:0] 	data5_in,
		   input 	inv5_in,
		   input [3:0] 	data6_in,
		   input 	inv6_in,
		   input [3:0] 	data7_in,
		   input 	inv7_in,
		   input [3:0] 	data8_in,
		   input 	inv8_in,
		   input [3:0] 	data9_in,
		   input 	inv9_in,
		   input [3:0] 	data10_in,
		   input 	inv10_in,
		   input [3:0] 	data11_in,
		   input 	inv11_in,
		   input [3:0] 	data12_in,
		   input 	inv12_in,
		   input [3:0] 	data13_in,
		   input 	inv13_in,
		   input [3:0] 	data14_in,
		   input 	inv14_in,
		   input [3:0] 	data15_in,
		   input 	inv15_in,
		   input [3:0] 	data16_in,
		   input 	inv16_in,
		   input [3:0] 	data17_in,
		   input 	inv17_in,
		   input [3:0] 	data18_in,
		   input 	inv18_in,
		   input [3:0] 	data19_in,
		   input 	inv19_in,
		   input [3:0] 	data20_in,
		   input 	inv20_in,
		   input [3:0] 	data21_in,
		   input 	inv21_in,
		   input [3:0] 	data22_in,
		   input 	inv22_in,
		   input [3:0] 	data23_in,
		   input 	inv23_in,
		   input [3:0] 	data24_in,
		   input 	inv24_in,
		   input [3:0] 	data25_in,
		   input 	inv25_in,
		   input [3:0] 	data26_in,
		   input 	inv26_in,
		   input [3:0] 	data27_in,
		   input 	inv27_in,
		   input [3:0] 	data28_in,
		   input 	inv28_in,
		   input [3:0] 	data29_in,
		   input 	inv29_in,
		   input [3:0] 	data30_in,
		   input 	inv30_in,
		   input [3:0] 	data31_in,
		   input 	inv31_in,
		   output [8:0] data_out);

   wire [3:0] 		 tmp_in0;
   wire [3:0] 		 tmp_in1;
   wire [3:0] 		 tmp_in2;
   wire [3:0] 		 tmp_in3;
   wire [3:0] 		 tmp_in4;
   wire [3:0] 		 tmp_in5;
   wire [3:0] 		 tmp_in6;
   wire [3:0] 		 tmp_in7;
   wire [3:0] 		 tmp_in8;
   wire [3:0] 		 tmp_in9;
   wire [3:0] 		 tmp_in10;
   wire [3:0] 		 tmp_in11;
   wire [3:0] 		 tmp_in12;
   wire [3:0] 		 tmp_in13;
   wire [3:0] 		 tmp_in14;
   wire [3:0] 		 tmp_in15;
   wire [3:0] 		 tmp_in16;
   wire [3:0] 		 tmp_in17;
   wire [3:0] 		 tmp_in18;
   wire [3:0] 		 tmp_in19;
   wire [3:0] 		 tmp_in20;
   wire [3:0] 		 tmp_in21;
   wire [3:0] 		 tmp_in22;
   wire [3:0] 		 tmp_in23;
   wire [3:0] 		 tmp_in24;
   wire [3:0] 		 tmp_in25;
   wire [3:0] 		 tmp_in26;
   wire [3:0] 		 tmp_in27;
   wire [3:0] 		 tmp_in28;
   wire [3:0] 		 tmp_in29;
   wire [3:0] 		 tmp_in30;
   wire [3:0] 		 tmp_in31;

   w_gen w0(.data_in(data0_in), .inv_in(inv0_in), .data_out(tmp_in0));
   w_gen w1(.data_in(data1_in), .inv_in(inv1_in), .data_out(tmp_in1));
   w_gen w2(.data_in(data2_in), .inv_in(inv2_in), .data_out(tmp_in2));
   w_gen w3(.data_in(data3_in), .inv_in(inv3_in), .data_out(tmp_in3));
   w_gen w4(.data_in(data4_in), .inv_in(inv4_in), .data_out(tmp_in4));
   w_gen w5(.data_in(data5_in), .inv_in(inv5_in), .data_out(tmp_in5));
   w_gen w6(.data_in(data6_in), .inv_in(inv6_in), .data_out(tmp_in6));
   w_gen w7(.data_in(data7_in), .inv_in(inv7_in), .data_out(tmp_in7));
   w_gen w8(.data_in(data8_in), .inv_in(inv8_in), .data_out(tmp_in8));
   w_gen w9(.data_in(data9_in), .inv_in(inv9_in), .data_out(tmp_in9));
   w_gen w10(.data_in(data10_in), .inv_in(inv10_in), .data_out(tmp_in10));
   w_gen w11(.data_in(data11_in), .inv_in(inv11_in), .data_out(tmp_in11));
   w_gen w12(.data_in(data12_in), .inv_in(inv12_in), .data_out(tmp_in12));
   w_gen w13(.data_in(data13_in), .inv_in(inv13_in), .data_out(tmp_in13));
   w_gen w14(.data_in(data14_in), .inv_in(inv14_in), .data_out(tmp_in14));
   w_gen w15(.data_in(data15_in), .inv_in(inv15_in), .data_out(tmp_in15));
   w_gen w16(.data_in(data16_in), .inv_in(inv16_in), .data_out(tmp_in16));
   w_gen w17(.data_in(data17_in), .inv_in(inv17_in), .data_out(tmp_in17));
   w_gen w18(.data_in(data18_in), .inv_in(inv18_in), .data_out(tmp_in18));
   w_gen w19(.data_in(data19_in), .inv_in(inv19_in), .data_out(tmp_in19));
   w_gen w20(.data_in(data20_in), .inv_in(inv20_in), .data_out(tmp_in20));
   w_gen w21(.data_in(data21_in), .inv_in(inv21_in), .data_out(tmp_in21));
   w_gen w22(.data_in(data22_in), .inv_in(inv22_in), .data_out(tmp_in22));
   w_gen w23(.data_in(data23_in), .inv_in(inv23_in), .data_out(tmp_in23));
   w_gen w24(.data_in(data24_in), .inv_in(inv24_in), .data_out(tmp_in24));
   w_gen w25(.data_in(data25_in), .inv_in(inv25_in), .data_out(tmp_in25));
   w_gen w26(.data_in(data26_in), .inv_in(inv26_in), .data_out(tmp_in26));
   w_gen w27(.data_in(data27_in), .inv_in(inv27_in), .data_out(tmp_in27));
   w_gen w28(.data_in(data28_in), .inv_in(inv28_in), .data_out(tmp_in28));
   w_gen w29(.data_in(data29_in), .inv_in(inv29_in), .data_out(tmp_in29));
   w_gen w30(.data_in(data30_in), .inv_in(inv30_in), .data_out(tmp_in30));
   w_gen w31(.data_in(data31_in), .inv_in(inv31_in), .data_out(tmp_in31));

   wire [8:0] 		 tmp_out1;
   add4_16 add1(.data0x(tmp_in0),
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
		.result(tmp_out1[7:0]));
   // 符号拡張
   assign tmp_out1[8] = tmp_out1[7];

   wire [8:0] 		 tmp_out2;
   add4_16 add2(.data0x(tmp_in16),
		.data1x(tmp_in17),
		.data2x(tmp_in18),
		.data3x(tmp_in19),
		.data4x(tmp_in20),
		.data5x(tmp_in21),
		.data6x(tmp_in22),
		.data7x(tmp_in23),
		.data8x(tmp_in24),
		.data9x(tmp_in25),
		.data10x(tmp_in26),
		.data11x(tmp_in27),
		.data12x(tmp_in28),
		.data13x(tmp_in29),
		.data14x(tmp_in30),
		.data15x(tmp_in31),
		.result(tmp_out2[7:0]));
   // 符号拡張
   assign tmp_out2[8] = tmp_out2[7];

   assign data_out = tmp_out1 + tmp_out2;

endmodule
