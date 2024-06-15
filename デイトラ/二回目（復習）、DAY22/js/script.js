// jQuery("#js-menu-drawer").on("click", function () {
//   jQuery(this).toggleClass("is-checked");
//   jQuery("#js-drawer").slideToggle();
//   jQuery("body").toggleClass("is-fixed");
// });

jQuery(".js-accordion").on("click", function () {
  jQuery(this).next().slideToggle();
});