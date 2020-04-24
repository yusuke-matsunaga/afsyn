// 入力用メモリブロック
//
// 4bit を1つの単位として128個のデータを持つ．
// 書き込む際には1つずつ書き込む．
// 読み出す際には32個のデータをひとまとめに読み出す．
// そのためアドレスは2ビットとなる．
// clock: クロック
// iaddr: 書き込みアドレス
// idata: 書き込むデータ
// wr:    書き込み制御
// oaddr: 読み出すアドレス
// odata: 読み出したデータ
// rd:    読み出し制御
module imem(input          clock,
	    input [6:0]    iaddr,
	    input [3:0]    idata,
	    input 	   wr,
	    input [1:0]    oaddr,
	    output [127:0] odata,
	    input 	   rd);

   reg [127:0] 		 memblock[0:3];
   reg [127:0] 		 tmp_out;
   wire 		 ibank = iaddr[6:5];
   always @ ( posedge clock ) begin
      if ( wr ) begin
	 case ( iaddr[4:0] )
	   5'd00: memblock[ibank][  3:  0] <= idata;
	   5'd01: memblock[ibank][  7:  4] <= idata;
	   5'd02: memblock[ibank][ 11:  8] <= idata;
	   5'd03: memblock[ibank][ 15: 12] <= idata;
	   5'd04: memblock[ibank][ 19: 16] <= idata;
	   5'd05: memblock[ibank][ 23: 20] <= idata;
	   5'd06: memblock[ibank][ 27: 24] <= idata;
	   5'd07: memblock[ibank][ 31: 28] <= idata;
	   5'd08: memblock[ibank][ 35: 32] <= idata;
	   5'd09: memblock[ibank][ 39: 36] <= idata;
	   5'd10: memblock[ibank][ 43: 40] <= idata;
	   5'd11: memblock[ibank][ 47: 44] <= idata;
	   5'd12: memblock[ibank][ 51: 48] <= idata;
	   5'd13: memblock[ibank][ 55: 52] <= idata;
	   5'd14: memblock[ibank][ 59: 56] <= idata;
	   5'd15: memblock[ibank][ 63: 60] <= idata;
	   5'd16: memblock[ibank][ 67: 64] <= idata;
	   5'd17: memblock[ibank][ 71: 68] <= idata;
	   5'd18: memblock[ibank][ 75: 72] <= idata;
	   5'd19: memblock[ibank][ 79: 76] <= idata;
	   5'd20: memblock[ibank][ 83: 80] <= idata;
	   5'd21: memblock[ibank][ 87: 84] <= idata;
	   5'd22: memblock[ibank][ 91: 88] <= idata;
	   5'd23: memblock[ibank][ 95: 92] <= idata;
	   5'd24: memblock[ibank][ 99: 96] <= idata;
	   5'd25: memblock[ibank][103:100] <= idata;
	   5'd26: memblock[ibank][107:104] <= idata;
	   5'd27: memblock[ibank][111:108] <= idata;
	   5'd28: memblock[ibank][115:112] <= idata;
	   5'd29: memblock[ibank][119:116] <= idata;
	   5'd30: memblock[ibank][123:120] <= idata;
	   5'd31: memblock[ibank][127:124] <= idata;
	 endcase
      end // if ( wr )
      else if ( rd ) begin
	 tmp_out <= memblock[oaddr];
      end
   end // always @ ( posedge clock )

   assign out = tmp_out;

endmodule
