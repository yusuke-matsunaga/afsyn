module affine3(
  input clock,
  input reset,
  input start,
  output busy,
  output [5:0] imem00_bank,
  output imem00_rd,
  input [5:0] imem00_in,
  output [5:0] imem01_bank,
  output imem01_rd,
  input [5:0] imem01_in,
  output [5:0] imem02_bank,
  output imem02_rd,
  input [5:0] imem02_in,
  output [5:0] imem03_bank,
  output imem03_rd,
  input [5:0] imem03_in,
  output [5:0] imem04_bank,
  output imem04_rd,
  input [5:0] imem04_in,
  output omem00_wr,
  output [13:0] omem00_out);


  // 0 番目の OP1
  reg [5:0] op1_00_in00;
  reg       op1_00_inv00;
  reg [5:0] op1_00_in01;
  reg       op1_00_inv01;
  reg [5:0] op1_00_in02;
  reg       op1_00_inv02;
  reg [5:0] op1_00_in03;
  reg       op1_00_inv03;
  reg [5:0] op1_00_in04;
  reg       op1_00_inv04;
  reg [5:0] op1_00_in05;
  reg       op1_00_inv05;
  reg [5:0] op1_00_in06;
  reg       op1_00_inv06;
  reg [5:0] op1_00_in07;
  reg       op1_00_inv07;
  reg [5:0] op1_00_in08;
  reg       op1_00_inv08;
  reg [5:0] op1_00_in09;
  reg       op1_00_inv09;
  reg [5:0] op1_00_in10;
  reg       op1_00_inv10;
  reg [5:0] op1_00_in11;
  reg       op1_00_inv11;
  reg [5:0] op1_00_in12;
  reg       op1_00_inv12;
  reg [5:0] op1_00_in13;
  reg       op1_00_inv13;
  reg [5:0] op1_00_in14;
  reg       op1_00_inv14;
  reg [5:0] op1_00_in15;
  reg       op1_00_inv15;
  wire [9:0] op1_00_out;
  affine3_op1 op1_00(
    .data0_in(op1_00_in00),
    .inv0_in(op1_00_inv00),
    .data1_in(op1_00_in01),
    .inv1_in(op1_00_inv01),
    .data2_in(op1_00_in02),
    .inv2_in(op1_00_inv02),
    .data3_in(op1_00_in03),
    .inv3_in(op1_00_inv03),
    .data4_in(op1_00_in04),
    .inv4_in(op1_00_inv04),
    .data5_in(op1_00_in05),
    .inv5_in(op1_00_inv05),
    .data6_in(op1_00_in06),
    .inv6_in(op1_00_inv06),
    .data7_in(op1_00_in07),
    .inv7_in(op1_00_inv07),
    .data8_in(op1_00_in08),
    .inv8_in(op1_00_inv08),
    .data9_in(op1_00_in09),
    .inv9_in(op1_00_inv09),
    .data10_in(op1_00_in10),
    .inv10_in(op1_00_inv10),
    .data11_in(op1_00_in11),
    .inv11_in(op1_00_inv11),
    .data12_in(op1_00_in12),
    .inv12_in(op1_00_inv12),
    .data13_in(op1_00_in13),
    .inv13_in(op1_00_inv13),
    .data14_in(op1_00_in14),
    .inv14_in(op1_00_inv14),
    .data15_in(op1_00_in15),
    .inv15_in(op1_00_inv15),
    .data_out(op1_00_out));

  // 1 番目の OP1
  reg [5:0] op1_01_in00;
  reg       op1_01_inv00;
  reg [5:0] op1_01_in01;
  reg       op1_01_inv01;
  reg [5:0] op1_01_in02;
  reg       op1_01_inv02;
  reg [5:0] op1_01_in03;
  reg       op1_01_inv03;
  reg [5:0] op1_01_in04;
  reg       op1_01_inv04;
  reg [5:0] op1_01_in05;
  reg       op1_01_inv05;
  reg [5:0] op1_01_in06;
  reg       op1_01_inv06;
  reg [5:0] op1_01_in07;
  reg       op1_01_inv07;
  reg [5:0] op1_01_in08;
  reg       op1_01_inv08;
  reg [5:0] op1_01_in09;
  reg       op1_01_inv09;
  reg [5:0] op1_01_in10;
  reg       op1_01_inv10;
  reg [5:0] op1_01_in11;
  reg       op1_01_inv11;
  reg [5:0] op1_01_in12;
  reg       op1_01_inv12;
  reg [5:0] op1_01_in13;
  reg       op1_01_inv13;
  reg [5:0] op1_01_in14;
  reg       op1_01_inv14;
  reg [5:0] op1_01_in15;
  reg       op1_01_inv15;
  wire [9:0] op1_01_out;
  affine3_op1 op1_01(
    .data0_in(op1_01_in00),
    .inv0_in(op1_01_inv00),
    .data1_in(op1_01_in01),
    .inv1_in(op1_01_inv01),
    .data2_in(op1_01_in02),
    .inv2_in(op1_01_inv02),
    .data3_in(op1_01_in03),
    .inv3_in(op1_01_inv03),
    .data4_in(op1_01_in04),
    .inv4_in(op1_01_inv04),
    .data5_in(op1_01_in05),
    .inv5_in(op1_01_inv05),
    .data6_in(op1_01_in06),
    .inv6_in(op1_01_inv06),
    .data7_in(op1_01_in07),
    .inv7_in(op1_01_inv07),
    .data8_in(op1_01_in08),
    .inv8_in(op1_01_inv08),
    .data9_in(op1_01_in09),
    .inv9_in(op1_01_inv09),
    .data10_in(op1_01_in10),
    .inv10_in(op1_01_inv10),
    .data11_in(op1_01_in11),
    .inv11_in(op1_01_inv11),
    .data12_in(op1_01_in12),
    .inv12_in(op1_01_inv12),
    .data13_in(op1_01_in13),
    .inv13_in(op1_01_inv13),
    .data14_in(op1_01_in14),
    .inv14_in(op1_01_inv14),
    .data15_in(op1_01_in15),
    .inv15_in(op1_01_inv15),
    .data_out(op1_01_out));

  // 2 番目の OP1
  reg [5:0] op1_02_in00;
  reg       op1_02_inv00;
  reg [5:0] op1_02_in01;
  reg       op1_02_inv01;
  reg [5:0] op1_02_in02;
  reg       op1_02_inv02;
  reg [5:0] op1_02_in03;
  reg       op1_02_inv03;
  reg [5:0] op1_02_in04;
  reg       op1_02_inv04;
  reg [5:0] op1_02_in05;
  reg       op1_02_inv05;
  reg [5:0] op1_02_in06;
  reg       op1_02_inv06;
  reg [5:0] op1_02_in07;
  reg       op1_02_inv07;
  reg [5:0] op1_02_in08;
  reg       op1_02_inv08;
  reg [5:0] op1_02_in09;
  reg       op1_02_inv09;
  reg [5:0] op1_02_in10;
  reg       op1_02_inv10;
  reg [5:0] op1_02_in11;
  reg       op1_02_inv11;
  reg [5:0] op1_02_in12;
  reg       op1_02_inv12;
  reg [5:0] op1_02_in13;
  reg       op1_02_inv13;
  reg [5:0] op1_02_in14;
  reg       op1_02_inv14;
  reg [5:0] op1_02_in15;
  reg       op1_02_inv15;
  wire [9:0] op1_02_out;
  affine3_op1 op1_02(
    .data0_in(op1_02_in00),
    .inv0_in(op1_02_inv00),
    .data1_in(op1_02_in01),
    .inv1_in(op1_02_inv01),
    .data2_in(op1_02_in02),
    .inv2_in(op1_02_inv02),
    .data3_in(op1_02_in03),
    .inv3_in(op1_02_inv03),
    .data4_in(op1_02_in04),
    .inv4_in(op1_02_inv04),
    .data5_in(op1_02_in05),
    .inv5_in(op1_02_inv05),
    .data6_in(op1_02_in06),
    .inv6_in(op1_02_inv06),
    .data7_in(op1_02_in07),
    .inv7_in(op1_02_inv07),
    .data8_in(op1_02_in08),
    .inv8_in(op1_02_inv08),
    .data9_in(op1_02_in09),
    .inv9_in(op1_02_inv09),
    .data10_in(op1_02_in10),
    .inv10_in(op1_02_inv10),
    .data11_in(op1_02_in11),
    .inv11_in(op1_02_inv11),
    .data12_in(op1_02_in12),
    .inv12_in(op1_02_inv12),
    .data13_in(op1_02_in13),
    .inv13_in(op1_02_inv13),
    .data14_in(op1_02_in14),
    .inv14_in(op1_02_inv14),
    .data15_in(op1_02_in15),
    .inv15_in(op1_02_inv15),
    .data_out(op1_02_out));

  // 0 番目の OP2
  reg [9:0] op2_00_in00;
  reg [9:0] op2_00_in01;
  reg [9:0] op2_00_in02;
  reg [9:0] op2_00_in03;
  reg [9:0] op2_00_in04;
  reg [9:0] op2_00_in05;
  reg [9:0] op2_00_in06;
  reg [9:0] op2_00_in07;
  reg [9:0] op2_00_in08;
  reg [9:0] op2_00_in09;
  reg [9:0] op2_00_in10;
  reg [9:0] op2_00_in11;
  reg [9:0] op2_00_in12;
  reg [9:0] op2_00_in13;
  reg [9:0] op2_00_in14;
  reg [9:0] op2_00_bias;
  wire [13:0] op2_00_out;
  affine3_op2 op2_00(
    .data0_in(op2_00_in00),
    .data1_in(op2_00_in01),
    .data2_in(op2_00_in02),
    .data3_in(op2_00_in03),
    .data4_in(op2_00_in04),
    .data5_in(op2_00_in05),
    .data6_in(op2_00_in06),
    .data7_in(op2_00_in07),
    .data8_in(op2_00_in08),
    .data9_in(op2_00_in09),
    .data10_in(op2_00_in10),
    .data11_in(op2_00_in11),
    .data12_in(op2_00_in12),
    .data13_in(op2_00_in13),
    .data14_in(op2_00_in14),
    .data15_in(op2_00_bias),
    .data_out(op2_00_out));

  // 中間レジスタ
  reg [13:0] reg_0000;
  reg [13:0] reg_0001;
  reg [13:0] reg_0002;
  reg [13:0] reg_0003;
  reg [13:0] reg_0004;
  reg [13:0] reg_0005;
  reg [13:0] reg_0006;
  reg [13:0] reg_0007;
  reg [13:0] reg_0008;
  reg [13:0] reg_0009;
  reg [13:0] reg_0010;
  reg [13:0] reg_0011;
  reg [13:0] reg_0012;
  reg [13:0] reg_0013;
  reg [13:0] reg_0014;
  reg [13:0] reg_0015;
  reg [13:0] reg_0016;
  reg [13:0] reg_0017;
  reg [13:0] reg_0018;
  reg [13:0] reg_0019;
  reg [13:0] reg_0020;
  reg [13:0] reg_0021;
  reg [13:0] reg_0022;
  reg [13:0] reg_0023;
  reg [13:0] reg_0024;
  reg [13:0] reg_0025;
  reg [13:0] reg_0026;
  reg [13:0] reg_0027;
  reg [13:0] reg_0028;
  reg [13:0] reg_0029;
  reg [13:0] reg_0030;
  reg [13:0] reg_0031;
  reg [13:0] reg_0032;
  reg [13:0] reg_0033;
  reg [13:0] reg_0034;
  reg [13:0] reg_0035;
  reg [13:0] reg_0036;
  reg [13:0] reg_0037;
  reg [13:0] reg_0038;
  reg [13:0] reg_0039;
  reg [13:0] reg_0040;
  reg [13:0] reg_0041;
  reg [13:0] reg_0042;
  reg [13:0] reg_0043;
  reg [13:0] reg_0044;
  reg [13:0] reg_0045;
  reg [13:0] reg_0046;
  reg [13:0] reg_0047;
  reg [13:0] reg_0048;
  reg [13:0] reg_0049;
  reg [13:0] reg_0050;
  reg [13:0] reg_0051;
  reg [13:0] reg_0052;
  reg [13:0] reg_0053;
  reg [13:0] reg_0054;
  reg [13:0] reg_0055;
  reg [13:0] reg_0056;
  reg [13:0] reg_0057;
  reg [13:0] reg_0058;
  reg [13:0] reg_0059;
  reg [13:0] reg_0060;
  reg [13:0] reg_0061;
  reg [13:0] reg_0062;
  reg [13:0] reg_0063;
  reg [13:0] reg_0064;
  reg [13:0] reg_0065;
  reg [13:0] reg_0066;
  reg [13:0] reg_0067;
  reg [13:0] reg_0068;
  reg [13:0] reg_0069;
  reg [13:0] reg_0070;
  reg [13:0] reg_0071;
  reg [13:0] reg_0072;
  reg [13:0] reg_0073;
  reg [13:0] reg_0074;
  reg [13:0] reg_0075;
  reg [13:0] reg_0076;
  reg [13:0] reg_0077;
  reg [13:0] reg_0078;

  // 制御マシンの状態
  reg [5:0] state;
  reg _busy;
  assign busy = _busy;
  // 制御マシンの動作
  always @ ( posedge clock or negedge reset ) begin
    if ( !reset ) begin
      _busy <= 0;
      state <= 0;
    end
    else if ( _busy ) begin
      if ( state < 38 ) begin
        state <= state + 1;
      end
      else begin
        _busy <= 0;
        state <= 0;
      end
    end
    else if ( start ) begin
      _busy <= 1;
    end
  end

  // 0番目の入力用メモリブロックの制御
  reg [5:0] _imem00_bank;
  always @ ( * ) begin
    case ( state )
    13: _imem00_bank = 0;
    12: _imem00_bank = 1;
    11: _imem00_bank = 5;
    10: _imem00_bank = 6;
    9: _imem00_bank = 10;
    8: _imem00_bank = 14;
    7: _imem00_bank = 16;
    6: _imem00_bank = 18;
    5: _imem00_bank = 19;
    4: _imem00_bank = 21;
    3: _imem00_bank = 22;
    2: _imem00_bank = 26;
    1: _imem00_bank = 27;
    0: _imem00_bank = 29;
    26: _imem00_bank = 30;
    25: _imem00_bank = 33;
    24: _imem00_bank = 35;
    23: _imem00_bank = 36;
    22: _imem00_bank = 37;
    21: _imem00_bank = 38;
    20: _imem00_bank = 39;
    19: _imem00_bank = 41;
    18: _imem00_bank = 46;
    17: _imem00_bank = 50;
    16: _imem00_bank = 52;
    15: _imem00_bank = 55;
    14: _imem00_bank = 56;
    27: _imem00_bank = 57;
    default: _imem00_bank = 0;
    endcase
  end // always @ ( * )
  assign imem00_bank = _imem00_bank;
  reg _imem00_rd;
  always @ ( * ) begin
    case ( state )
    13: _imem00_rd = 1;
    12: _imem00_rd = 1;
    11: _imem00_rd = 1;
    10: _imem00_rd = 1;
    9: _imem00_rd = 1;
    8: _imem00_rd = 1;
    7: _imem00_rd = 1;
    6: _imem00_rd = 1;
    5: _imem00_rd = 1;
    4: _imem00_rd = 1;
    3: _imem00_rd = 1;
    2: _imem00_rd = 1;
    1: _imem00_rd = 1;
    0: _imem00_rd = 1;
    26: _imem00_rd = 1;
    25: _imem00_rd = 1;
    24: _imem00_rd = 1;
    23: _imem00_rd = 1;
    22: _imem00_rd = 1;
    21: _imem00_rd = 1;
    20: _imem00_rd = 1;
    19: _imem00_rd = 1;
    18: _imem00_rd = 1;
    17: _imem00_rd = 1;
    16: _imem00_rd = 1;
    15: _imem00_rd = 1;
    14: _imem00_rd = 1;
    27: _imem00_rd = 1;
    default: _imem00_rd = 0;
    endcase
  end // always @ ( * )
  assign imem00_rd = _imem00_rd;

  // 1番目の入力用メモリブロックの制御
  reg [5:0] _imem01_bank;
  always @ ( * ) begin
    case ( state )
    27: _imem01_bank = 0;
    26: _imem01_bank = 1;
    25: _imem01_bank = 2;
    24: _imem01_bank = 3;
    23: _imem01_bank = 7;
    22: _imem01_bank = 8;
    21: _imem01_bank = 10;
    20: _imem01_bank = 13;
    19: _imem01_bank = 14;
    18: _imem01_bank = 15;
    17: _imem01_bank = 18;
    16: _imem01_bank = 19;
    14: _imem01_bank = 21;
    13: _imem01_bank = 26;
    12: _imem01_bank = 27;
    11: _imem01_bank = 28;
    10: _imem01_bank = 30;
    9: _imem01_bank = 33;
    8: _imem01_bank = 35;
    7: _imem01_bank = 37;
    6: _imem01_bank = 39;
    5: _imem01_bank = 40;
    4: _imem01_bank = 41;
    3: _imem01_bank = 42;
    2: _imem01_bank = 43;
    1: _imem01_bank = 44;
    0: _imem01_bank = 45;
    33: _imem01_bank = 49;
    32: _imem01_bank = 52;
    31: _imem01_bank = 54;
    30: _imem01_bank = 55;
    29: _imem01_bank = 57;
    28: _imem01_bank = 58;
    15: _imem01_bank = 59;
    default: _imem01_bank = 0;
    endcase
  end // always @ ( * )
  assign imem01_bank = _imem01_bank;
  reg _imem01_rd;
  always @ ( * ) begin
    case ( state )
    27: _imem01_rd = 1;
    26: _imem01_rd = 1;
    25: _imem01_rd = 1;
    24: _imem01_rd = 1;
    23: _imem01_rd = 1;
    22: _imem01_rd = 1;
    21: _imem01_rd = 1;
    20: _imem01_rd = 1;
    19: _imem01_rd = 1;
    18: _imem01_rd = 1;
    17: _imem01_rd = 1;
    16: _imem01_rd = 1;
    14: _imem01_rd = 1;
    13: _imem01_rd = 1;
    12: _imem01_rd = 1;
    11: _imem01_rd = 1;
    10: _imem01_rd = 1;
    9: _imem01_rd = 1;
    8: _imem01_rd = 1;
    7: _imem01_rd = 1;
    6: _imem01_rd = 1;
    5: _imem01_rd = 1;
    4: _imem01_rd = 1;
    3: _imem01_rd = 1;
    2: _imem01_rd = 1;
    1: _imem01_rd = 1;
    0: _imem01_rd = 1;
    33: _imem01_rd = 1;
    32: _imem01_rd = 1;
    31: _imem01_rd = 1;
    30: _imem01_rd = 1;
    29: _imem01_rd = 1;
    28: _imem01_rd = 1;
    15: _imem01_rd = 1;
    default: _imem01_rd = 0;
    endcase
  end // always @ ( * )
  assign imem01_rd = _imem01_rd;

  // 2番目の入力用メモリブロックの制御
  reg [5:0] _imem02_bank;
  always @ ( * ) begin
    case ( state )
    33: _imem02_bank = 4;
    32: _imem02_bank = 6;
    31: _imem02_bank = 7;
    30: _imem02_bank = 11;
    29: _imem02_bank = 14;
    14: _imem02_bank = 16;
    13: _imem02_bank = 17;
    12: _imem02_bank = 18;
    11: _imem02_bank = 20;
    10: _imem02_bank = 21;
    9: _imem02_bank = 22;
    8: _imem02_bank = 23;
    7: _imem02_bank = 24;
    6: _imem02_bank = 26;
    5: _imem02_bank = 27;
    4: _imem02_bank = 29;
    3: _imem02_bank = 30;
    2: _imem02_bank = 31;
    1: _imem02_bank = 32;
    0: _imem02_bank = 33;
    26: _imem02_bank = 35;
    25: _imem02_bank = 36;
    24: _imem02_bank = 39;
    23: _imem02_bank = 42;
    22: _imem02_bank = 43;
    21: _imem02_bank = 47;
    20: _imem02_bank = 50;
    19: _imem02_bank = 51;
    18: _imem02_bank = 55;
    17: _imem02_bank = 56;
    16: _imem02_bank = 57;
    15: _imem02_bank = 59;
    default: _imem02_bank = 0;
    endcase
  end // always @ ( * )
  assign imem02_bank = _imem02_bank;
  reg _imem02_rd;
  always @ ( * ) begin
    case ( state )
    33: _imem02_rd = 1;
    32: _imem02_rd = 1;
    31: _imem02_rd = 1;
    30: _imem02_rd = 1;
    29: _imem02_rd = 1;
    14: _imem02_rd = 1;
    13: _imem02_rd = 1;
    12: _imem02_rd = 1;
    11: _imem02_rd = 1;
    10: _imem02_rd = 1;
    9: _imem02_rd = 1;
    8: _imem02_rd = 1;
    7: _imem02_rd = 1;
    6: _imem02_rd = 1;
    5: _imem02_rd = 1;
    4: _imem02_rd = 1;
    3: _imem02_rd = 1;
    2: _imem02_rd = 1;
    1: _imem02_rd = 1;
    0: _imem02_rd = 1;
    26: _imem02_rd = 1;
    25: _imem02_rd = 1;
    24: _imem02_rd = 1;
    23: _imem02_rd = 1;
    22: _imem02_rd = 1;
    21: _imem02_rd = 1;
    20: _imem02_rd = 1;
    19: _imem02_rd = 1;
    18: _imem02_rd = 1;
    17: _imem02_rd = 1;
    16: _imem02_rd = 1;
    15: _imem02_rd = 1;
    default: _imem02_rd = 0;
    endcase
  end // always @ ( * )
  assign imem02_rd = _imem02_rd;

  // 3番目の入力用メモリブロックの制御
  reg [5:0] _imem03_bank;
  always @ ( * ) begin
    case ( state )
    26: _imem03_bank = 0;
    14: _imem03_bank = 1;
    13: _imem03_bank = 2;
    12: _imem03_bank = 6;
    11: _imem03_bank = 7;
    10: _imem03_bank = 9;
    9: _imem03_bank = 10;
    8: _imem03_bank = 11;
    7: _imem03_bank = 12;
    6: _imem03_bank = 13;
    5: _imem03_bank = 15;
    4: _imem03_bank = 16;
    3: _imem03_bank = 17;
    2: _imem03_bank = 19;
    1: _imem03_bank = 20;
    0: _imem03_bank = 23;
    27: _imem03_bank = 28;
    25: _imem03_bank = 30;
    24: _imem03_bank = 31;
    23: _imem03_bank = 39;
    22: _imem03_bank = 40;
    21: _imem03_bank = 41;
    20: _imem03_bank = 44;
    19: _imem03_bank = 45;
    18: _imem03_bank = 46;
    17: _imem03_bank = 48;
    16: _imem03_bank = 50;
    15: _imem03_bank = 51;
    32: _imem03_bank = 55;
    31: _imem03_bank = 56;
    30: _imem03_bank = 57;
    29: _imem03_bank = 58;
    28: _imem03_bank = 59;
    default: _imem03_bank = 0;
    endcase
  end // always @ ( * )
  assign imem03_bank = _imem03_bank;
  reg _imem03_rd;
  always @ ( * ) begin
    case ( state )
    26: _imem03_rd = 1;
    14: _imem03_rd = 1;
    13: _imem03_rd = 1;
    12: _imem03_rd = 1;
    11: _imem03_rd = 1;
    10: _imem03_rd = 1;
    9: _imem03_rd = 1;
    8: _imem03_rd = 1;
    7: _imem03_rd = 1;
    6: _imem03_rd = 1;
    5: _imem03_rd = 1;
    4: _imem03_rd = 1;
    3: _imem03_rd = 1;
    2: _imem03_rd = 1;
    1: _imem03_rd = 1;
    0: _imem03_rd = 1;
    27: _imem03_rd = 1;
    25: _imem03_rd = 1;
    24: _imem03_rd = 1;
    23: _imem03_rd = 1;
    22: _imem03_rd = 1;
    21: _imem03_rd = 1;
    20: _imem03_rd = 1;
    19: _imem03_rd = 1;
    18: _imem03_rd = 1;
    17: _imem03_rd = 1;
    16: _imem03_rd = 1;
    15: _imem03_rd = 1;
    32: _imem03_rd = 1;
    31: _imem03_rd = 1;
    30: _imem03_rd = 1;
    29: _imem03_rd = 1;
    28: _imem03_rd = 1;
    default: _imem03_rd = 0;
    endcase
  end // always @ ( * )
  assign imem03_rd = _imem03_rd;

  // 4番目の入力用メモリブロックの制御
  reg [5:0] _imem04_bank;
  always @ ( * ) begin
    case ( state )
    32: _imem04_bank = 1;
    31: _imem04_bank = 2;
    30: _imem04_bank = 4;
    29: _imem04_bank = 5;
    28: _imem04_bank = 7;
    27: _imem04_bank = 8;
    26: _imem04_bank = 9;
    25: _imem04_bank = 11;
    24: _imem04_bank = 14;
    13: _imem04_bank = 16;
    12: _imem04_bank = 17;
    11: _imem04_bank = 19;
    10: _imem04_bank = 21;
    9: _imem04_bank = 22;
    8: _imem04_bank = 25;
    7: _imem04_bank = 26;
    6: _imem04_bank = 28;
    5: _imem04_bank = 30;
    4: _imem04_bank = 31;
    3: _imem04_bank = 33;
    2: _imem04_bank = 34;
    1: _imem04_bank = 35;
    0: _imem04_bank = 36;
    34: _imem04_bank = 38;
    33: _imem04_bank = 39;
    23: _imem04_bank = 40;
    22: _imem04_bank = 41;
    21: _imem04_bank = 43;
    20: _imem04_bank = 45;
    19: _imem04_bank = 48;
    18: _imem04_bank = 50;
    17: _imem04_bank = 52;
    16: _imem04_bank = 53;
    15: _imem04_bank = 56;
    14: _imem04_bank = 57;
    default: _imem04_bank = 0;
    endcase
  end // always @ ( * )
  assign imem04_bank = _imem04_bank;
  reg _imem04_rd;
  always @ ( * ) begin
    case ( state )
    32: _imem04_rd = 1;
    31: _imem04_rd = 1;
    30: _imem04_rd = 1;
    29: _imem04_rd = 1;
    28: _imem04_rd = 1;
    27: _imem04_rd = 1;
    26: _imem04_rd = 1;
    25: _imem04_rd = 1;
    24: _imem04_rd = 1;
    13: _imem04_rd = 1;
    12: _imem04_rd = 1;
    11: _imem04_rd = 1;
    10: _imem04_rd = 1;
    9: _imem04_rd = 1;
    8: _imem04_rd = 1;
    7: _imem04_rd = 1;
    6: _imem04_rd = 1;
    5: _imem04_rd = 1;
    4: _imem04_rd = 1;
    3: _imem04_rd = 1;
    2: _imem04_rd = 1;
    1: _imem04_rd = 1;
    0: _imem04_rd = 1;
    34: _imem04_rd = 1;
    33: _imem04_rd = 1;
    23: _imem04_rd = 1;
    22: _imem04_rd = 1;
    21: _imem04_rd = 1;
    20: _imem04_rd = 1;
    19: _imem04_rd = 1;
    18: _imem04_rd = 1;
    17: _imem04_rd = 1;
    16: _imem04_rd = 1;
    15: _imem04_rd = 1;
    14: _imem04_rd = 1;
    default: _imem04_rd = 0;
    endcase
  end // always @ ( * )
  assign imem04_rd = _imem04_rd;

  // 0番目の出力用メモリブロックの制御
  reg [-1:0] _omem00_bank;
  always @ ( * ) begin
    case ( state )
    38: _omem00_bank = 0;
    default: _omem00_bank = 0;
    endcase
  end // always @ ( * )
  assign omem00_bank = _omem00_bank;
  reg _omem00_wr;
  always @ ( * ) begin
    case ( state )
    38: _omem00_wr = 1;
    default: _omem00_wr = 0;
    endcase
  end // always @ ( * )
  assign omem00_wr = _omem00_wr;
  reg [13:0] _omem00_out;
  always @ ( * ) begin
    case ( state )
    38: _omem00_out = reg_0000;
    default: _omem00_out = 0;
    endcase
  end // always @ ( * )
  assign omem00_out = _omem00_out[13:0];

  // OP1#0の0番目の入力
  always @ ( * ) begin
    case ( state )
    15: op1_00_in00 = imem00_in[5:0];
    28: op1_00_in00 = imem00_in[5:0];
    29: op1_00_in00 = imem00_in[5:0];
    16: op1_00_in00 = imem01_in[5:0];
    35: op1_00_in00 = imem01_in[5:0];
    34: op1_00_in00 = imem03_in[5:0];
    36: op1_00_in00 = imem04_in[5:0];
    default: op1_00_in00 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の0番目の入力反転
  always @ ( * ) begin
    case ( state )
    15: op1_00_inv00 = 1;
    28: op1_00_inv00 = 1;
    29: op1_00_inv00 = 1;
    16: op1_00_inv00 = 1;
    34: op1_00_inv00 = 1;
    default: op1_00_inv00 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の1番目の入力
  always @ ( * ) begin
    case ( state )
    15: op1_00_in01 = reg_0060;
    28: op1_00_in01 = reg_0050;
    29: op1_00_in01 = imem01_in[5:0];
    16: op1_00_in01 = reg_0067;
    35: op1_00_in01 = reg_0017;
    34: op1_00_in01 = reg_0014;
    36: op1_00_in01 = reg_0024;
    default: op1_00_in01 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の1番目の入力反転
  always @ ( * ) begin
    case ( state )
    15: op1_00_inv01 = 1;
    35: op1_00_inv01 = 1;
    34: op1_00_inv01 = 1;
    36: op1_00_inv01 = 1;
    default: op1_00_inv01 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の2番目の入力
  always @ ( * ) begin
    case ( state )
    15: op1_00_in02 = reg_0055;
    28: op1_00_in02 = reg_0045;
    29: op1_00_in02 = reg_0052;
    16: op1_00_in02 = reg_0062;
    35: op1_00_in02 = reg_0012;
    34: op1_00_in02 = reg_0009;
    36: op1_00_in02 = reg_0041;
    default: op1_00_in02 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の2番目の入力反転
  always @ ( * ) begin
    case ( state )
    29: op1_00_inv02 = 1;
    16: op1_00_inv02 = 1;
    36: op1_00_inv02 = 1;
    default: op1_00_inv02 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の3番目の入力
  always @ ( * ) begin
    case ( state )
    15: op1_00_in03 = reg_0050;
    28: op1_00_in03 = reg_0040;
    29: op1_00_in03 = reg_0047;
    16: op1_00_in03 = reg_0057;
    35: op1_00_in03 = reg_0007;
    34: op1_00_in03 = reg_0004;
    36: op1_00_in03 = reg_0036;
    default: op1_00_in03 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の3番目の入力反転
  always @ ( * ) begin
    case ( state )
    15: op1_00_inv03 = 1;
    28: op1_00_inv03 = 1;
    29: op1_00_inv03 = 1;
    16: op1_00_inv03 = 1;
    35: op1_00_inv03 = 1;
    34: op1_00_inv03 = 1;
    36: op1_00_inv03 = 1;
    default: op1_00_inv03 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の4番目の入力
  always @ ( * ) begin
    case ( state )
    15: op1_00_in04 = reg_0045;
    28: op1_00_in04 = reg_0035;
    29: op1_00_in04 = reg_0042;
    16: op1_00_in04 = reg_0052;
    35: op1_00_in04 = reg_0002;
    34: op1_00_in04 = reg_0054;
    36: op1_00_in04 = reg_0031;
    default: op1_00_in04 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の4番目の入力反転
  always @ ( * ) begin
    case ( state )
    16: op1_00_inv04 = 1;
    35: op1_00_inv04 = 1;
    34: op1_00_inv04 = 1;
    default: op1_00_inv04 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の5番目の入力
  always @ ( * ) begin
    case ( state )
    15: op1_00_in05 = reg_0040;
    28: op1_00_in05 = reg_0030;
    29: op1_00_in05 = reg_0037;
    16: op1_00_in05 = reg_0047;
    35: op1_00_in05 = reg_0067;
    34: op1_00_in05 = imem04_in[5:0];
    36: op1_00_in05 = reg_0026;
    default: op1_00_in05 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の5番目の入力反転
  always @ ( * ) begin
    case ( state )
    28: op1_00_inv05 = 1;
    36: op1_00_inv05 = 1;
    default: op1_00_inv05 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の6番目の入力
  always @ ( * ) begin
    case ( state )
    15: op1_00_in06 = reg_0035;
    28: op1_00_in06 = reg_0025;
    29: op1_00_in06 = reg_0032;
    16: op1_00_in06 = reg_0042;
    35: op1_00_in06 = reg_0065;
    34: op1_00_in06 = reg_0020;
    36: op1_00_in06 = reg_0021;
    default: op1_00_in06 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の6番目の入力反転
  always @ ( * ) begin
    case ( state )
    29: op1_00_inv06 = 1;
    default: op1_00_inv06 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の7番目の入力
  always @ ( * ) begin
    case ( state )
    15: op1_00_in07 = reg_0030;
    28: op1_00_in07 = reg_0020;
    29: op1_00_in07 = reg_0027;
    16: op1_00_in07 = reg_0037;
    35: op1_00_in07 = imem02_in[5:0];
    34: op1_00_in07 = reg_0015;
    36: op1_00_in07 = reg_0016;
    default: op1_00_in07 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の7番目の入力反転
  always @ ( * ) begin
    case ( state )
    15: op1_00_inv07 = 1;
    28: op1_00_inv07 = 1;
    35: op1_00_inv07 = 1;
    36: op1_00_inv07 = 1;
    default: op1_00_inv07 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の8番目の入力
  always @ ( * ) begin
    case ( state )
    15: op1_00_in08 = reg_0025;
    28: op1_00_in08 = reg_0015;
    29: op1_00_in08 = reg_0022;
    16: op1_00_in08 = reg_0032;
    35: op1_00_in08 = reg_0018;
    34: op1_00_in08 = reg_0061;
    36: op1_00_in08 = reg_0011;
    default: op1_00_in08 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の8番目の入力反転
  always @ ( * ) begin
    case ( state )
    15: op1_00_inv08 = 1;
    16: op1_00_inv08 = 1;
    34: op1_00_inv08 = 1;
    36: op1_00_inv08 = 1;
    default: op1_00_inv08 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の9番目の入力
  always @ ( * ) begin
    case ( state )
    15: op1_00_in09 = reg_0020;
    28: op1_00_in09 = reg_0010;
    29: op1_00_in09 = reg_0017;
    16: op1_00_in09 = reg_0027;
    35: op1_00_in09 = reg_0013;
    34: op1_00_in09 = reg_0000;
    36: op1_00_in09 = reg_0006;
    default: op1_00_in09 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の9番目の入力反転
  always @ ( * ) begin
    case ( state )
    15: op1_00_inv09 = 1;
    28: op1_00_inv09 = 1;
    default: op1_00_inv09 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の10番目の入力
  always @ ( * ) begin
    case ( state )
    15: op1_00_in10 = reg_0015;
    28: op1_00_in10 = reg_0005;
    29: op1_00_in10 = reg_0012;
    16: op1_00_in10 = reg_0022;
    35: op1_00_in10 = reg_0008;
    34: op1_00_in10 = reg_0062;
    36: op1_00_in10 = reg_0001;
    default: op1_00_in10 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の10番目の入力反転
  always @ ( * ) begin
    case ( state )
    15: op1_00_inv10 = 1;
    29: op1_00_inv10 = 1;
    16: op1_00_inv10 = 1;
    35: op1_00_inv10 = 1;
    34: op1_00_inv10 = 1;
    36: op1_00_inv10 = 1;
    default: op1_00_inv10 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の11番目の入力
  always @ ( * ) begin
    case ( state )
    15: op1_00_in11 = reg_0010;
    28: op1_00_in11 = reg_0000;
    29: op1_00_in11 = reg_0007;
    16: op1_00_in11 = reg_0017;
    35: op1_00_in11 = reg_0003;
    34: op1_00_in11 = reg_0056;
    36: op1_00_in11 = reg_0074;
    default: op1_00_in11 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の11番目の入力反転
  always @ ( * ) begin
    case ( state )
    default: op1_00_inv11 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の12番目の入力
  always @ ( * ) begin
    case ( state )
    15: op1_00_in12 = reg_0005;
    28: op1_00_in12 = reg_0073;
    29: op1_00_in12 = reg_0002;
    16: op1_00_in12 = reg_0012;
    35: op1_00_in12 = reg_0065;
    34: op1_00_in12 = reg_0051;
    default: op1_00_in12 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の12番目の入力反転
  always @ ( * ) begin
    case ( state )
    28: op1_00_inv12 = 1;
    34: op1_00_inv12 = 1;
    default: op1_00_inv12 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の13番目の入力
  always @ ( * ) begin
    case ( state )
    15: op1_00_in13 = reg_0000;
    28: op1_00_in13 = imem00_in[5:0];
    29: op1_00_in13 = reg_0032;
    16: op1_00_in13 = reg_0007;
    35: op1_00_in13 = reg_0065;
    34: op1_00_in13 = reg_0046;
    default: op1_00_in13 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の13番目の入力反転
  always @ ( * ) begin
    case ( state )
    15: op1_00_inv13 = 1;
    28: op1_00_inv13 = 1;
    29: op1_00_inv13 = 1;
    default: op1_00_inv13 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の14番目の入力
  always @ ( * ) begin
    case ( state )
    15: op1_00_in14 = reg_0040;
    28: op1_00_in14 = reg_0020;
    29: op1_00_in14 = reg_0017;
    16: op1_00_in14 = reg_0002;
    35: op1_00_in14 = imem01_in[5:0];
    34: op1_00_in14 = reg_0004;
    default: op1_00_in14 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の14番目の入力反転
  always @ ( * ) begin
    case ( state )
    28: op1_00_inv14 = 1;
    16: op1_00_inv14 = 1;
    34: op1_00_inv14 = 1;
    default: op1_00_inv14 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の15番目の入力
  always @ ( * ) begin
    case ( state )
    default: op1_00_in15 = 0;
    endcase
  end // always @ ( * )

  // OP1#0の15番目の入力反転
  always @ ( * ) begin
    case ( state )
    default: op1_00_inv15 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の0番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_01_in00 = imem02_in[5:0];
    28: op1_01_in00 = imem02_in[5:0];
    29: op1_01_in00 = imem03_in[5:0];
    15: op1_01_in00 = imem04_in[5:0];
    default: op1_01_in00 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の0番目の入力反転
  always @ ( * ) begin
    case ( state )
    28: op1_01_inv00 = 1;
    29: op1_01_inv00 = 1;
    15: op1_01_inv00 = 1;
    default: op1_01_inv00 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の1番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_01_in01 = reg_0068;
    28: op1_01_in01 = reg_0048;
    29: op1_01_in01 = reg_0049;
    15: op1_01_in01 = reg_0061;
    default: op1_01_in01 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の1番目の入力反転
  always @ ( * ) begin
    case ( state )
    16: op1_01_inv01 = 1;
    default: op1_01_inv01 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の2番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_01_in02 = reg_0063;
    28: op1_01_in02 = reg_0043;
    29: op1_01_in02 = reg_0044;
    15: op1_01_in02 = reg_0056;
    default: op1_01_in02 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の2番目の入力反転
  always @ ( * ) begin
    case ( state )
    28: op1_01_inv02 = 1;
    15: op1_01_inv02 = 1;
    default: op1_01_inv02 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の3番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_01_in03 = reg_0058;
    28: op1_01_in03 = reg_0038;
    29: op1_01_in03 = reg_0039;
    15: op1_01_in03 = reg_0051;
    default: op1_01_in03 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の3番目の入力反転
  always @ ( * ) begin
    case ( state )
    16: op1_01_inv03 = 1;
    29: op1_01_inv03 = 1;
    15: op1_01_inv03 = 1;
    default: op1_01_inv03 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の4番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_01_in04 = reg_0053;
    28: op1_01_in04 = reg_0033;
    29: op1_01_in04 = reg_0034;
    15: op1_01_in04 = reg_0046;
    default: op1_01_in04 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の4番目の入力反転
  always @ ( * ) begin
    case ( state )
    16: op1_01_inv04 = 1;
    default: op1_01_inv04 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の5番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_01_in05 = reg_0048;
    28: op1_01_in05 = reg_0028;
    29: op1_01_in05 = reg_0029;
    15: op1_01_in05 = reg_0041;
    default: op1_01_in05 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の5番目の入力反転
  always @ ( * ) begin
    case ( state )
    16: op1_01_inv05 = 1;
    15: op1_01_inv05 = 1;
    default: op1_01_inv05 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の6番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_01_in06 = reg_0043;
    28: op1_01_in06 = reg_0023;
    29: op1_01_in06 = reg_0024;
    15: op1_01_in06 = reg_0036;
    default: op1_01_in06 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の6番目の入力反転
  always @ ( * ) begin
    case ( state )
    16: op1_01_inv06 = 1;
    28: op1_01_inv06 = 1;
    29: op1_01_inv06 = 1;
    15: op1_01_inv06 = 1;
    default: op1_01_inv06 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の7番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_01_in07 = reg_0038;
    28: op1_01_in07 = reg_0018;
    29: op1_01_in07 = reg_0019;
    15: op1_01_in07 = reg_0031;
    default: op1_01_in07 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の7番目の入力反転
  always @ ( * ) begin
    case ( state )
    16: op1_01_inv07 = 1;
    29: op1_01_inv07 = 1;
    default: op1_01_inv07 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の8番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_01_in08 = reg_0033;
    28: op1_01_in08 = reg_0013;
    29: op1_01_in08 = reg_0014;
    15: op1_01_in08 = reg_0026;
    default: op1_01_in08 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の8番目の入力反転
  always @ ( * ) begin
    case ( state )
    28: op1_01_inv08 = 1;
    default: op1_01_inv08 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の9番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_01_in09 = reg_0028;
    28: op1_01_in09 = reg_0008;
    29: op1_01_in09 = reg_0009;
    15: op1_01_in09 = reg_0021;
    default: op1_01_in09 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の9番目の入力反転
  always @ ( * ) begin
    case ( state )
    16: op1_01_inv09 = 1;
    default: op1_01_inv09 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の10番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_01_in10 = reg_0023;
    28: op1_01_in10 = reg_0003;
    29: op1_01_in10 = reg_0004;
    15: op1_01_in10 = reg_0016;
    default: op1_01_in10 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の10番目の入力反転
  always @ ( * ) begin
    case ( state )
    16: op1_01_inv10 = 1;
    29: op1_01_inv10 = 1;
    default: op1_01_inv10 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の11番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_01_in11 = reg_0018;
    28: op1_01_in11 = reg_0060;
    29: op1_01_in11 = reg_0061;
    15: op1_01_in11 = reg_0011;
    default: op1_01_in11 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の11番目の入力反転
  always @ ( * ) begin
    case ( state )
    16: op1_01_inv11 = 1;
    28: op1_01_inv11 = 1;
    29: op1_01_inv11 = 1;
    default: op1_01_inv11 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の12番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_01_in12 = reg_0013;
    28: op1_01_in12 = imem03_in[5:0];
    29: op1_01_in12 = imem03_in[5:0];
    15: op1_01_in12 = reg_0006;
    default: op1_01_in12 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の12番目の入力反転
  always @ ( * ) begin
    case ( state )
    28: op1_01_inv12 = 1;
    29: op1_01_inv12 = 1;
    default: op1_01_inv12 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の13番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_01_in13 = reg_0008;
    28: op1_01_in13 = reg_0023;
    29: op1_01_in13 = reg_0049;
    15: op1_01_in13 = reg_0001;
    default: op1_01_in13 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の13番目の入力反転
  always @ ( * ) begin
    case ( state )
    16: op1_01_inv13 = 1;
    28: op1_01_inv13 = 1;
    default: op1_01_inv13 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の14番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_01_in14 = reg_0003;
    28: op1_01_in14 = reg_0018;
    29: op1_01_in14 = reg_0024;
    15: op1_01_in14 = reg_0046;
    default: op1_01_in14 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の14番目の入力反転
  always @ ( * ) begin
    case ( state )
    29: op1_01_inv14 = 1;
    default: op1_01_inv14 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の15番目の入力
  always @ ( * ) begin
    case ( state )
    default: op1_01_in15 = 0;
    endcase
  end // always @ ( * )

  // OP1#1の15番目の入力反転
  always @ ( * ) begin
    case ( state )
    default: op1_01_inv15 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の0番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_02_in00 = imem03_in[5:0];
    default: op1_02_in00 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の0番目の入力反転
  always @ ( * ) begin
    case ( state )
    default: op1_02_inv00 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の1番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_02_in01 = reg_0069;
    default: op1_02_in01 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の1番目の入力反転
  always @ ( * ) begin
    case ( state )
    default: op1_02_inv01 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の2番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_02_in02 = reg_0064;
    default: op1_02_in02 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の2番目の入力反転
  always @ ( * ) begin
    case ( state )
    default: op1_02_inv02 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の3番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_02_in03 = reg_0059;
    default: op1_02_in03 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の3番目の入力反転
  always @ ( * ) begin
    case ( state )
    default: op1_02_inv03 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の4番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_02_in04 = reg_0054;
    default: op1_02_in04 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の4番目の入力反転
  always @ ( * ) begin
    case ( state )
    default: op1_02_inv04 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の5番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_02_in05 = reg_0049;
    default: op1_02_in05 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の5番目の入力反転
  always @ ( * ) begin
    case ( state )
    16: op1_02_inv05 = 1;
    default: op1_02_inv05 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の6番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_02_in06 = reg_0044;
    default: op1_02_in06 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の6番目の入力反転
  always @ ( * ) begin
    case ( state )
    16: op1_02_inv06 = 1;
    default: op1_02_inv06 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の7番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_02_in07 = reg_0039;
    default: op1_02_in07 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の7番目の入力反転
  always @ ( * ) begin
    case ( state )
    default: op1_02_inv07 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の8番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_02_in08 = reg_0034;
    default: op1_02_in08 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の8番目の入力反転
  always @ ( * ) begin
    case ( state )
    default: op1_02_inv08 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の9番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_02_in09 = reg_0029;
    default: op1_02_in09 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の9番目の入力反転
  always @ ( * ) begin
    case ( state )
    16: op1_02_inv09 = 1;
    default: op1_02_inv09 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の10番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_02_in10 = reg_0024;
    default: op1_02_in10 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の10番目の入力反転
  always @ ( * ) begin
    case ( state )
    16: op1_02_inv10 = 1;
    default: op1_02_inv10 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の11番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_02_in11 = reg_0019;
    default: op1_02_in11 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の11番目の入力反転
  always @ ( * ) begin
    case ( state )
    16: op1_02_inv11 = 1;
    default: op1_02_inv11 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の12番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_02_in12 = reg_0014;
    default: op1_02_in12 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の12番目の入力反転
  always @ ( * ) begin
    case ( state )
    default: op1_02_inv12 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の13番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_02_in13 = reg_0009;
    default: op1_02_in13 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の13番目の入力反転
  always @ ( * ) begin
    case ( state )
    default: op1_02_inv13 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の14番目の入力
  always @ ( * ) begin
    case ( state )
    16: op1_02_in14 = reg_0004;
    default: op1_02_in14 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の14番目の入力反転
  always @ ( * ) begin
    case ( state )
    default: op1_02_inv14 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の15番目の入力
  always @ ( * ) begin
    case ( state )
    default: op1_02_in15 = 0;
    endcase
  end // always @ ( * )

  // OP1#2の15番目の入力反転
  always @ ( * ) begin
    case ( state )
    default: op1_02_inv15 = 0;
    endcase
  end // always @ ( * )

  // OP2#0の0番目の入力
  always @ ( * ) begin
    case ( state )
    37: op2_00_in00 = reg_0075;
    default: op2_00_in00 = 0;
    endcase
  end // always @ ( * )

  // OP2#0の1番目の入力
  always @ ( * ) begin
    case ( state )
    37: op2_00_in01 = reg_0063;
    default: op2_00_in01 = 0;
    endcase
  end // always @ ( * )

  // OP2#0の2番目の入力
  always @ ( * ) begin
    case ( state )
    37: op2_00_in02 = reg_0005;
    default: op2_00_in02 = 0;
    endcase
  end // always @ ( * )

  // OP2#0の3番目の入力
  always @ ( * ) begin
    case ( state )
    37: op2_00_in03 = reg_0066;
    default: op2_00_in03 = 0;
    endcase
  end // always @ ( * )

  // OP2#0の4番目の入力
  always @ ( * ) begin
    case ( state )
    37: op2_00_in04 = reg_0004;
    default: op2_00_in04 = 0;
    endcase
  end // always @ ( * )

  // OP2#0の5番目の入力
  always @ ( * ) begin
    case ( state )
    37: op2_00_in05 = reg_0077;
    default: op2_00_in05 = 0;
    endcase
  end // always @ ( * )

  // OP2#0の6番目の入力
  always @ ( * ) begin
    case ( state )
    37: op2_00_in06 = reg_0064;
    default: op2_00_in06 = 0;
    endcase
  end // always @ ( * )

  // OP2#0の7番目の入力
  always @ ( * ) begin
    case ( state )
    37: op2_00_in07 = reg_0078;
    default: op2_00_in07 = 0;
    endcase
  end // always @ ( * )

  // OP2#0の8番目の入力
  always @ ( * ) begin
    case ( state )
    37: op2_00_in08 = reg_0010;
    default: op2_00_in08 = 0;
    endcase
  end // always @ ( * )

  // OP2#0の9番目の入力
  always @ ( * ) begin
    case ( state )
    37: op2_00_in09 = reg_0025;
    default: op2_00_in09 = 0;
    endcase
  end // always @ ( * )

  // OP2#0の10番目の入力
  always @ ( * ) begin
    case ( state )
    37: op2_00_in10 = reg_0076;
    default: op2_00_in10 = 0;
    endcase
  end // always @ ( * )

  // OP2#0の11番目の入力
  always @ ( * ) begin
    case ( state )
    37: op2_00_in11 = reg_0002;
    default: op2_00_in11 = 0;
    endcase
  end // always @ ( * )

  // OP2#0の12番目の入力
  always @ ( * ) begin
    case ( state )
    default: op2_00_in12 = 0;
    endcase
  end // always @ ( * )

  // OP2#0の13番目の入力
  always @ ( * ) begin
    case ( state )
    default: op2_00_in13 = 0;
    endcase
  end // always @ ( * )

  // OP2#0の14番目の入力
  always @ ( * ) begin
    case ( state )
    default: op2_00_in14 = 0;
    endcase
  end // always @ ( * )

  // OP2#0のバイアス入力
  always @ ( * ) begin
    case ( state )
    37: op2_00_bias = 84;
    default: op2_00_bias = 0;
    endcase
  end // always @ ( * )

  // REG#0の入力
  always @ ( posedge clock ) begin
    case ( state )
    2: reg_0000 <= imem00_in[5:0];
    17: reg_0000 <= imem00_in[5:0];
    30: reg_0000 <= imem04_in[5:0];
    36: reg_0000 <= imem04_in[5:0];
    37: reg_0000 <= op2_00_out;
    endcase
  end

  // REG#1の入力
  always @ ( posedge clock ) begin
    case ( state )
    2: reg_0001 <= imem04_in[5:0];
    17: reg_0001 <= imem04_in[5:0];
    endcase
  end

  // REG#2の入力
  always @ ( posedge clock ) begin
    case ( state )
    2: reg_0002 <= imem01_in[5:0];
    18: reg_0002 <= imem01_in[5:0];
    31: reg_0002 <= imem01_in[5:0];
    36: reg_0002 <= op1_00_out;
    endcase
  end

  // REG#3の入力
  always @ ( posedge clock ) begin
    case ( state )
    2: reg_0003 <= imem02_in[5:0];
    18: reg_0003 <= imem02_in[5:0];
    31: reg_0003 <= imem02_in[5:0];
    endcase
  end

  // REG#4の入力
  always @ ( posedge clock ) begin
    case ( state )
    2: reg_0004 <= imem03_in[5:0];
    18: reg_0004 <= imem03_in[5:0];
    31: reg_0004 <= imem03_in[5:0];
    35: reg_0004 <= op1_00_out;
    endcase
  end

  // REG#5の入力
  always @ ( posedge clock ) begin
    case ( state )
    3: reg_0005 <= imem00_in[5:0];
    18: reg_0005 <= imem00_in[5:0];
    29: reg_0005 <= op1_00_out;
    endcase
  end

  // REG#6の入力
  always @ ( posedge clock ) begin
    case ( state )
    3: reg_0006 <= imem04_in[5:0];
    18: reg_0006 <= imem04_in[5:0];
    endcase
  end

  // REG#7の入力
  always @ ( posedge clock ) begin
    case ( state )
    3: reg_0007 <= imem01_in[5:0];
    19: reg_0007 <= imem01_in[5:0];
    32: reg_0007 <= imem01_in[5:0];
    endcase
  end

  // REG#8の入力
  always @ ( posedge clock ) begin
    case ( state )
    3: reg_0008 <= imem02_in[5:0];
    19: reg_0008 <= imem02_in[5:0];
    32: reg_0008 <= imem02_in[5:0];
    endcase
  end

  // REG#9の入力
  always @ ( posedge clock ) begin
    case ( state )
    3: reg_0009 <= imem03_in[5:0];
    19: reg_0009 <= imem03_in[5:0];
    32: reg_0009 <= imem03_in[5:0];
    endcase
  end

  // REG#10の入力
  always @ ( posedge clock ) begin
    case ( state )
    4: reg_0010 <= imem00_in[5:0];
    19: reg_0010 <= imem00_in[5:0];
    29: reg_0010 <= op1_01_out;
    endcase
  end

  // REG#11の入力
  always @ ( posedge clock ) begin
    case ( state )
    4: reg_0011 <= imem04_in[5:0];
    19: reg_0011 <= imem04_in[5:0];
    endcase
  end

  // REG#12の入力
  always @ ( posedge clock ) begin
    case ( state )
    4: reg_0012 <= imem01_in[5:0];
    20: reg_0012 <= imem01_in[5:0];
    33: reg_0012 <= imem01_in[5:0];
    endcase
  end

  // REG#13の入力
  always @ ( posedge clock ) begin
    case ( state )
    4: reg_0013 <= imem02_in[5:0];
    20: reg_0013 <= imem02_in[5:0];
    33: reg_0013 <= imem02_in[5:0];
    endcase
  end

  // REG#14の入力
  always @ ( posedge clock ) begin
    case ( state )
    4: reg_0014 <= imem03_in[5:0];
    20: reg_0014 <= imem03_in[5:0];
    33: reg_0014 <= imem03_in[5:0];
    endcase
  end

  // REG#15の入力
  always @ ( posedge clock ) begin
    case ( state )
    5: reg_0015 <= imem00_in[5:0];
    20: reg_0015 <= imem00_in[5:0];
    32: reg_0015 <= imem04_in[5:0];
    endcase
  end

  // REG#16の入力
  always @ ( posedge clock ) begin
    case ( state )
    5: reg_0016 <= imem04_in[5:0];
    20: reg_0016 <= imem04_in[5:0];
    endcase
  end

  // REG#17の入力
  always @ ( posedge clock ) begin
    case ( state )
    5: reg_0017 <= imem01_in[5:0];
    21: reg_0017 <= imem01_in[5:0];
    34: reg_0017 <= imem01_in[5:0];
    endcase
  end

  // REG#18の入力
  always @ ( posedge clock ) begin
    case ( state )
    5: reg_0018 <= imem02_in[5:0];
    21: reg_0018 <= imem02_in[5:0];
    34: reg_0018 <= imem02_in[5:0];
    endcase
  end

  // REG#19の入力
  always @ ( posedge clock ) begin
    case ( state )
    5: reg_0019 <= imem03_in[5:0];
    21: reg_0019 <= imem03_in[5:0];
    34: reg_0019 <= imem03_in[5:0];
    endcase
  end

  // REG#20の入力
  always @ ( posedge clock ) begin
    case ( state )
    6: reg_0020 <= imem00_in[5:0];
    21: reg_0020 <= imem00_in[5:0];
    33: reg_0020 <= imem04_in[5:0];
    endcase
  end

  // REG#21の入力
  always @ ( posedge clock ) begin
    case ( state )
    6: reg_0021 <= imem04_in[5:0];
    21: reg_0021 <= imem04_in[5:0];
    endcase
  end

  // REG#22の入力
  always @ ( posedge clock ) begin
    case ( state )
    6: reg_0022 <= imem01_in[5:0];
    22: reg_0022 <= imem01_in[5:0];
    34: reg_0022 <= imem04_in[5:0];
    endcase
  end

  // REG#23の入力
  always @ ( posedge clock ) begin
    case ( state )
    6: reg_0023 <= imem02_in[5:0];
    22: reg_0023 <= imem02_in[5:0];
    35: reg_0023 <= imem02_in[5:0];
    endcase
  end

  // REG#24の入力
  always @ ( posedge clock ) begin
    case ( state )
    6: reg_0024 <= imem03_in[5:0];
    22: reg_0024 <= imem03_in[5:0];
    35: reg_0024 <= imem04_in[5:0];
    endcase
  end

  // REG#25の入力
  always @ ( posedge clock ) begin
    case ( state )
    7: reg_0025 <= imem00_in[5:0];
    22: reg_0025 <= imem00_in[5:0];
    34: reg_0025 <= op1_00_out;
    endcase
  end

  // REG#26の入力
  always @ ( posedge clock ) begin
    case ( state )
    7: reg_0026 <= imem04_in[5:0];
    22: reg_0026 <= imem04_in[5:0];
    endcase
  end

  // REG#27の入力
  always @ ( posedge clock ) begin
    case ( state )
    7: reg_0027 <= imem01_in[5:0];
    23: reg_0027 <= imem01_in[5:0];
    35: reg_0027 <= imem01_in[5:0];
    endcase
  end

  // REG#28の入力
  always @ ( posedge clock ) begin
    case ( state )
    7: reg_0028 <= imem02_in[5:0];
    23: reg_0028 <= imem02_in[5:0];
    endcase
  end

  // REG#29の入力
  always @ ( posedge clock ) begin
    case ( state )
    7: reg_0029 <= imem03_in[5:0];
    23: reg_0029 <= imem03_in[5:0];
    endcase
  end

  // REG#30の入力
  always @ ( posedge clock ) begin
    case ( state )
    8: reg_0030 <= imem00_in[5:0];
    23: reg_0030 <= imem00_in[5:0];
    endcase
  end

  // REG#31の入力
  always @ ( posedge clock ) begin
    case ( state )
    8: reg_0031 <= imem04_in[5:0];
    23: reg_0031 <= imem04_in[5:0];
    endcase
  end

  // REG#32の入力
  always @ ( posedge clock ) begin
    case ( state )
    8: reg_0032 <= imem01_in[5:0];
    24: reg_0032 <= imem01_in[5:0];
    endcase
  end

  // REG#33の入力
  always @ ( posedge clock ) begin
    case ( state )
    8: reg_0033 <= imem02_in[5:0];
    24: reg_0033 <= imem02_in[5:0];
    endcase
  end

  // REG#34の入力
  always @ ( posedge clock ) begin
    case ( state )
    8: reg_0034 <= imem03_in[5:0];
    24: reg_0034 <= imem03_in[5:0];
    endcase
  end

  // REG#35の入力
  always @ ( posedge clock ) begin
    case ( state )
    9: reg_0035 <= imem00_in[5:0];
    24: reg_0035 <= imem00_in[5:0];
    endcase
  end

  // REG#36の入力
  always @ ( posedge clock ) begin
    case ( state )
    9: reg_0036 <= imem04_in[5:0];
    24: reg_0036 <= imem04_in[5:0];
    endcase
  end

  // REG#37の入力
  always @ ( posedge clock ) begin
    case ( state )
    9: reg_0037 <= imem01_in[5:0];
    25: reg_0037 <= imem01_in[5:0];
    endcase
  end

  // REG#38の入力
  always @ ( posedge clock ) begin
    case ( state )
    9: reg_0038 <= imem02_in[5:0];
    25: reg_0038 <= imem02_in[5:0];
    endcase
  end

  // REG#39の入力
  always @ ( posedge clock ) begin
    case ( state )
    9: reg_0039 <= imem03_in[5:0];
    25: reg_0039 <= imem03_in[5:0];
    endcase
  end

  // REG#40の入力
  always @ ( posedge clock ) begin
    case ( state )
    10: reg_0040 <= imem00_in[5:0];
    25: reg_0040 <= imem00_in[5:0];
    endcase
  end

  // REG#41の入力
  always @ ( posedge clock ) begin
    case ( state )
    10: reg_0041 <= imem04_in[5:0];
    25: reg_0041 <= imem04_in[5:0];
    endcase
  end

  // REG#42の入力
  always @ ( posedge clock ) begin
    case ( state )
    10: reg_0042 <= imem01_in[5:0];
    26: reg_0042 <= imem01_in[5:0];
    endcase
  end

  // REG#43の入力
  always @ ( posedge clock ) begin
    case ( state )
    10: reg_0043 <= imem02_in[5:0];
    26: reg_0043 <= imem02_in[5:0];
    endcase
  end

  // REG#44の入力
  always @ ( posedge clock ) begin
    case ( state )
    10: reg_0044 <= imem03_in[5:0];
    26: reg_0044 <= imem03_in[5:0];
    endcase
  end

  // REG#45の入力
  always @ ( posedge clock ) begin
    case ( state )
    11: reg_0045 <= imem00_in[5:0];
    26: reg_0045 <= imem00_in[5:0];
    endcase
  end

  // REG#46の入力
  always @ ( posedge clock ) begin
    case ( state )
    11: reg_0046 <= imem04_in[5:0];
    26: reg_0046 <= imem04_in[5:0];
    endcase
  end

  // REG#47の入力
  always @ ( posedge clock ) begin
    case ( state )
    11: reg_0047 <= imem01_in[5:0];
    27: reg_0047 <= imem01_in[5:0];
    endcase
  end

  // REG#48の入力
  always @ ( posedge clock ) begin
    case ( state )
    11: reg_0048 <= imem02_in[5:0];
    27: reg_0048 <= imem02_in[5:0];
    endcase
  end

  // REG#49の入力
  always @ ( posedge clock ) begin
    case ( state )
    11: reg_0049 <= imem03_in[5:0];
    27: reg_0049 <= imem03_in[5:0];
    endcase
  end

  // REG#50の入力
  always @ ( posedge clock ) begin
    case ( state )
    12: reg_0050 <= imem00_in[5:0];
    27: reg_0050 <= imem00_in[5:0];
    endcase
  end

  // REG#51の入力
  always @ ( posedge clock ) begin
    case ( state )
    12: reg_0051 <= imem04_in[5:0];
    27: reg_0051 <= imem04_in[5:0];
    endcase
  end

  // REG#52の入力
  always @ ( posedge clock ) begin
    case ( state )
    12: reg_0052 <= imem01_in[5:0];
    28: reg_0052 <= imem01_in[5:0];
    endcase
  end

  // REG#53の入力
  always @ ( posedge clock ) begin
    case ( state )
    12: reg_0053 <= imem02_in[5:0];
    28: reg_0053 <= imem02_in[5:0];
    endcase
  end

  // REG#54の入力
  always @ ( posedge clock ) begin
    case ( state )
    12: reg_0054 <= imem03_in[5:0];
    28: reg_0054 <= imem03_in[5:0];
    30: reg_0054 <= imem03_in[5:0];
    endcase
  end

  // REG#55の入力
  always @ ( posedge clock ) begin
    case ( state )
    13: reg_0055 <= imem00_in[5:0];
    28: reg_0055 <= imem00_in[5:0];
    endcase
  end

  // REG#56の入力
  always @ ( posedge clock ) begin
    case ( state )
    13: reg_0056 <= imem04_in[5:0];
    28: reg_0056 <= imem04_in[5:0];
    endcase
  end

  // REG#57の入力
  always @ ( posedge clock ) begin
    case ( state )
    13: reg_0057 <= imem01_in[5:0];
    29: reg_0057 <= imem01_in[5:0];
    endcase
  end

  // REG#58の入力
  always @ ( posedge clock ) begin
    case ( state )
    13: reg_0058 <= imem02_in[5:0];
    29: reg_0058 <= imem00_in[5:0];
    endcase
  end

  // REG#59の入力
  always @ ( posedge clock ) begin
    case ( state )
    13: reg_0059 <= imem03_in[5:0];
    29: reg_0059 <= imem03_in[5:0];
    endcase
  end

  // REG#60の入力
  always @ ( posedge clock ) begin
    case ( state )
    14: reg_0060 <= imem00_in[5:0];
    17: reg_0060 <= imem02_in[5:0];
    endcase
  end

  // REG#61の入力
  always @ ( posedge clock ) begin
    case ( state )
    14: reg_0061 <= imem04_in[5:0];
    17: reg_0061 <= imem03_in[5:0];
    31: reg_0061 <= imem04_in[5:0];
    endcase
  end

  // REG#62の入力
  always @ ( posedge clock ) begin
    case ( state )
    14: reg_0062 <= imem01_in[5:0];
    29: reg_0062 <= imem04_in[5:0];
    endcase
  end

  // REG#63の入力
  always @ ( posedge clock ) begin
    case ( state )
    14: reg_0063 <= imem02_in[5:0];
    28: reg_0063 <= op1_00_out;
    endcase
  end

  // REG#64の入力
  always @ ( posedge clock ) begin
    case ( state )
    14: reg_0064 <= imem03_in[5:0];
    28: reg_0064 <= op1_01_out;
    endcase
  end

  // REG#65の入力
  always @ ( posedge clock ) begin
    case ( state )
    15: reg_0065 <= imem00_in[5:0];
    17: reg_0065 <= imem01_in[5:0];
    endcase
  end

  // REG#66の入力
  always @ ( posedge clock ) begin
    case ( state )
    15: reg_0066 <= imem04_in[5:0];
    16: reg_0066 <= op1_00_out;
    endcase
  end

  // REG#67の入力
  always @ ( posedge clock ) begin
    case ( state )
    15: reg_0067 <= imem01_in[5:0];
    30: reg_0067 <= imem01_in[5:0];
    endcase
  end

  // REG#68の入力
  always @ ( posedge clock ) begin
    case ( state )
    15: reg_0068 <= imem02_in[5:0];
    endcase
  end

  // REG#69の入力
  always @ ( posedge clock ) begin
    case ( state )
    15: reg_0069 <= imem03_in[5:0];
    endcase
  end

  // REG#70の入力
  always @ ( posedge clock ) begin
    case ( state )
    16: reg_0070 <= imem01_in[5:0];
    endcase
  end

  // REG#71の入力
  always @ ( posedge clock ) begin
    case ( state )
    16: reg_0071 <= imem02_in[5:0];
    endcase
  end

  // REG#72の入力
  always @ ( posedge clock ) begin
    case ( state )
    16: reg_0072 <= imem03_in[5:0];
    endcase
  end

  // REG#73の入力
  always @ ( posedge clock ) begin
    case ( state )
    16: reg_0073 <= imem00_in[5:0];
    endcase
  end

  // REG#74の入力
  always @ ( posedge clock ) begin
    case ( state )
    16: reg_0074 <= imem04_in[5:0];
    endcase
  end

  // REG#75の入力
  always @ ( posedge clock ) begin
    case ( state )
    15: reg_0075 <= op1_00_out;
    endcase
  end

  // REG#76の入力
  always @ ( posedge clock ) begin
    case ( state )
    15: reg_0076 <= op1_01_out;
    endcase
  end

  // REG#77の入力
  always @ ( posedge clock ) begin
    case ( state )
    16: reg_0077 <= op1_01_out;
    endcase
  end

  // REG#78の入力
  always @ ( posedge clock ) begin
    case ( state )
    16: reg_0078 <= op1_02_out;
    endcase
  end
endmodule
