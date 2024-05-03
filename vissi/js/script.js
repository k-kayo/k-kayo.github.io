// mvのスライダー //
$(".mv-area").slick({
  autoplay: true,
  autoplaySpeed: 4000,
  infinite: true,
  arrows: false, // 👈前後の矢印
  swipe: false, //👈 スマホでスワイプした時にスワイプしない
});

// Conceptと定番商品のスライダーの設定 //
$(".slider").slick({
  autoplay: true, //自動的に動き出すか。初期値はfalse。
  autoplaySpeed: 3000, //次のスライドに切り替わる待ち時間
  speed: 1000, //スライドの動きのスピード。初期値は300。
  infinite: true, //スライドをループさせるかどうか。初期値はtrue。
  slidesToShow: 1, //スライドを画面に3枚見せる
  slidesToScroll: 1, //1回のスクロールで3枚の写真を移動して見せる
  arrows: true, //左右の矢印あり
  prevArrow: '<div class="slick-prev"></div>', //矢印部分PreviewのHTMLを変更
  nextArrow: '<div class="slick-next"></div>', //矢印部分NextのHTMLを変更
  dots: true, //下部ドットナビゲーションの表示
  pauseOnFocus: false, //フォーカスで一時停止を無効
  pauseOnHover: false, //マウスホバーで一時停止を無効
  pauseOnDotsHover: false, //ドットナビゲーションをマウスホバーで一時停止を無効

  responsive: [
    {
      breakpoint: 992, // 768〜992px以下のサイズに適用
      settings: {
        slidesToShow: 2,
        slidesToScroll: 2,
        // centerMode: true,
        // variableWidth: true,
      },
    },
    {
      breakpoint: 768, // 480〜767px以下のサイズに適用
      settings: {
        slidesToShow: 1, // 画面に表示するスライドの数を設定します。
        slidesToScroll: 1, // 1回のスクロールでスライドする数を設定します。
      },
    },
  ],
});

// 定番商品 //
$(document).on("ready", function () {
  $(".regular_2").slick({
    dots: true,
    infinite: true,
    slidesToShow: 2,
    slidesToScroll: 1,
    responsive: [
      {
        breakpoint: 992, // 768〜992px以下のサイズに適用
        settings: {
          slidesToShow: 2,
          slidesToScroll: 1,
          // centerMode: true,
          // variableWidth: true,
        },
      },
      {
        breakpoint: 768, // 480〜767px以下のサイズに適用
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2,
        },
      },
    ],
  });
});

/*=================================
            アコーディオン
===================================*/
$(".faq-title").on("click", function () {
  //タイトル要素をクリックしたら
  var findElm = $(this).next(".faq-box"); //直後のアコーディオンを行うエリアを取得し
  $(findElm).slideToggle(); //アコーディオンの上下動作

  if ($(this).hasClass("close")) {
    //タイトル要素にクラス名closeがあれば
    $(this).removeClass("close"); //クラス名を除去し
  } else {
    //それ以外は
    $(this).addClass("close"); //クラス名closeを付与
  }
});

//ページが読み込まれた際にopenクラスをつけ、openがついていたら開く動作※不必要なら下記全て削除
// $(window).on("load", function () {
//   $(".accordion-area li:first-of-type").addClass("open");
//   $(".open").each(function (index, element) {
//     //openクラスを取得
//     var Title = $(element).children(".faq-title"); //openクラスの子要素のtitleクラスを取得
//     $(Title).addClass("close"); //タイトルにクラス名closeを付与し
//     var Box = $(element).children(".faq-box"); //openクラスの子要素boxクラスを取得
//     $(Box).slideDown(500); //アコーディオンを開く
//   });
// });

/*=================================
          トップへ戻るボタン
===================================*/
$(function () {
  const pagetop = $("#page-top");
  $(window).scroll(function () {
    if ($(this).scrollTop() > 800) {
      pagetop.fadeIn(300);
    } else {
      pagetop.fadeOut(300);
    }
  });
  pagetop.click(function () {
    $("body, html").animate({ scrollTop: 0 }, 800);
    return false;
  });
});
