
`timescale 1ns/1ns

// ダミーの8ビット入力12ビット出力の16入力加算器
module add8_16(input [7:0]   data0x,
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

   wire [11:0] 		   in0 = {{4{data0x[7]}}, data0x};
   wire [11:0] 		   in1 = {{4{data1x[7]}}, data1x};
   wire [11:0] 		   in2 = {{4{data2x[7]}}, data2x};
   wire [11:0] 		   in3 = {{4{data3x[7]}}, data3x};
   wire [11:0] 		   in4 = {{4{data4x[7]}}, data4x};
   wire [11:0] 		   in5 = {{4{data5x[7]}}, data5x};
   wire [11:0] 		   in6 = {{4{data6x[7]}}, data6x};
   wire [11:0] 		   in7 = {{4{data7x[7]}}, data7x};
   wire [11:0] 		   in8 = {{4{data8x[7]}}, data8x};
   wire [11:0] 		   in9 = {{4{data9x[7]}}, data9x};
   wire [11:0] 		   in10 = {{4{data10x[7]}}, data10x};
   wire [11:0] 		   in11 = {{4{data11x[7]}}, data11x};
   wire [11:0] 		   in12 = {{4{data12x[7]}}, data12x};
   wire [11:0] 		   in13 = {{4{data13x[7]}}, data13x};
   wire [11:0] 		   in14 = {{4{data14x[7]}}, data14x};
   wire [11:0] 		   in15 = {{4{data15x[7]}}, data15x};

   wire [11:0] 		   tmp1_1 = in0 + in1;
   wire [11:0] 		   tmp1_2 = in2 + in3;
   wire [11:0] 		   tmp1_3 = in4 + in5;
   wire [11:0] 		   tmp1_4 = in6 + in7;
   wire [11:0] 		   tmp1_5 = in8 + in9;
   wire [11:0] 		   tmp1_6 = in10 + in11;
   wire [11:0] 		   tmp1_7 = in12 + in13;
   wire [11:0] 		   tmp1_8 = in14 + in15;

   wire [11:0] 		   tmp2_1 = tmp1_1 + tmp1_2;
   wire [11:0] 		   tmp2_2 = tmp1_3 + tmp1_4;
   wire [11:0] 		   tmp2_3 = tmp1_5 + tmp1_6;
   wire [11:0] 		   tmp2_4 = tmp1_7 + tmp1_8;

   wire [11:0] 		   tmp3_1 = tmp2_1 + tmp2_2;
   wire [11:0] 		   tmp3_2 = tmp2_3 + tmp2_4;

   assign result = tmp3_1 + tmp3_2;
endmodule // add16

// ダミーの12ビット入力16ビット出力の16入力加算器
module add12_16(input [11:0]  data0x,
		input [11:0]  data1x,
		input [11:0]  data2x,
		input [11:0]  data3x,
		input [11:0]  data4x,
		input [11:0]  data5x,
		input [11:0]  data6x,
		input [11:0]  data7x,
		input [11:0]  data8x,
		input [11:0]  data9x,
		input [11:0]  data10x,
		input [11:0]  data11x,
		input [11:0]  data12x,
		input [11:0]  data13x,
		input [11:0]  data14x,
		input [11:0]  data15x,
		output [15:0] result);

   wire [15:0] 		     in0 = {{4{data0x[11]}}, data0x};
   wire [15:0] 		     in1 = {{4{data1x[11]}}, data1x};
   wire [15:0] 		     in2 = {{4{data2x[11]}}, data2x};
   wire [15:0] 		     in3 = {{4{data3x[11]}}, data3x};
   wire [15:0] 		     in4 = {{4{data4x[11]}}, data4x};
   wire [15:0] 		     in5 = {{4{data5x[11]}}, data5x};
   wire [15:0] 		     in6 = {{4{data6x[11]}}, data6x};
   wire [15:0] 		     in7 = {{4{data7x[11]}}, data7x};
   wire [15:0] 		     in8 = {{4{data8x[11]}}, data8x};
   wire [15:0] 		     in9 = {{4{data9x[11]}}, data9x};
   wire [15:0] 		     in10 = {{4{data10x[11]}}, data10x};
   wire [15:0] 		     in11 = {{4{data11x[11]}}, data11x};
   wire [15:0] 		     in12 = {{4{data12x[11]}}, data12x};
   wire [15:0] 		     in13 = {{4{data13x[11]}}, data13x};
   wire [15:0] 		     in14 = {{4{data14x[11]}}, data14x};
   wire [15:0] 		     in15 = {{4{data15x[11]}}, data15x};

   wire [15:0] 		     tmp1_1 = in0 + in1;
   wire [15:0] 		     tmp1_2 = in2 + in3;
   wire [15:0] 		     tmp1_3 = in4 + in5;
   wire [15:0] 		     tmp1_4 = in6 + in7;
   wire [15:0] 		     tmp1_5 = in8 + in9;
   wire [15:0] 		     tmp1_6 = in10 + in11;
   wire [15:0] 		     tmp1_7 = in12 + in13;
   wire [15:0] 		     tmp1_8 = in14 + in15;

   wire [15:0] tmp2_1 = tmp1_1 + tmp1_2;
   wire [15:0] tmp2_2 = tmp1_3 + tmp1_4;
   wire [15:0] tmp2_3 = tmp1_5 + tmp1_6;
   wire [15:0] tmp2_4 = tmp1_7 + tmp1_8;

   wire [15:0] tmp3_1 = tmp2_1 + tmp2_2;
   wire [15:0] tmp3_2 = tmp2_3 + tmp2_4;

   assign result = tmp3_1 + tmp3_2;
endmodule // add16_2

module affine_test;

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
   reg [255:0]  imem00_in;
   wire [255:0] imem00_out;
   imem imem00(.clock(clock),
               .oaddr(imem00_bank),
               .rd(imem00_rd),
               .wr(imem00_wr),
               .odata(imem00_out));

   // 1 番目の入力用メモリブロック
   wire [1:0] 	imem01_bank;
   wire		imem01_rd;
   reg 		imem01_wr;
   reg [255:0] 	imem01_in;
   wire [255:0] imem01_out;
   imem imem01(.clock(clock),
               .oaddr(imem01_bank),
               .rd(imem01_rd),
               .wr(imem01_wr),
               .odata(imem01_out));

   // 2 番目の入力用メモリブロック
   wire [1:0] 	imem02_bank;
   wire 	imem02_rd;
   reg 		imem02_wr;
   reg [255:0] 	imem02_in;
   wire [255:0] imem02_out;
   imem imem02(.clock(clock),
               .oaddr(imem02_bank),
               .rd(imem02_rd),
               .wr(imem02_wr),
               .odata(imem02_out));

   // 3 番目の入力用メモリブロック
   wire [1:0] 	imem03_bank;
   wire 	imem03_rd;
   reg 		imem03_wr;
   reg [255:0] 	imem03_in;
   wire [255:0] imem03_out;
   imem imem03(.clock(clock),
               .oaddr(imem03_bank),
               .rd(imem03_rd),
               .wr(imem03_wr),
               .odata(imem03_out));

   // 4 番目の入力用メモリブロック
   wire [1:0] 	imem04_bank;
   wire 	imem04_rd;
   reg 		imem04_wr;
   reg [255:0] 	imem04_in;
   wire [255:0] imem04_out;
   imem imem04(.clock(clock),
               .oaddr(imem04_bank),
               .rd(imem04_rd),
               .wr(imem04_wr),
               .odata(imem04_out));

   // 5 番目の入力用メモリブロック
   wire [1:0] 	imem05_bank;
   wire		imem05_rd;
   reg 		imem05_wr;
   reg [255:0] 	imem05_in;
   wire [255:0] imem05_out;
   imem imem05(.clock(clock),
               .oaddr(imem05_bank),
               .rd(imem05_rd),
               .wr(imem05_wr),
               .odata(imem05_out));

   // 6 番目の入力用メモリブロック
   wire [1:0] 	imem06_bank;
   wire 	imem06_rd;
   reg 		imem06_wr;
   reg [255:0] 	imem06_in;
   wire [255:0] imem06_out;
   imem imem06(.clock(clock),
               .oaddr(imem06_bank),
               .rd(imem06_rd),
               .wr(imem06_wr),
               .odata(imem06_out));

   // 7 番目の入力用メモリブロック
   wire [1:0] 	imem07_bank;
   wire 	imem07_rd;
   reg 		imem07_wr;
   reg [255:0] 	imem07_in;
   wire [255:0] imem07_out;
   imem imem07(.clock(clock),
               .oaddr(imem07_bank),
               .rd(imem07_rd),
               .wr(imem07_wr),
               .odata(imem07_out));

   // 8 番目の入力用メモリブロック
   wire [1:0] 	imem08_bank;
   wire 	imem08_rd;
   reg 		imem08_wr;
   reg [255:0] 	imem08_in;
   wire [255:0] imem08_out;
   imem imem08(.clock(clock),
               .oaddr(imem08_bank),
               .rd(imem08_rd),
               .wr(imem08_wr),
               .odata(imem08_out));

   // 9 番目の入力用メモリブロック
   wire [1:0] 	imem09_bank;
   wire 	imem09_rd;
   reg 		imem09_wr;
   reg [255:0] 	imem09_in;
   wire [255:0] imem09_out;
   imem imem09(.clock(clock),
               .oaddr(imem09_bank),
               .rd(imem09_rd),
               .wr(imem09_wr),
               .odata(imem09_out));

   // 10 番目の入力用メモリブロック
   wire [1:0] 	imem10_bank;
   wire 	imem10_rd;
   reg 		imem10_wr;
   reg [255:0] 	imem10_in;
   wire [255:0] imem10_out;
   imem imem10(.clock(clock),
               .oaddr(imem10_bank),
               .rd(imem10_rd),
               .wr(imem10_wr),
               .odata(imem10_out));

   // 11 番目の入力用メモリブロック
   wire [1:0] 	imem11_bank;
   wire 	imem11_rd;
   reg 		imem11_wr;
   reg [255:0] imem11_in;
   wire [255:0] imem11_out;
   imem imem11(.clock(clock),
               .oaddr(imem11_bank),
               .rd(imem11_rd),
               .wr(imem11_wr),
               .odata(imem11_out));

   // 0 番目の出力用メモリブロック
   wire [6:0] 	omem00_bank;
   reg 		omem00_rd;
   wire 	omem00_wr;
   wire [7:0] 	omem00_in;
   wire [7:0] 	omem00_out;
   omem omem00(.clock(clock),
               .bank(omem00_bank),
               .rd(omem00_rd),
               .wr(omem00_wr),
	       .in(omem00_in));

   // 1 番目の出力用メモリブロック
   wire [6:0] 	omem01_bank;
   reg 		omem01_rd;
   wire 	omem01_wr;
   wire [7:0] 	omem01_in;
   wire [7:0] 	omem01_out;
   omem omem01(.clock(clock),
               .bank(omem01_bank),
               .rd(omem01_rd),
               .wr(omem01_wr),
               .in(omem01_in));

   // 2 番目の出力用メモリブロック
   wire [6:0] 	omem02_bank;
   reg 		omem02_rd;
   wire 	omem02_wr;
   wire [7:0] 	omem02_in;
   wire [7:0] 	omem02_out;
   omem omem02(.clock(clock),
               .bank(omem02_bank),
               .rd(omem02_rd),
               .wr(omem02_wr),
               .in(omem02_in));

   // 3 番目の出力用メモリブロック
   wire [6:0] 	omem03_bank;
   reg 		omem03_rd;
   wire 	omem03_wr;
   wire [7:0] 	omem03_in;
   wire [7:0] 	omem03_out;
   omem omem03(.clock(clock),
               .bank(omem03_bank),
               .rd(omem03_rd),
               .wr(omem03_wr),
               .in(omem03_in));

   // 4 番目の出力用メモリブロック
   wire [6:0] 	omem04_bank;
   reg 		omem04_rd;
   wire 	omem04_wr;
   wire [7:0] 	omem04_in;
   wire [7:0] 	omem04_out;
   omem omem04(.clock(clock),
               .bank(omem04_bank),
               .rd(omem04_rd),
               .wr(omem04_wr),
               .in(omem04_in));

   // 5 番目の出力用メモリブロック
   wire [6:0] 	omem05_bank;
   reg 		omem05_rd;
   wire 	omem05_wr;
   wire [7:0] 	omem05_in;
   wire [7:0] 	omem05_out;
   omem omem05(.clock(clock),
               .bank(omem05_bank),
               .rd(omem05_rd),
               .wr(omem05_wr),
               .in(omem05_in));

   // 6 番目の出力用メモリブロック
   wire [6:0] 	omem06_bank;
   reg 		omem06_rd;
   wire 	omem06_wr;
   wire [7:0] 	omem06_in;
   wire [7:0] 	omem06_out;
   omem omem06(.clock(clock),
               .bank(omem06_bank),
               .rd(omem06_rd),
               .wr(omem06_wr),
               .in(omem06_in));

   // 7 番目の出力用メモリブロック
   wire [6:0] 	omem07_bank;
   reg 		omem07_rd;
   wire 	omem07_wr;
   wire [7:0] 	omem07_in;
   wire [7:0] 	omem07_out;
   omem omem07(.clock(clock),
               .bank(omem07_bank),
               .rd(omem07_rd),
               .wr(omem07_wr),
               .in(omem07_in));

   // affine モジュールのインスタンス
   wire 	busy;
   affine affine(.clock(clock),
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
                 .imem08_bank(imem08_bank),
                 .imem08_rd(imem08_rd),
                 .imem08_in(imem08_out),
                 .imem09_bank(imem09_bank),
                 .imem09_rd(imem09_rd),
                 .imem09_in(imem09_out),
                 .imem10_bank(imem10_bank),
                 .imem10_rd(imem10_rd),
                 .imem10_in(imem10_out),
                 .imem11_bank(imem11_bank),
                 .imem11_rd(imem11_rd),
                 .imem11_in(imem11_out),
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
                 .omem04_out(omem04_in),
                 .omem05_bank(omem05_bank),
                 .omem05_wr(omem05_wr),
                 .omem05_out(omem05_in),
                 .omem06_bank(omem06_bank),
                 .omem06_wr(omem06_wr),
                 .omem06_out(omem06_in),
                 .omem07_bank(omem07_bank),
                 .omem07_wr(omem07_wr),
                 .omem07_out(omem07_in));

   integer i, j;
   reg [7:0] omem0_ref[0:124];
   reg [7:0] omem1_ref[0:124];
   reg [7:0] omem2_ref[0:124];
   reg [7:0] omem3_ref[0:124];
   reg [7:0] omem4_ref[0:124];
   reg [7:0] omem5_ref[0:124];
   reg [7:0] omem6_ref[0:124];
   reg [7:0] omem7_ref[0:124];

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
      imem08_wr = 1'b0;
      imem09_wr = 1'b0;
      imem10_wr = 1'b0;
      imem11_wr = 1'b0;

      omem00_rd = 1'b0;
      omem01_rd = 1'b0;
      omem02_rd = 1'b0;
      omem03_rd = 1'b0;
      omem04_rd = 1'b0;
      omem05_rd = 1'b0;
      omem06_rd = 1'b0;
      omem07_rd = 1'b0;

      // 入力データの読み込み

      $readmemh("imem00.hex", imem00.memblock);
      $readmemh("imem01.hex", imem01.memblock);
      $readmemh("imem02.hex", imem02.memblock);
      $readmemh("imem03.hex", imem03.memblock);
      $readmemh("imem04.hex", imem04.memblock);
      $readmemh("imem05.hex", imem05.memblock);
      $readmemh("imem06.hex", imem06.memblock);
      $readmemh("imem07.hex", imem07.memblock);
      $readmemh("imem08.hex", imem08.memblock);
      $readmemh("imem09.hex", imem09.memblock);
      $readmemh("imem10.hex", imem10.memblock);
      $readmemh("imem11.hex", imem11.memblock);

      $readmemh("omem0.hex", omem0_ref);
      $readmemh("omem1.hex", omem1_ref);
      $readmemh("omem2.hex", omem2_ref);
      $readmemh("omem3.hex", omem3_ref);
      $readmemh("omem4.hex", omem4_ref);
      $readmemh("omem5.hex", omem5_ref);
      $readmemh("omem6.hex", omem6_ref);
      $readmemh("omem7.hex", omem7_ref);

      // affine モジュールを動作させる．
      start = 1'b1;

      wait_for_next_clock;

      // 完了を待つ．
      @ ( !busy );

      $display("affine finished");

      // 期待値と比較
      for ( i = 0; i < 125; i = i + 1 ) begin
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
	 if ( omem5_ref[i] != omem05.memblock[i] ) begin
	    $display("Error in omem5[%d]", i);
	    $display(" expected: %d, actual: %d", omem5_ref[i], omem05.memblock[i]);
	 end
	 else begin
	    $display("omem5[%d] is OK", i);
	 end
	 if ( omem6_ref[i] != omem06.memblock[i] ) begin
	    $display("Error in omem6[%d]", i);
	    $display(" expected: %d, actual: %d", omem6_ref[i], omem06.memblock[i]);
	 end
	 else begin
	    $display("omem6[%d] is OK", i);
	 end
	 if ( omem7_ref[i] != omem07.memblock[i] ) begin
	    $display("Error in omem7[%d]", i);
	    $display(" expected: %d, actual: %d", omem7_ref[i], omem07.memblock[i]);
	 end
	 else begin
	    $display("omem7[%d] is OK", i);
	 end
      end

      $finish;

   end

endmodule // affine_test
