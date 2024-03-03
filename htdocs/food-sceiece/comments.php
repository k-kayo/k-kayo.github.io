<section class="comments">
  <?php
  $args = [
    /**
     * 'fields' => [
     * 'url' => '<div class="sss">自分のサイトアドレス：
     * <input type ="test name="author"></div>',
     *]
     */
    'title_reply' => 'コメント投稿フォーム',
  ];
  comment_form($args);
  if (have_comments()) :
  ?>
    <ol class="commentlist">
      <?php
      $wp_list_comments_args = [
        'avatar_size' => 50,
        // 'format' => 'html5' 👈function.phpに記述しても良い
      ];
      wp_list_comments($wp_list_comments_args);
      ?>
    </ol>
  <?php
    $args = [
      'prev_text' => '←前のコメントページ',
      'next_text' => '次のコメントページ→',
      // 'type' => 'array', //データの取得のみに変化する
    ];
    // $data = paginate_comments_links($args);
    paginate_comments_links($args);
  // var_dump($data);
  endif;
  ?>
</section>