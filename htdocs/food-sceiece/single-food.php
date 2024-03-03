<?php get_header(); ?>
<main>
  <?php if (have_posts()) : ?>
    <?php while (have_posts()) : the_post(); ?>
      <section class="section">
        <div class="section_inner">

          <div class="food">
            <div class="food_body">
              <div class="food_text">
                <h2 class="heading heading-primary"><?php the_title(); ?></h2>
                <div class="food_content">
                  <?php the_content(); ?>
                </div>
              </div>
              <div class="food_pic">
                <?php if (get_field('recommend')) : ?>
                  <span class="food_label">オススメ</span>
                <?php endif; ?>
                <?php $pic = get_field('pic');
                $pic_url = $pic['sizes']['large'];  //大サイズ画像のURL
                ?>
                <img src="<?= $pic_url; ?>" alt="">
              </div>
            </div>
            <ul class="food_list">
              <li class="food_item">
                <span class="food_itemLabel">価格</span>
                <span class="food_itemData"><?php the_field('price'); ?>円</span>
              </li>
              <li class="food_item">
                <span class="food_itemLabel">カロリー</span>
                <span class="food_itemData"><?= number_format(get_field('calorie')); ?>kcal</span>
              </li>
              <li class="food_item">
                <span class="food_itemLabel">アレルギー</span>
                <span class="food_itemData">
                  <?php
                  $allergies = get_field('allergies');
                  echo implode('、 ', $allergies);

                  /**教科書のやり方
                   *   foreach ($allergies as $key => $allergy) {
                   *     echo $allergy;
                   *     if (
                   *    $allergy !== end($allergies)
                   *       ) {
                   *       echo ', ';
                   *        }
                   *       }
                   */
                  ?>
                </span>
              </li>
            </ul>
          </div>
        </div>
      </section>
    <?php endwhile; ?>
  <?php endif; ?>
</main>

<?php get_footer(); ?>