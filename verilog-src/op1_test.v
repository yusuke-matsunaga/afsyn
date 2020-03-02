
`timescale 1ns/1ns

module add16(input [7:0]   data0x,
	     input [7:0]   data1x,
	     input [7:0]   data2x,
	     input [7:0]   data3x,
	     input [7:0]   data4x,
	     input [7:0]   data5x,
	     input [7:0]   data6x,
	     input [7:0]   data7x,
	     input [7:0]   data8x,
	     input [7:0]   data9x,
	     input [7:0]   data10x,
	     input [7:0]   data11x,
	     input [7:0]   data12x,
	     input [7:0]   data13x,
	     input [7:0]   data14x,
	     input [7:0]   data15x,
	     output [11:0] result);

   wire [8:0] tmp1_1 = data0x + data1x;
   wire [8:0] tmp1_2 = data2x + data3x;
   wire [8:0] tmp1_3 = data4x + data5x;
   wire [8:0] tmp1_4 = data6x + data7x;
   wire [8:0] tmp1_5 = data8x + data9x;
   wire [8:0] tmp1_6 = data10x + data11x;
   wire [8:0] tmp1_7 = data12x + data13x;
   wire [8:0] tmp1_8 = data14x + data15x;

   wire [9:0] tmp2_1 = tmp1_1 + tmp1_2;
   wire [9:0] tmp2_2 = tmp1_3 + tmp1_4;
   wire [9:0] tmp2_3 = tmp1_5 + tmp1_6;
   wire [9:0] tmp2_4 = tmp1_7 + tmp1_8;

   wire [10:0] tmp3_1 = tmp2_1 + tmp2_2;
   wire [10:0] tmp3_2 = tmp2_3 + tmp2_4;

   assign result = tmp3_1 + tmp3_2;
endmodule // add16

module op1_test;

   // クロック周期(ns)
   integer clock_length = 100;

   // クロックエッジからのマージン
   integer clock_margin = 10;

   reg clock;
   reg reset;

   // 次の立ち上がりクロックを待つ
   task wait_for_next_clock;
      begin
	 @ ( posedge clock );

	 // さらにちょっと待つ
	 #clock_margin;
      end
   endtask // wait_for_next_clock

   // リセットを行う．
   task do_reset;
      begin
	 reset = 1'b1;

	 // クロックに同期する．
	 wait_for_next_clock;

	 // リセットする．
	 reset = 1'b0;

	 // ちょっと待つ
	 #clock_margin;

	 // リセットを元に戻す．
	 reset = 1'b1;
      end
   endtask // do_reset

   // クロックの生成
   always begin
      clock = 1'b1;

      #(clock_length / 2);

      clock = 1'b0;

      #(clock_length / 2);
   end

   // op1 モジュールのインスタンス
   reg [7:0] data0_in;
   reg       ctrl0_in;
   reg [7:0] data1_in;
   reg       ctrl1_in;
   reg [7:0] data2_in;
   reg       ctrl2_in;
   reg [7:0] data3_in;
   reg       ctrl3_in;
   reg [7:0] data4_in;
   reg       ctrl4_in;
   reg [7:0] data5_in;
   reg       ctrl5_in;
   reg [7:0] data6_in;
   reg       ctrl6_in;
   reg [7:0] data7_in;
   reg       ctrl7_in;
   reg [7:0] data8_in;
   reg       ctrl8_in;
   reg [7:0] data9_in;
   reg       ctrl9_in;
   reg [7:0] data10_in;
   reg       ctrl10_in;
   reg [7:0] data11_in;
   reg       ctrl11_in;
   reg [7:0] data12_in;
   reg       ctrl12_in;
   reg [7:0] data13_in;
   reg       ctrl13_in;
   reg [7:0] data14_in;
   reg       ctrl14_in;
   reg [7:0] data15_in;
   reg       ctrl15_in;
   wire [11:0] result;
   op1 op1(.clock(clock), .reset(reset),
	   .data0_in(data0_in), .ctrl0_in(ctrl0_in),
	   .data1_in(data1_in), .ctrl1_in(ctrl1_in),
	   .data2_in(data2_in), .ctrl2_in(ctrl2_in),
	   .data3_in(data3_in), .ctrl3_in(ctrl3_in),
	   .data4_in(data4_in), .ctrl4_in(ctrl4_in),
	   .data5_in(data5_in), .ctrl5_in(ctrl5_in),
	   .data6_in(data6_in), .ctrl6_in(ctrl6_in),
	   .data7_in(data7_in), .ctrl7_in(ctrl7_in),
	   .data8_in(data8_in), .ctrl8_in(ctrl8_in),
	   .data9_in(data9_in), .ctrl9_in(ctrl9_in),
	   .data10_in(data10_in), .ctrl10_in(ctrl10_in),
	   .data11_in(data11_in), .ctrl11_in(ctrl11_in),
	   .data12_in(data12_in), .ctrl12_in(ctrl12_in),
	   .data13_in(data13_in), .ctrl13_in(ctrl13_in),
	   .data14_in(data14_in), .ctrl14_in(ctrl14_in),
	   .data15_in(data15_in), .ctrl15_in(ctrl15_in),
	   .data_out(result));

   initial begin

      // リセット
      do_reset;

      $display("result = %16d", result);

      data0_in = 8'd0;
      data1_in = 8'd1;
      data2_in = 8'd2;
      data3_in = 8'd3;
      data4_in = 8'd4;
      data5_in = 8'd5;
      data6_in = 8'd6;
      data7_in = 8'd7;
      data8_in = 8'd8;
      data9_in = 8'd9;
      data10_in = 8'd10;
      data11_in = 8'd11;
      data12_in = 8'd12;
      data13_in = 8'd13;
      data14_in = 8'd14;
      data15_in = 8'd15;

      ctrl0_in = 1'b0;
      ctrl1_in = 1'b0;
      ctrl2_in = 1'b0;
      ctrl3_in = 1'b0;
      ctrl4_in = 1'b0;
      ctrl5_in = 1'b0;
      ctrl6_in = 1'b0;
      ctrl7_in = 1'b0;
      ctrl8_in = 1'b0;
      ctrl9_in = 1'b0;
      ctrl10_in = 1'b0;
      ctrl11_in = 1'b0;
      ctrl12_in = 1'b0;
      ctrl13_in = 1'b0;
      ctrl14_in = 1'b0;
      ctrl15_in = 1'b0;

      wait_for_next_clock;

      $display("result = %12d", result);

      $finish;
   end

endmodule
