$('.mv').slick({
  fade: true,
  autoplay: true,
  autoplaySpeed: 4000,
  speed: 1200,
  arrows: false,
  swipe: false,
})

window.addEventListener('load', () => {
  AOS.init()
})