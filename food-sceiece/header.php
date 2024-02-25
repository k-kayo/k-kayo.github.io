<!DOCTYPE html>
<html lang="ja">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, user-scalable=no">
  <link rel="stylesheet" href="<?= get_template_directory_uri() ?>/assets/css/app.css" type="text/css" />
  <?php

  // 外部のスタイルシート（Googleフォントなど）を読み込む
  wp_enqueue_style('font-awesome', 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.2/css/all.min.css');
  wp_enqueue_style('google-web-fonts', 'https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap');

  //👇 独自のJavaScriptを読み込む関数
  wp_enqueue_script(
    'food-science-main',
    get_template_directory_uri() . '/assets/js/main.js',
    ['jquery'],
    filemtime(get_template_directory() . '/assets/js/main.js'), // 👈ファイルで更新時間を読み込む。ファイルの更新忘れを防止するため、ファイル更新時間を取得する
    true
    //  '1.1.2' 👈 (jsのバージョンを変えることが出来る)
  );

  wp_enqueue_script('jquery');  // jQueryの重複を回避して、適切なタイミングで読み込む
  wp_head(); ?> <!-- WordPressを使う上ではほぼマスト・headの閉じタグの直前で-->

</head>

<body <?php body_class(); ?>>
  <?php wp_body_open(); ?>
  <header class="header">
    <div class="header_logo">
      <h1 class="logo"><a href="<?= home_url(); ?>">FOOD SCIENCE<span><?PHP bloginfo('description'); ?></span></a></h1>
    </div>

    <div class="header_nav">
      <div class="header_menu js-menu-icon"><span></span></div>
      <div class="gnav js-menu">
        <ul>
          <li><a href="concept.html">コンセプト</a></li>
          <li><a href="food.html">メニュー</a></li>
          <li><a href="access.html">アクセス</a></li>
          <li><a href="category.html">最新情報</a></li>
        </ul>

        <div class="header_info">
          <form class="header_search">
            <input type="text" aria-label="Search">
            <button type="submit"><i class="fas fa-search"></i></button>
          </form>

          <div class="header_contact">
            <div class="header_time">
              <dl>
                <dt>OPEN</dt>
                <dd>09:00〜21:00</dd>
              </dl>
              <dl>
                <dt>CLOSED</dt>
                <dd>Tuesday</dd>
              </dl>
            </div>
            <p>
              <a href="#"><i class="fa-solid fa-envelope"></i><span>ご予約・お問い合わせ</span></a>
            </p>
          </div>
        </div>
      </div>
    </div>
  </header>