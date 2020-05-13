// 入力用メモリブロック
//
// 9bit を1つの単位として60個のデータを持つ．
// 書き込む際には1つずつ書き込む．
// 読み出す際にも1つずつ読み出す．
// そのためアドレスは6ビットとなる．
// clock: クロック
// iaddr: 書き込みアドレス
// idata: 書き込むデータ
// wr:    書き込み制御
// oaddr: 読み出すアドレス
// odata: 読み出したデータ
// rd:    読み出し制御
module imem(input        clock,
	    input [5:0]  iaddr,
	    input [5:0]  idata,
	    input 	 wr,
	    input [5:0]  oaddr,
	    output [5:0] odata,
	    input 	 rd);

   reg [5:0] 		 memblock[0:5];
   reg [5:0] 		 tmp_out;
   always @ ( posedge clock ) begin
      if ( wr ) begin
	 memblock[iaddr] <= idata;
      end // if ( wr )
      else if ( rd ) begin
	 tmp_out <= memblock[iaddr];
      end
   end // always @ ( posedge clock )

   assign out = tmp_out;

endmodule
