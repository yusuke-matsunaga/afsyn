// 第１層と第２層の間のメモリブロック
//
// 4bit を1つの単位として127個のデータを持つ．
// 書き込む際には直接アドレスを指定する．
// 読み出す際には32個のデータをひとまとめに読み出す．
// そのためアドレスは2ビットとなる．
// clock:  クロック
// iaddr:  書き込むアドレス
// idata:  書き込むデータ
// wr:     書き込み制御
// oaddr:  読み出すアドレス
// odata:  読み出したデータ
// rd:     読み出し制御
module l1mem(input          clock,
	     input [6:0]    iaddr,
	     input [3:0]    idata,
	     input 	    wr,
	     input [1:0]    oaddr,
	     output [127:0] odata,
	     input 	    rd);

   reg [127:0] 		    memblock[0:3];
   reg [127:0] 		    tmp_out;
   wire 		    ibank = iaddr[6:5];
   always @ ( posedge clock ) begin
      if ( wr ) begin
	 case ( iaddr[4:0] )
	   4'd00: memblock[ibank][  3:  0] <= idata;
	   4'd01: memblock[ibank][  7:  4] <= idata;
	   4'd02: memblock[ibank][ 11:  8] <= idata;
	   4'd03: memblock[ibank][ 15: 12] <= idata;
	   4'd04: memblock[ibank][ 19: 16] <= idata;
	   4'd05: memblock[ibank][ 23: 20] <= idata;
	   4'd06: memblock[ibank][ 27: 24] <= idata;
	   4'd07: memblock[ibank][ 31: 28] <= idata;
	   4'd08: memblock[ibank][ 35: 32] <= idata;
	   4'd09: memblock[ibank][ 39: 36] <= idata;
	   4'd10: memblock[ibank][ 43: 40] <= idata;
	   4'd11: memblock[ibank][ 47: 44] <= idata;
	   4'd12: memblock[ibank][ 51: 48] <= idata;
	   4'd13: memblock[ibank][ 55: 52] <= idata;
	   4'd14: memblock[ibank][ 59: 56] <= idata;
	   4'd15: memblock[ibank][ 63: 60] <= idata;
	   4'd16: memblock[ibank][ 67: 64] <= idata;
	   4'd17: memblock[ibank][ 71: 68] <= idata;
	   4'd18: memblock[ibank][ 75: 72] <= idata;
	   4'd19: memblock[ibank][ 79: 76] <= idata;
	   4'd20: memblock[ibank][ 83: 80] <= idata;
	   4'd21: memblock[ibank][ 87: 84] <= idata;
	   4'd22: memblock[ibank][ 91: 88] <= idata;
	   4'd23: memblock[ibank][ 95: 92] <= idata;
	   4'd24: memblock[ibank][ 99: 96] <= idata;
	   4'd25: memblock[ibank][103:100] <= idata;
	   4'd26: memblock[ibank][107:104] <= idata;
	   4'd27: memblock[ibank][111:108] <= idata;
	   4'd28: memblock[ibank][115:112] <= idata;
	   4'd29: memblock[ibank][119:116] <= idata;
	   4'd30: memblock[ibank][123:120] <= idata;
	   4'd31: memblock[ibank][127:124] <= idata;
	 endcase
      end // if ( wr )
      else if ( rd ) begin
	 tmp_out <= memblock[oaddr];
      end
   end // always @ ( posedge clock )

   assign odata = tmp_out;

endmodule
