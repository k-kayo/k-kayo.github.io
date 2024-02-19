<?php
if (isset($_GET['submit'])) {
  // ひとまずechoしてみる
  echo $_GET['chef-name'] . '<br>';
  echo $_GET['pizza-name'] . '<br>';
  echo $_GET['toppings'];
}
?>

<!doctype html>
<html lang="ja">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Pizzeriaインタープラン</title>
  <link rel="stylesheet" href="	https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
  <link rel="stylesheet" href="./css/style.css">
</head>

<body class="bg-light">
  <header>
    <nav class="navbar bg-white">
      <div class="container">
        <a href="index.php" class="navbar-brand">Pizzeriaインタープラン</a>
        <a href="add.php" class="btn btn-primary">ピザを追加する</a>
      </div>
    </nav>
  </header>