
`timescale 1ns/1ns

// ダミーの9ビット入力13ビット出力の32入力加算器
module add9_32(input [8:0]  data0x,
	       input [8:0]  data1x,
	       input [8:0]  data2x,
	       input [8:0]  data3x,
	       input [8:0]  data4x,
	       input [8:0]  data5x,
	       input [8:0]  data6x,
	       input [8:0]  data7x,
	       input [8:0]  data8x,
	       input [8:0]  data9x,
	       input [8:0]  data10x,
	       input [8:0]  data11x,
	       input [8:0]  data12x,
	       input [8:0]  data13x,
	       input [8:0]  data14x,
	       input [8:0]  data15x,
	       input [8:0]  data16x,
	       input [8:0]  data17x,
	       input [8:0]  data18x,
	       input [8:0]  data19x,
	       input [8:0]  data20x,
	       input [8:0]  data21x,
	       input [8:0]  data22x,
	       input [8:0]  data23x,
	       input [8:0]  data24x,
	       input [8:0]  data25x,
	       input [8:0]  data26x,
	       input [8:0]  data27x,
	       input [8:0]  data28x,
	       input [8:0]  data29x,
	       input [8:0]  data30x,
	       input [8:0]  data31x,
	       output [13:0] result);

   wire [13:0] 		     in0 = {{5{data0x[8]}}, data0x};
   wire [13:0] 		     in1 = {{5{data1x[8]}}, data1x};
   wire [13:0] 		     in2 = {{5{data2x[8]}}, data2x};
   wire [13:0] 		     in3 = {{5{data3x[8]}}, data3x};
   wire [13:0] 		     in4 = {{5{data4x[8]}}, data4x};
   wire [13:0] 		     in5 = {{5{data5x[8]}}, data5x};
   wire [13:0] 		     in6 = {{5{data6x[8]}}, data6x};
   wire [13:0] 		     in7 = {{5{data7x[8]}}, data7x};
   wire [13:0] 		     in8 = {{5{data8x[8]}}, data8x};
   wire [13:0] 		     in9 = {{5{data9x[8]}}, data9x};
   wire [13:0] 		     in10 = {{5{data10x[8]}}, data10x};
   wire [13:0] 		     in11 = {{5{data11x[8]}}, data11x};
   wire [13:0] 		     in12 = {{5{data12x[8]}}, data12x};
   wire [13:0] 		     in13 = {{5{data13x[8]}}, data13x};
   wire [13:0] 		     in14 = {{5{data14x[8]}}, data14x};
   wire [13:0] 		     in15 = {{5{data15x[8]}}, data15x};
   wire [13:0] 		     in16 = {{5{data16x[8]}}, data16x};
   wire [13:0] 		     in17 = {{5{data17x[8]}}, data17x};
   wire [13:0] 		     in18 = {{5{data18x[8]}}, data18x};
   wire [13:0] 		     in19 = {{5{data19x[8]}}, data19x};
   wire [13:0] 		     in20 = {{5{data20x[8]}}, data20x};
   wire [13:0] 		     in21 = {{5{data21x[8]}}, data21x};
   wire [13:0] 		     in22 = {{5{data22x[8]}}, data22x};
   wire [13:0] 		     in23 = {{5{data23x[8]}}, data23x};
   wire [13:0] 		     in24 = {{5{data24x[8]}}, data24x};
   wire [13:0] 		     in25 = {{5{data25x[8]}}, data25x};
   wire [13:0] 		     in26 = {{5{data26x[8]}}, data26x};
   wire [13:0] 		     in27 = {{5{data27x[8]}}, data27x};
   wire [13:0] 		     in28 = {{5{data28x[8]}}, data28x};
   wire [13:0] 		     in29 = {{5{data29x[8]}}, data29x};
   wire [13:0] 		     in30 = {{5{data30x[8]}}, data30x};
   wire [13:0] 		     in31 = {{5{data31x[8]}}, data31x};

   assign result = in0 + in1 + in2 + in3 + in4 + in5 + in6 + in7 +
		   in8 + in9 + in10 + in11 + in12 + in13 + in14 + in15 +
		   in16 + in17 + in18 + in19 + in20 + in21 + in22 + in23 +
		   in24 + in25 + in26 + in27 + in28 + in29 + in30 + in31;

endmodule // add9_32

module affine2_test;

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
   wire [1:0]   imem00_bank;
   wire 	imem00_rd;
   reg 		imem00_wr;
   reg [127:0]  imem00_in;
   wire [127:0] imem00_out;
   imem imem00(.clock(clock),
               .oaddr(imem00_bank),
               .rd(imem00_rd),
               .wr(imem00_wr),
               .odata(imem00_out));

   // 1 番目の入力用メモリブロック
   wire [1:0] 	imem01_bank;
   wire		imem01_rd;
   reg 		imem01_wr;
   reg [127:0] 	imem01_in;
   wire [127:0] imem01_out;
   imem imem01(.clock(clock),
               .oaddr(imem01_bank),
               .rd(imem01_rd),
               .wr(imem01_wr),
               .odata(imem01_out));

   // 2 番目の入力用メモリブロック
   wire [1:0] 	imem02_bank;
   wire 	imem02_rd;
   reg 		imem02_wr;
   reg [127:0] 	imem02_in;
   wire [127:0] imem02_out;
   imem imem02(.clock(clock),
               .oaddr(imem02_bank),
               .rd(imem02_rd),
               .wr(imem02_wr),
               .odata(imem02_out));

   // 3 番目の入力用メモリブロック
   wire [1:0] 	imem03_bank;
   wire 	imem03_rd;
   reg 		imem03_wr;
   reg [127:0] 	imem03_in;
   wire [127:0] imem03_out;
   imem imem03(.clock(clock),
               .oaddr(imem03_bank),
               .rd(imem03_rd),
               .wr(imem03_wr),
               .odata(imem03_out));

   // 4 番目の入力用メモリブロック
   wire [1:0] 	imem04_bank;
   wire 	imem04_rd;
   reg 		imem04_wr;
   reg [127:0] 	imem04_in;
   wire [127:0] imem04_out;
   imem imem04(.clock(clock),
               .oaddr(imem04_bank),
               .rd(imem04_rd),
               .wr(imem04_wr),
               .odata(imem04_out));

   // 5 番目の入力用メモリブロック
   wire [1:0] 	imem05_bank;
   wire		imem05_rd;
   reg 		imem05_wr;
   reg [127:0] 	imem05_in;
   wire [127:0] imem05_out;
   imem imem05(.clock(clock),
               .oaddr(imem05_bank),
               .rd(imem05_rd),
               .wr(imem05_wr),
               .odata(imem05_out));

   // 6 番目の入力用メモリブロック
   wire [1:0] 	imem06_bank;
   wire 	imem06_rd;
   reg 		imem06_wr;
   reg [127:0] 	imem06_in;
   wire [127:0] imem06_out;
   imem imem06(.clock(clock),
               .oaddr(imem06_bank),
               .rd(imem06_rd),
               .wr(imem06_wr),
               .odata(imem06_out));

   // 7 番目の入力用メモリブロック
   wire [1:0] 	imem07_bank;
   wire 	imem07_rd;
   reg 		imem07_wr;
   reg [127:0] 	imem07_in;
   wire [127:0] imem07_out;
   imem imem07(.clock(clock),
               .oaddr(imem07_bank),
               .rd(imem07_rd),
               .wr(imem07_wr),
               .odata(imem07_out));

   // 0 番目の出力用メモリブロック
   wire [5:0] 	omem00_bank;
   reg 		omem00_rd;
   wire 	omem00_wr;
   wire [8:0] 	omem00_in;
   wire [8:0] 	omem00_out;
   omem omem00(.clock(clock),
               .bank(omem00_bank),
               .rd(omem00_rd),
               .wr(omem00_wr),
               .in(omem00_in));

   // 1 番目の出力用メモリブロック
   wire [5:0] 	omem01_bank;
   reg 		omem01_rd;
   wire 	omem01_wr;
   wire [8:0] 	omem01_in;
   wire [8:0] 	omem01_out;
   omem omem01(.clock(clock),
               .bank(omem01_bank),
               .rd(omem01_rd),
               .wr(omem01_wr),
               .in(omem01_in));

   // 2 番目の出力用メモリブロック
   wire [5:0] 	omem02_bank;
   reg 		omem02_rd;
   wire 	omem02_wr;
   wire [8:0] 	omem02_in;
   wire [8:0] 	omem02_out;
   omem omem02(.clock(clock),
               .bank(omem02_bank),
               .rd(omem02_rd),
               .wr(omem02_wr),
               .in(omem02_in));

   // 3 番目の出力用メモリブロック
   wire [5:0] 	omem03_bank;
   reg 		omem03_rd;
   wire 	omem03_wr;
   wire [8:0] 	omem03_in;
   wire [8:0] 	omem03_out;
   omem omem03(.clock(clock),
               .bank(omem03_bank),
               .rd(omem03_rd),
               .wr(omem03_wr),
               .in(omem03_in));

   // 4 番目の出力用メモリブロック
   wire [5:0] 	omem04_bank;
   reg 		omem04_rd;
   wire 	omem04_wr;
   wire [8:0] 	omem04_in;
   wire [8:0] 	omem04_out;
   omem omem04(.clock(clock),
               .bank(omem04_bank),
               .rd(omem04_rd),
               .wr(omem04_wr),
               .in(omem04_in));

   // affine モジュールのインスタンス
   wire 	busy;
   affine2 affine2(.clock(clock),
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
                   .imem05_bank(imem05_bank),
                   .imem05_rd(imem05_rd),
                   .imem05_in(imem05_out),
                   .imem06_bank(imem06_bank),
                   .imem06_rd(imem06_rd),
                   .imem06_in(imem06_out),
                   .imem07_bank(imem07_bank),
                   .imem07_rd(imem07_rd),
                   .imem07_in(imem07_out),
                   .omem00_bank(omem00_bank),
                   .omem00_wr(omem00_wr),
                   .omem00_out(omem00_in),
                   .omem01_bank(omem01_bank),
                   .omem01_wr(omem01_wr),
                   .omem01_out(omem01_in),
                   .omem02_bank(omem02_bank),
                   .omem02_wr(omem02_wr),
                   .omem02_out(omem02_in),
                   .omem03_bank(omem03_bank),
                   .omem03_wr(omem03_wr),
                   .omem03_out(omem03_in),
                   .omem04_bank(omem04_bank),
                   .omem04_wr(omem04_wr),
                   .omem04_out(omem04_in));

   integer i, j;
   reg [8:0] omem0_ref[0:59];
   reg [8:0] omem1_ref[0:59];
   reg [8:0] omem2_ref[0:59];
   reg [8:0] omem3_ref[0:59];
   reg [8:0] omem4_ref[0:59];

   initial begin

      // リセット
      do_reset;

      start = 1'b0;

      imem00_wr = 1'b0;
      imem01_wr = 1'b0;
      imem02_wr = 1'b0;
      imem03_wr = 1'b0;
      imem04_wr = 1'b0;
      imem05_wr = 1'b0;
      imem06_wr = 1'b0;
      imem07_wr = 1'b0;

      omem00_rd = 1'b0;
      omem01_rd = 1'b0;
      omem02_rd = 1'b0;
      omem03_rd = 1'b0;
      omem04_rd = 1'b0;

      // 入力データの読み込み

      $readmemh("imem00.hex", imem00.memblock);
      $readmemh("imem01.hex", imem01.memblock);
      $readmemh("imem02.hex", imem02.memblock);
      $readmemh("imem03.hex", imem03.memblock);
      $readmemh("imem04.hex", imem04.memblock);
      $readmemh("imem05.hex", imem05.memblock);
      $readmemh("imem06.hex", imem06.memblock);
      $readmemh("imem07.hex", imem07.memblock);

      $readmemh("omem0.hex", omem0_ref);
      $readmemh("omem1.hex", omem1_ref);
      $readmemh("omem2.hex", omem2_ref);
      $readmemh("omem3.hex", omem3_ref);
      $readmemh("omem4.hex", omem4_ref);

      // affine モジュールを動作させる．
      start = 1'b1;

      wait_for_next_clock;

      // 完了を待つ．
      @ ( !busy );

      $display("affine2 finished");

      // 期待値と比較
      for ( i = 0; i < 60; i = i + 1 ) begin
	 if ( omem0_ref[i] != omem00.memblock[i] ) begin
	    $display("Error in omem0[%d]", i);
	    $display(" expected: %d, actual: %dx", omem0_ref[i], omem00.memblock[i]);
	 end
	 else begin
	    $display("omem0[%d] is OK", i);
	 end
	 if ( omem1_ref[i] != omem01.memblock[i] ) begin
	    $display("Error in omem1[%d]", i);
	    $display(" expected: %d, actual: %d", omem1_ref[i], omem01.memblock[i]);
	 end
	 else begin
	    $display("omem1[%d] is OK", i);
	 end
	 if ( omem2_ref[i] != omem02.memblock[i] ) begin
	    $display("Error in omem2[%d]", i);
	    $display(" expected: %d, actual: %d", omem2_ref[i], omem02.memblock[i]);
	 end
	 else begin
	    $display("omem2[%d] is OK", i);
	 end
	 if ( omem3_ref[i] != omem03.memblock[i] ) begin
	    $display("Error in omem3[%d]", i);
	    $display(" expected: %d, actual: %d", omem3_ref[i], omem03.memblock[i]);
	 end
	 else begin
	    $display("omem3[%d] is OK", i);
	 end
	 if ( omem4_ref[i] != omem04.memblock[i] ) begin
	    $display("Error in omem4[%d]", i);
	    $display(" expected: %d, actual: %d", omem4_ref[i], omem04.memblock[i]);
	 end
	 else begin
	    $display("omem4[%d] is OK", i);
	 end
      end

      $finish;

   end

endmodule // affine2_test
