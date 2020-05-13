
`timescale 1ns/1ns

// ダミーの10ビット入力14ビット出力の16入力加算器
module add10_16(input [9:0]  data0x,
		input [9:0]   data1x,
		input [9:0]   data2x,
		input [9:0]   data3x,
		input [9:0]   data4x,
		input [9:0]   data5x,
		input [9:0]   data6x,
		input [9:0]   data7x,
		input [9:0]   data8x,
		input [9:0]   data9x,
		input [9:0]   data10x,
		input [9:0]   data11x,
		input [9:0]   data12x,
		input [9:0]   data13x,
		input [9:0]   data14x,
		input [9:0]   data15x,
		input [9:0]   data16x,
		input [9:0]   data17x,
		input [9:0]   data18x,
		input [9:0]   data19x,
		input [9:0]   data20x,
		input [9:0]   data21x,
		input [9:0]   data22x,
		input [9:0]   data23x,
		input [9:0]   data24x,
		input [9:0]   data25x,
		input [9:0]   data26x,
		input [9:0]   data27x,
		input [9:0]   data28x,
		input [9:0]   data29x,
		input [9:0]   data30x,
		input [9:0]   data31x,
		output [13:0] result);

   wire [13:0] 		     in0 = {{4{data0x[9]}}, data0x};
   wire [13:0] 		     in1 = {{4{data1x[9]}}, data1x};
   wire [13:0] 		     in2 = {{4{data2x[9]}}, data2x};
   wire [13:0] 		     in3 = {{4{data3x[9]}}, data3x};
   wire [13:0] 		     in4 = {{4{data4x[9]}}, data4x};
   wire [13:0] 		     in5 = {{4{data5x[9]}}, data5x};
   wire [13:0] 		     in6 = {{4{data6x[9]}}, data6x};
   wire [13:0] 		     in7 = {{4{data7x[9]}}, data7x};
   wire [13:0] 		     in8 = {{4{data8x[9]}}, data8x};
   wire [13:0] 		     in9 = {{4{data9x[9]}}, data9x};
   wire [13:0] 		     in10 = {{4{data10x[9]}}, data10x};
   wire [13:0] 		     in11 = {{4{data11x[9]}}, data11x};
   wire [13:0] 		     in12 = {{4{data12x[9]}}, data12x};
   wire [13:0] 		     in13 = {{4{data13x[9]}}, data13x};
   wire [13:0] 		     in14 = {{4{data14x[9]}}, data14x};
   wire [13:0] 		     in15 = {{4{data15x[9]}}, data15x};

   assign result = in0 + in1 + in2 + in3 + in4 + in5 + in6 + in7 +
		   in8 + in9 + in10 + in11 + in12 + in13 + in14 + in15;

endmodule // add10_16

module affine3_test;

   // クロック周期(ns)
   integer clock_length = 100;

   // クロックエッジからのマージン
   integer clock_margin = 10;

   reg clock;
   reg reset;
   reg start;

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
	 start = 1'b0;

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

   // 0 番目の入力用メモリブロック
   wire [5:0]   imem00_bank;
   wire 	imem00_rd;
   reg 		imem00_wr;
   reg [5:0]  imem00_in;
   wire [5:0] imem00_out;
   imem imem00(.clock(clock),
               .oaddr(imem00_bank),
               .rd(imem00_rd),
               .wr(imem00_wr),
               .odata(imem00_out));

   // 1 番目の入力用メモリブロック
   wire [5:0] 	imem01_bank;
   wire		imem01_rd;
   reg 		imem01_wr;
   reg [5:0] 	imem01_in;
   wire [5:0] imem01_out;
   imem imem01(.clock(clock),
               .oaddr(imem01_bank),
               .rd(imem01_rd),
               .wr(imem01_wr),
               .odata(imem01_out));

   // 2 番目の入力用メモリブロック
   wire [5:0] 	imem02_bank;
   wire 	imem02_rd;
   reg 		imem02_wr;
   reg [5:0] 	imem02_in;
   wire [5:0] imem02_out;
   imem imem02(.clock(clock),
               .oaddr(imem02_bank),
               .rd(imem02_rd),
               .wr(imem02_wr),
               .odata(imem02_out));

   // 3 番目の入力用メモリブロック
   wire [5:0] 	imem03_bank;
   wire 	imem03_rd;
   reg 		imem03_wr;
   reg [5:0] 	imem03_in;
   wire [5:0] imem03_out;
   imem imem03(.clock(clock),
               .oaddr(imem03_bank),
               .rd(imem03_rd),
               .wr(imem03_wr),
               .odata(imem03_out));

   // 4 番目の入力用メモリブロック
   wire [5:0] 	imem04_bank;
   wire 	imem04_rd;
   reg 		imem04_wr;
   reg [5:0] 	imem04_in;
   wire [5:0] imem04_out;
   imem imem04(.clock(clock),
               .oaddr(imem04_bank),
               .rd(imem04_rd),
               .wr(imem04_wr),
               .odata(imem04_out));

   // 出力値
   wire [13:0] omem00_in;
   wire        omem00_wr;

   // affine3 モジュールのインスタンス
   wire 	busy;
   affine3 affine3(.clock(clock),
		   .reset(reset),
		   .start(start),
		   .busy(busy),
                   .imem00_bank(imem00_bank),
                   .imem00_rd(imem00_rd),
                   .imem00_in(imem00_out),
                   .imem01_bank(imem01_bank),
                   .imem01_rd(imem01_rd),
                   .imem01_in(imem01_out),
                   .imem02_bank(imem02_bank),
                   .imem02_rd(imem02_rd),
                   .imem02_in(imem02_out),
                   .imem03_bank(imem03_bank),
                   .imem03_rd(imem03_rd),
                   .imem03_in(imem03_out),
                   .imem04_bank(imem04_bank),
                   .imem04_rd(imem04_rd),
                   .imem04_in(imem04_out),
                   .omem00_wr(omem00_wr),
                   .omem00_out(omem00_in));

   integer i, j;
   reg [13:0] omem0_ref;

   initial begin

      // リセット
      do_reset;

      start = 1'b0;

      imem00_wr = 1'b0;
      imem01_wr = 1'b0;
      imem02_wr = 1'b0;
      imem03_wr = 1'b0;
      imem04_wr = 1'b0;

      // 入力データの読み込み

      $readmemh("imem00.hex", imem00.memblock);
      $readmemh("imem01.hex", imem01.memblock);
      $readmemh("imem02.hex", imem02.memblock);
      $readmemh("imem03.hex", imem03.memblock);
      $readmemh("imem04.hex", imem04.memblock);

      $readmemh("omem0.hex", omem0_ref);

      // affine モジュールを動作させる．
      start = 1'b1;

      wait_for_next_clock;

      // 完了を待つ．
      @ ( !busy );

      $display("affine2 finished");

      // 期待値と比較
      if ( omem0_ref != omem00_in ) begin
	 $display("Error in omem0");
	 $display(" expected: %d, actual: %dx", omem0_ref, omem00_in);
      end
      else begin
	 $display("omem0 is OK");
      end

      $finish;

   end

endmodule // affine3_test
