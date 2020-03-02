// デバイス名: 5CEFA7F31C7N

// 入力の重み付け係数を作る回路
//
// data_in: ８ビットのデータ入力
// ctrl_in: 0 - 通常入力
//          1 - マイナス(実際にはビット反転)
// data_out: 8ビットのデータ出力
module w_gen(input [7:0]  data_in,
	     input 	  ctrl_in,
	     output [7:0] data_out);
   assign data_out = ctrl_in ? ~data_in : data_in;
endmodule

// 1段目の加算器
// clock:    クロック
// reset:    リセット
// dataX_in: X番目のデータ入力
// ctrlX_in: X番目の重みコントロール
// data_out: データ出力
//
// データは内部でラッチされる．
module op1(input         clock,
	   input 	 reset,
	   input [7:0] 	 data0_in,
	   input       	 ctrl0_in,
	   input [7:0] 	 data1_in,
	   input       	 ctrl1_in,
	   input [7:0] 	 data2_in,
	   input       	 ctrl2_in,
	   input [7:0] 	 data3_in,
	   input       	 ctrl3_in,
	   input [7:0] 	 data4_in,
	   input       	 ctrl4_in,
	   input [7:0] 	 data5_in,
	   input       	 ctrl5_in,
	   input [7:0] 	 data6_in,
	   input       	 ctrl6_in,
	   input [7:0] 	 data7_in,
	   input       	 ctrl7_in,
	   input [7:0] 	 data8_in,
	   input       	 ctrl8_in,
	   input [7:0] 	 data9_in,
	   input       	 ctrl9_in,
	   input [7:0] 	 data10_in,
	   input       	 ctrl10_in,
	   input [7:0] 	 data11_in,
	   input       	 ctrl11_in,
	   input [7:0] 	 data12_in,
	   input       	 ctrl12_in,
	   input [7:0] 	 data13_in,
	   input       	 ctrl13_in,
	   input [7:0] 	 data14_in,
	   input       	 ctrl14_in,
	   input [7:0] 	 data15_in,
	   input       	 ctrl15_in,
	   output [11:0] data_out);

   wire [7:0] 		 tmp_in0;
   wire [7:0] 		 tmp_in1;
   wire [7:0] 		 tmp_in2;
   wire [7:0] 		 tmp_in3;
   wire [7:0] 		 tmp_in4;
   wire [7:0] 		 tmp_in5;
   wire [7:0] 		 tmp_in6;
   wire [7:0] 		 tmp_in7;
   wire [7:0] 		 tmp_in8;
   wire [7:0] 		 tmp_in9;
   wire [7:0] 		 tmp_in10;
   wire [7:0] 		 tmp_in11;
   wire [7:0] 		 tmp_in12;
   wire [7:0] 		 tmp_in13;
   wire [7:0] 		 tmp_in14;
   wire [7:0] 		 tmp_in15;
   wire [11:0] 		 tmp_out;

   w_gen w0(.data_in(data0_in), .ctrl_in(ctrl0_in), .data_out(tmp_in0));
   w_gen w1(.data_in(data1_in), .ctrl_in(ctrl1_in), .data_out(tmp_in1));
   w_gen w2(.data_in(data2_in), .ctrl_in(ctrl2_in), .data_out(tmp_in2));
   w_gen w3(.data_in(data3_in), .ctrl_in(ctrl3_in), .data_out(tmp_in3));
   w_gen w4(.data_in(data4_in), .ctrl_in(ctrl4_in), .data_out(tmp_in4));
   w_gen w5(.data_in(data5_in), .ctrl_in(ctrl5_in), .data_out(tmp_in5));
   w_gen w6(.data_in(data6_in), .ctrl_in(ctrl6_in), .data_out(tmp_in6));
   w_gen w7(.data_in(data7_in), .ctrl_in(ctrl7_in), .data_out(tmp_in7));
   w_gen w8(.data_in(data8_in), .ctrl_in(ctrl8_in), .data_out(tmp_in8));
   w_gen w9(.data_in(data9_in), .ctrl_in(ctrl9_in), .data_out(tmp_in9));
   w_gen w10(.data_in(data10_in), .ctrl_in(ctrl10_in), .data_out(tmp_in10));
   w_gen w11(.data_in(data11_in), .ctrl_in(ctrl11_in), .data_out(tmp_in11));
   w_gen w12(.data_in(data12_in), .ctrl_in(ctrl12_in), .data_out(tmp_in12));
   w_gen w13(.data_in(data13_in), .ctrl_in(ctrl13_in), .data_out(tmp_in13));
   w_gen w14(.data_in(data14_in), .ctrl_in(ctrl14_in), .data_out(tmp_in14));
   w_gen w15(.data_in(data15_in), .ctrl_in(ctrl15_in), .data_out(tmp_in15));

   add16 add16(.data0x(tmp_in0),
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

   reg [11:0] 		 tmp_reg;

   always @ ( posedge clock or negedge reset ) begin
      if ( !reset ) begin
	 tmp_reg <= 12'b0;
      end
      else begin
	 tmp_reg <= tmp_out;
      end
   end

   assign data_out = tmp_reg;

endmodule
