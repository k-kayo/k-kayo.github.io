<?php
//データ受信後の処理
//1. 送信のチェック
//3-1. （エラーあり）エラーメッセージを表示
//3-2. （エラーなし）トップページにリダイレクト
//4. フラッシュメッセージ（1回のみ表示する）


$error = [
  'pizza-name' => [
    'required' => false,
    'format' => false,
  ],
  'chef-name' => [
    'required' => false,
    'format' => false,
  ],
  'topping' => [
    'required' => false,
    'format' => false,
  ],
];

//1. 送信のチェック
if (
  isset($_POST['submit']) &&
  $_POST['submit'] === 'submit'
)

  //2. エラーチェック
  if (empty($_POST['pizza-name'])) {
    $error = '必須入力です';
  } else {
    //入力があった場合
  }
if (empty($_POST['chef-name'])) {
} else {
  //入力があった場合
}
if (empty($_POST['topping'])) {
} else {
  //入力があった場合
}

//3-1. （エラーあり）エラーメッセージを表示

//3-2. （エラーなし）トップページにリダイレクト


//4. フラッシュメッセージ（1回のみ表示する）

?>


<?php
include 'template/header.php';
?>

<div class="container">
  <h1 class="text-center my-5">ピザの追加</h1>
</div>

<div class="row justify-content-center">
  <div class="col-md-8 bg-white p-4 rounded">
    <form action="add.php" method="get">
      <div class="mb-3">
        <label for="pizza-name" class="form-label fw-bold">ピザの名前</label>
        <input type="text" name="pizza-name" id="pizza-name" placeholder="マルゲリータ" class="form-control">
        <p class="form-text">ピザの作者の名前を入力して下さい。ニックネームもOK。</p>
      </div>
      <div class="mb-3">
        <label for="chef-name" class="form-label fw-bold">シェフの名前</label>
        <input type="text" name="chef-name" id="chef-name" placeholder="マルゲリータ" class="form-control">
        <p class="form-text">100文字以内で入力</p>
        <p class="text-danger"> <?= $error = '必須入力です'; ?></p>

      </div>
      <div class="mb-3">
        <label for="topping-name" class="form-label fw-bold">トッピング</label>
        <input type="text" name="topping-name" id="topping-name" placeholder="チーズ、バジル" class="form-control">
      </div>
      <div class="text-center">
        <button class="btn btn-primary" value="submit" name="submit">追加する</button>
      </div>
    </form>
    <?php
    var_dump($_POST);
    ?>
  </div>
</div>

<?php
include 'template/footer.php';
?>