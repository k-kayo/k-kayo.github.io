AOS.init();

$(function () {
  $(".mv-area_photo").slick({
    autoplay: true,
    autoplaySpeed: 4000,
    infinite: true,
    speed: 1200,
    fade: true,
    cssEase: "linear",
    adaptiveHeight: true,
    arrows: false, // 👈前後の矢印
    swipe: false, //👈 スマホでスワイプした時にスワイプしない
  });
});
