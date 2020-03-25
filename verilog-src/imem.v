// 入力用メモリブロック

// clk:  クロック
// bank: バンク
// rd:   読み出し制御
// outX: X番目の読み出し口
module imem(input          clock,
	    input [1:0]    bank,
	    input 	   rd,
	    input 	   wr,
	    input [255:0]  in,
	    output [255:0] out);

   reg [255:0] 		 memblock[0:3];
   reg [255:0] 		 tmp_out;
   always @ ( posedge clock ) begin
      if ( wr ) begin
	 memblock[bank] <= in;
      end
      if ( rd ) begin
	 tmp_out <= memblock[bank];
      end
   end

   assign out = tmp_out;
endmodule
