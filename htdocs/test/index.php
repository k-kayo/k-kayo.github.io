<?php
// HTMLの出力
echo 'おはようございます';

$str = 'こんにちは';

?>

<br>

<?php echo $str ?>、山田太郎さん。
<!-- 👇上が省略されたものがしたのやつ -->
<?= $str ?>、山田太郎さん。
<!-- 👆単純にechoする場合はは上の記述で良い -->

<br>

<?php
$name = 'ケンシロウ';
$name = 'ラオウ';
echo $name;
?>
<br>


<?php
define('NAME', 'ケンシロウ');
// define('NAME', 'ラオウ');　再定義は出来ない
?>

<br>

<!-- 【phpの情報を出力出来る関数】 -->
<!-- <?php
			// phpinfo();
			?> -->

<?php

$one = '今日の天気は';
$two = '晴れです';
echo $one . $two;

?>

<!-- <?php
			echo "{$one} 曇りです";
			?> -->

<br>

<?php
echo '私の流派は北斗神拳です', "\n"; // \nは改行
echo "私の流派は南斗聖拳です";
?>

<br>

<?php
$test = '文字列数の確認';
echo strlen($test);
// 15  日本語のバイト数によるものです（Unicodeでは1文字3バイト扱い）
echo mb_strlen($test);
// 15  日本語の文字数を正しくカウントする場合は`mb_strlen`関数を使いましょう。
?>

<?php

$pear = '梨には和梨と洋梨があります';
$pear_replaced = str_replace('梨', '🍐', $pear);
echo $pear_replaced;
?>

<br>

<?php
$colors = ['赤', '青', '青', '黄'];
// echo $colors;
// print_r($colors);
$colors[2] = '紫';
$colors[] = '橙'; // 👈末尾に追加される
array_push($colors, '茶', '白'); //  沢山追加する時は使うと楽
?>
<br>

<pre><?php print_r($colors); ?></pre>
<!-- ↑改行してくれる？ -->
<br>

<?php
$fruits1 = ['バナナ', '梨', '桃'];
$fruits2 = ['さくらんぼ', 'ブドウ'];
$fruits_merged = array_merge($fruits1, $fruits2);
print_r($fruits_merged);
?>
<!-- →Array ( [0] => バナナ [1] => 梨 [2] => 桃 [3] => さくらんぼ [4] => ブドウ ) -->

<br>


<?php
echo count($fruits_merged);  //→5
?>

<br>

<?php
echo count($fruits_merged);
array_pop($fruits_merged);
print_r($fruits_merged);
?>
<!-- →5 -->
<!-- Array ( [0] => バナナ [1] => 梨 [2] => 桃 [3] => さくらんぼ ) -->
<br>

<!--------2/14   07，配列の途中まで ----------->

<!------------------ 2/15 講義分------------------------------->

<?php
$ages = [
	'kenshiro' => 18,
	'bat' => 10,
	'rin' => 7,
];

// $ages['kenshiro'] => 19,

print_r($ages);
echo $ages['bat'];
?>
<br>

<!-- 連想配列の場合 👇-->
<?php
$game_machines = [
	['name' => 'ファミリーコンピューター', 'brand' => '任天堂', 'year' => 1983],
	['name' => 'メガドライブ', 'brand' => 'セガ', 'year' => 1988],
	['name' => 'ネオジオ', 'brand' => 'SNK', 'year' => 1990],
];

echo $game_machines[0]['name'];

// 多次元配列へのデータの追加👇
$game_machines[] = [
	'name' => 'PlayStation',
	'brand' => 'SONY',
	'year' => 1994,
];

?>

<br>
<!-- For文 -->
<?php
for ($i = 0; $i < count($game_machines); $i++) {
	echo $game_machines[$i]['name'] . '<br>';
}
?>

<br>

<?php
$names = ['ケンシロウ', 'ラオウ', 'レイ'];

for ($i = 0; $i < count($names); $i++) {
	echo $names[$i];
}
?>

<br>

<!-- Foreach文 -->
<?php
$names = ['ケンシロウ', 'ラオウ', 'レイ'];

foreach ($names as $name) {
	echo $name . '<br>';
}
?>
<br>

<?php
$machines = [
	['name' => 'ファミリーコンピューター', 'brand' => '任天堂', 'year' => 1983],
	['name' => 'メガドライブ', 'brand' => 'セガ', 'year' => 1988],
	['name' => 'ネオジオ', 'brand' => 'SNK', 'year' => 1990],
];

foreach ($machines as $machine) {
	echo "{$machine['name']} - {$machine['brand']} ({$machine['year']})<br>";
}
?>

<br>

<!-- While文 -->
<?php
$machines = [
	['name' => 'ファミリーコンピューター', 'brand' => '任天堂', 'year' => 1983],
	['name' => 'メガドライブ', 'brand' => 'snk', 'year' => 1988],
	['name' => 'ネオジオ', 'brand' => 'snk', 'year' => 1990],
];

$i = 0; //初期化式
while ($i < count($machines)) { //繰り返し条件//
	echo $machines[$i]['name'] . " - {$machines[$i]['brand']} " . "({$machines[$i]['year']})<br>";
	$i++; //更新処理
}
?>
<!-- while文の場合は上記の例のように繰り返しの処理を分けて記述します。 -->

<br>

<!-- HTML内での繰り返し処理 -->
<h1>繰り返し処理テスト（foreach）</h1>
<ul>
	<?php foreach ($game_machines as $game_machine) : ?>
		<li><?= $machine['name']; ?></li>
	<?php endforeach; ?>
</ul>

<br>

<!-- 10 ブーリアンと比較 -->
<!-- 比較演算とブール値 -->
<?php
echo true; // 1
echo false; // "" 
var_dump(true);
var_dump(false);
var_dump(12);
var_dump(['赤’, ’青', '黄']);
?>

<br>

<!-- 11 条件分岐と論理演算 -->

<!-- 12 Continue と Break -->

<?php
$fruits = [
	['name' => 'りんご', 'price' => 100],
	['name' => 'なし', 'price' => 120],
	['name' => 'みかん', 'price' => 90],
];

foreach ($fruits as $f) {
	if ($f['price'] >= 120) {
		// break;
		continue;
	}
	echo $f['name'] . $f['price'] . '円<br>';
}

$score = 80;
switch ($score) {
	case $score == 100:
		echo '満点です！';
		break;
	case $score <= 90:
		echo 'おしい。満点まであと少し';
		break;

	case $score <= 80:
		echo 'よく頑張りました';
		break;

	case $score <= 70:
		echo 'そこそこ頑張りました';
		break;
}
?>

<br>

<!-- 13 関数 -->

<?php
// $price = 1000;
// 数字に円を付ける

/**
 * 数字に円をつけてフォーマットする 
 *
 * 詳しい説明～～
 *
 * @param int $price 価格の数字
 * @return string フォーマットされた価格
 */

function formatYenPrice($price)
{
	return number_format($price, 0) . '円';
}

echo	formatYenPrice(2000); // 結果: 1000円 
?>

<br>

<!-- 14 変数のスコープ -->
<?php
$age = 20;

function outputAge()
{
	global $age;
	echo '年齢は、' . $age;

	echo '<pre>';
	var_dump($_SERVER);
	echo '</pre>';	// スーパーグローバル変数
}

outputAge();
?>

<br>

<!-- 15 Include と Require -->

<!-- 16 ヘッダーとフッター -->