//ドロワー
document.querySelector("#js-drawer-button").addEventListener("click", function (e) {
  e.preventDefault();

  document.querySelector("#js-drawer-button").classList.toggle("is-checked");
  document.querySelector("#js-drawer-content").classList.toggle("is-checked");
});

//--swiper --//
const swiper = new Swiper(".about__swiper", {
  loop: true,
  loopAdditionalSlides: 1,
  speed: 3000,
  autoplay: {
    delay: 0,
  },
  slidesPerView: 4,
  slidesPerView: "auto",
  spaceBetween: 10,

  breakpoints: {
    // ブレークポイント
    900: {
      slidesPerView: 5,
      slidesPerView: "auto",
      spaceBetween: 20,
    },
  },

  //ユーザーがドラッグしたときのスピード調整
  on: {
    touchEnd: (swiper) => {
      swiper.slideTo(swiper.activeIndex + 1);
    },
  },
});

// スライドを複製する処理
function cloneAndAppend(element, swiperWrap) {
  let clonedElement = element.cloneNode(true);
  swiperWrap.appendChild(clonedElement);
}

const swiperWrap = document.querySelector("#js-swiper-wrap");
const swiperSlides = swiperWrap.querySelectorAll(".swiper-slide");

for (let swiperSlide of swiperSlides) {
  cloneAndAppend(swiperSlide, swiperWrap);
}
// swiper ここまで//

// document.querySelectorAll('#js-drawer-content a[href^="#"]').forEach(function (link) {
//   link.addEventListener("click", function (e) {
//     document.querySelector("#js-drawer-button").classList.remove("is-checked");
//     document.querySelector("#js-drawer-content").classList.remove("is-checked");
//   });
// });
