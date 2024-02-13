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

// AOS.init(); 👈私が記述していたもの
window.addEventListener("load", () => {
  AOS.init();
}); // 👈先生が解説で教えてくれたもの/このように書くと、読み込みが遅れることが解消されるとのこと。
