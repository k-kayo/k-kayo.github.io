<?php

/*テーマの機能を追加する
 * @return void
 */

function my_theme_support()    // 「my_theme_support」＝任意の関数名
{
  // titleタグを出力する
  add_theme_support('title-tag');

  // アイキャッチ画像を有効化する
  add_theme_support('post-thumbnails');

  // カスタムメニュー機能を使用可能にする/カスタムメニューを作成する
  add_theme_support('menus');
}
//👇テーマのセットアップが終わった後,自分の関数であるthemeセットアップを行うという意味
add_action('after_setup_theme', 'my_theme_support');


// htmlを出力する
add_theme_support('html5');


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


/** コンタクトフォーム７の時には、整形機能をOFFにする
 *
 * @return bool
 */
function my_wpcf7_autop()
{
  return false;
}
add_filter('wpcf7_autop_or_not', 'my_wpcf7_autop');


/**
 *メインクエリを変更する
 */
function my_pre_get_posts($query)
{
  if (is_admin() || !$query->is_main_query()) {
    return;
  }
  // 管理画面、メインクエリ以外には設定しない
  if ($query->is_home()) {
    $query->set('posts_per_page', 3);
    return;
  }
}


/* タイトルの「保護中」の文字を削除する
 * @return void
 */
add_action('pre_get_posts', 'my_pre_get_posts');
// '保護中: %s'
function my_protected_title()
{
  return '%s';
}
add_filter('protected_title_format', 'my_protected_title');


/*
 * パスワード保護フォームをカスタマイズする
 */
function my_password_form()
{
  remove_filter('the_content', 'wpautop');
  $wp_login_url = wp_login_url();
  // 👇heredocは $html = "";とほぼ同義 複数行にわたる文字列の作成に便利
  $html = <<<HTML
  <p>パスワードを入力してください。</p>
  <form  action="{$wp_login_url}?action=postpass" method="post" class="post-password-form">
  <input type="password" name="post_password" />
  <input type="submit" name="送信" value="送信" />
</form>
HTML;
  return $html;
}
add_filter('the_password_form', 'my_password_form');


/**
 * Var dump with pre tag
 *
 * @param mixed $content
 * @return void
 */

function my_dump($content)
{
  echo '<pre>';
  var_dump($content);
  echo '</pre>';
}
