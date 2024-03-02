<?php get_header(); ?>

<main>
  <section class="section section-foodList">
    <div class="section_inner">
      <div class="section_header">
        <h2 class="heading heading-primary"><span>フード紹介</span>FOOD</h2>
      </div>

      <?php
      $menu_terms = get_terms(['taxonomy' => 'menu']);
      ?>

      <?php if (!empty($menu_terms)) : ?>
        <?php foreach ($menu_terms as $menu) : ?>
          <section class="section_body">
            <h3 class="heading heading-secondary">
              <a href="<?= get_term_link($menu); ?>"><?= $menu->name; ?></a>
              <span><?= strtoupper($menu->slug); ?></span>
            </h3>
            <ul class="foodList">

              <?php
              $args = [
                'post_type' => 'food',
                'posts_per_page' => -1,
              ];

              $taxquerysp = [
                'relation' => 'AND',
                [
                  'taxonomy' => 'menu',
                  'field' => 'slug',
                  'terms' => $menu->slug,
                ],
              ];

              $args['tax_query'] = $taxquerysp;

              $the_query = new WP_Query($args);
              ?>
              <?php if ($the_query->have_posts()) : ?>
                <?php while ($the_query->have_posts()) : $the_query->the_post(); ?>
                  <li class="foodList_item">
                    <?php get_template_part('template-parts/loop', 'food'); ?>
                  </li>
                <?php endwhile; ?>
              <?php endif; ?>

            </ul>
          </section>
        <?php endforeach; ?>
      <?php endif; ?>

    </div>
  </section>
</main>

<?php get_footer(); ?>