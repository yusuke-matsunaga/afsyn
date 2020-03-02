// 2段目の加算器
// clock:    クロック
// reset:    リセット
// dataX_in: X番目のデータ入力
// data_out: データ出力
//
// IP Catalog で生成した PARALLEL_ADDER のモジュール名を add16_2
// としている．
module op2(input         clock,
	   input 	 reset,
	   input [11:0]  data0_in,
	   input [11:0]  data1_in,
	   input [11:0]  data2_in,
	   input [11:0]  data3_in,
	   input [11:0]  data4_in,
	   input [11:0]  data5_in,
	   input [11:0]  data6_in,
	   input [11:0]  data7_in,
	   input [11:0]  data8_in,
	   input [11:0]  data9_in,
	   input [11:0]  data10_in,
	   input [11:0]  data11_in,
	   input [11:0]  data12_in,
	   input [11:0]  data13_in,
	   input [11:0]  data14_in,
	   input [11:0]  data15_in,
	   output [15:0] data_out);
   wire [15:0] 		 tmp_out;

   add16_2 add16(.data0x(data0_in),
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

   reg [15:0] 		 tmp_reg;

   always @ ( posedge clock or negedge reset ) begin
      if ( !reset ) begin
	 tmp_reg <= 16'b0;
      end
      else begin
	 tmp_reg <= tmp_out;
      end
   end

   assign data_out = tmp_reg;

endmodule
