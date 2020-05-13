// tmem (1層目TanH -> affine2のバッファ)
//
// clock:    クロック入力
// data_in:  4ビットのデータ入力
// wr_addr:  書き込みアドレス(7ビット)
// wr:       書き込み制御
// data_out: 128ビットのデータ出力
// rd_addr:  読み出しアドレス(2ビット)
// rd:       読み出し制御
module tmem(input          clock,
	    input [3:0]    data_in,
	    input [6:0]    wr_addr,
	    input 	   wr,
	    output [127:0] data_out,
	    input [1:0]    rd_addr,
	    input 	   rd);


endmodule // tmem
