# アフィン変換回路生成器

<div style="text-align:right;">
松永 裕介<br>
2020.10.15 Ver.1<bt>
</div>


## はじめに

deep learning では入力信号を複数の演算層で処理した結果を出力するが，
その各層で行われる主要な処理の一つにアフィン変換(Affine
transformation)がある．
定義上，アフィン変換層ではすべての入力信号がすべての出力信号に関係していることなる（そのため「全結合層」の別名を持つ）が，
実際にはアフィン変換行列が非常に疎な場合が多い．
その場合，単純に行列演算の定義に従って全要素の演算を網羅的に行うのは効率が悪い．
そこで，与えられたデータに合わせて専用のアフィン変換を行うハードウェアを合成するプログラムを開発する．


## アフィン変換

アフィン変換は以下の式で表される

Y = A・X

ここで A はアフィン変換行列，Xは入力信号(ベクトル)，Yは出力信号(ベクトル)である．
上の式を展開すると以下のようになる．

Y<sub>i</sub> = Σ<sub>j</sub> A<sub>ij</sub>・X<sub>j</sub>

ここで A_{ij} はAのi行i列の要素を表す．
行列のサイズをm行n列とすると上の式では m × n 回の乗算と加算を行う必要がある．
ただし，A<sub>ij</sub>が0の場合，この項に関する演算は無意味であり省略できる．
さらに今回はA<sub>ij</sub>の値の種類も 0.125, 0.25, -0.125
の３種類のみと限定された場合を考える．
0.125 は 1/8 であり2進数を3ビット右シフトすることで実現できる．
0.25 は 0.25 の2倍であり，同じ値を2回加算することで実現できる．
-0.125 は 0.125 にマイナスを掛けたものなので，
最終結果を3ビット右シフトすることで1/8倍するとすると，
この例のアフィン変換では係数の乗算は必要なく，
加算と2回の加算と減算だけで実現できる．


## Data Flow Graph

ここでは実現する演算を表すために Data Flow Graph(DFG) を用いる．
DFGは計算構造を表す非巡回有向グラフ(DAG)である．
DFGのノードは以下の3種類からなる．
* 入力ノード(入力メモリノード)
  入力値(を納めたメモリのアドレス)を表す．
  入力メモリからの読み出し動作を行う．
* 演算ノード
  計算を表す．
* 出力ノード(出力メモリノード)
  計算結果(を格納するメモリのアドレス)を表す．
  結果を出力メモリに書き出す動作を行う．


## スケジューリングとバインディング

単純にはDFGの演算ノードを一つずつ実際の演算器ハードウェアに割り当てるとDFGの計算を行うハードウェアを実現することができる．
しかし，ノード数が多い場合，ノード数と等しい個数の演算器を用意することは現実的ではない．
そこで，計算の実行を複数クロックに分割して一つの演算器を複数のノードで時分割で共有することで使用する演算器の個数を減らす方法が考えられる．
一般に実行クロック数を増やせばより多くの演算ノードが共有可能となるが，
具体的には個々の演算ノードがどのタイミングで実行されるかがわからないと共有可能かどうかはわからない．
そこで，DFGの各ノードの実行タイミングを決定する処理を「スケジューリング」とよぶ．

スケジューリングが決まるとDFGの実行にかかるクロック数(ステップ数)と必要になる演算器の個数(の最小値)が決定される．
しかし，演算器の共有を行うためには入力や出力の切り替えを行うハードウェア(セレクタ，もしくはマルチプレクサ)が必要となる．
また，演算に用いる値が1クロック以上前のクロックで生成されていた場合，
その値を保存しておくためのレジスタが必要となる．
これらの付加的なハードウェアは，
実際にどのノードを共有するかを決めなければ決まらない．
この処理を「バインディング」と呼ぶ．

スケジューリングもバインディングも単純に決められるものではなく様々な方法が考えられる．
さらにスケジューリング・バインディング結果に応じて計算ステップ数と必要となるハードウェア量が変わってくるため，
適切な方法を選ぶ必要がある．


## 具体例

`data/Affine_W.op`

の例について説明する．

このファイルは1行で1つの出力に関する計算式を表している．
ただし，`#`で始まる行はコメントであり無視される．
例えば最初の行は以下のようになっている．

```
0: (15, 0.125), (70, -0.125), (87, -0.125), ・・・
```

最初の`0:` はこの行が0番目の出力のものであることを示している．
その後につづく`(15, 0.125)`は15番目の入力に係数 0.125 を掛けることを表している．
以下同様である．
係数0の項は省略されている．
先頭のコメントに書いてあるようにこの例では入力のサイズは 1536，
出力のサイズは 1000 である．
そのため仮想的には 1,536,000 の演算が必要であるが，
実際には


## 基本演算

上記の例で用いられている係数は 0.125, -0.125, 0.25 の3種類のみである．
そこで，最終結果を1/8する(3ビット右シフト)することにすれば，
各係数はそれぞれ1, -1, 2となる．
-1を掛けるということは「2の補数」を求めることに他ならない．
2の補数はもとの2進数の0と1を反転させた結果に1を足せばよい．
2倍するのは左に1ビットシフトすればよいが，
値がオーバーフローする可能性があるので，
同じ入力を2回足すことにする．
すると係数を乗算する回路はほぼ不要となり加算回路のみあればよいことになる(2の補数の1を足す部分も含む)．
さらに，加算は1度に2つの数を足し合わせるよりも複数の数を足し合わせるほうが効率がよい．
そこで今回は16入力の加算器を基本演算器として用いることとする．
今回の例では1つの出力に対する最大の入力数は200程度なので，
16入力の加算器を2段組み合わせることで対応する．
すると16 × 16 = 256 入力まで対応可能である．
この例ではこの16入力加算器を基本演算とする．


## 演算器のビット幅

今回の例では入力データは8ビット幅で与えられる．
基本的に8ビットどうしの加算の結果を誤差なく表すためには9ビット必要となる．
同様に8ビットの入力を16個同時に足し合わせる場合結果は12ビット必要となる．

すると2段めの16入力加算器は入力が12ビット，出力が16ビットとなる．
そのため，16入力加算器は1段めと2段めで異なるビット幅のものを用意する必要がある．


## 前処理

前述のように入力データはグループ化されておらずバラバラに与えられる．
そのため16入力加算器を基本演算としたDFGを作るためには，
入力データを最大16入力の加算ノードに分割する必要がある．
どの入力を同じグループにするかによって最終的な結果が変わってくるが，
現在はどのようなグループ化がよいのかを表すよい指標が思いつかないので適当に分割することとする．
余裕があればこのグループ化の方法も検討課題である．


## スケジューリング

DFG が出来上がったらスケジューリングを行う．
