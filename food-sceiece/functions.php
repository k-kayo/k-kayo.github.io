<!-- このファイルについて：
  検索結果ページに表示する記事の数や、サイトのRSSフィードに含めるコンテンツなど、WordPressの中核となる動作を調整
ショートコードを自作
特定のページにライブチャットサービスのスクリプトを注入する、サイトのフッターを編集するなど、コンテンツやスクリプトを操作できる
functions.phpファイルには、静的であるHTMLだけでなく、PHPコードを追加することができるため、可能性は無限大です。
 -->

<?php

add_theme_support('title-tag');

// @return void

function my_theme_support()
{
  // タイトルタグを出力する
  add_theme_support('title-tag');

  // アイキャッチ画像を有効化する
  add_theme_support('post-thumbnails');
}

add_action('after_setup_theme', 'my_theme_support');


// <title>の区切り文字を変更する※教科書に書いてある順番と先生の書き方が違う
function my_document_title_separator($separator)
{
  $separator = '|';
  return $separator;
}
add_filter(
  'document_title_separator',
  'my_document_title_separator'
);
