AOS.init();

// ---------------授業の内容---------------------------------//
// $(document).ready(function () {
//   alert("jQuery動作テスト");
// });

/*
$("h1").css("color", "green");

$(".site-header-nav li a").css("color", "blue");

$(".mv-copy").next().css("text-decoration", "underline");

$(".mv-subcopy").prev().css("font-weight", "bold");

$(".service-card").parent().css("border", "1px solid orange");

$(".site-footer-sns").children().css("color", "orange");

$(".works-panel").find(".works-title").css("border-bottom", "2px solid #000");

$(".contact-logo").closest("div").css("background", "#eee");
*/
//jQuery４まで

// $(".works-container")
// .css("border", "4px dotted orange")
// .find(".works-thumb")
// .css("opacity", "0.5")
// .next()
// .css('background', 'rgba(255,255,0,0.5)')
// .children().css('text-decoration', 'underline');
// jQuery5まで

// const tweet = '<div class="tweet-content">イエローマジックデザインワークショップを開催しました。「普段何気なく使っているモノの見方を変えて見る」をテーマに、参加者のいろんなアイデアと作品が生まれました。</div>';

// const $tweetContainer = $('.tweet-container');

// $tweetContainer.append(tweet);
// $tweetContainer.prepend(tweet);
// $tweetContainer.before(tweet);
// $tweetContainer.after(tweet);
// $tweetContainer.html(tweet);
// $tweetContainer.text(tweet);
// jQuery6まで

// jQuery7まで
// let display = true;
// const $content = $(".quick-news-content");
// $("#quick-news-btn").on("click", (e) => {
//   if (display) {
//     $content.wrap('<div class="hidden">');
//     $(e.target).text("＋ ニュースを開く");
//     display = false;
//   } else {
//     $content.unwrap();
//     $(e.target).text("✕  ニュースを閉じる");
//     display = true;
//   }
// });

// jQuery８まで
// $(".works-desc").empty();
// $(".works-desc").remove();

// jQuery９
// const $workImg = $('.works-thumb img');
// $workImg.removeAttr("alt");
// console.log($workImg.attr("alt"));
// $workImg.attr("alt", "アンティーク家具ショップ");
// $workImg.attr("id", "works-antique");

// jQuery１０
// const $serviceIcon = $(".service-icon");
// console.log($serviceIcon.css("color"));
// $serviceIcon.css({
//   'font-size': '20px',
//   'color': "red",
//   opacity: "0.8",
// });

// jQuery１１
// $(".faq-openclose").addClass("is-open");
// $(".faq-openclose").removeClass("faq-openclose");
// $(".faq-openclose").toggleClass("is-open");
// console.log($(".faq-openclose").hasClass("is-open"));

// jQuery１２
// $(".faq-openclose").on("click", (e) => {
//   console.log("クリックしました");
//   $(e.target).off('click');
//   $(e.target).toggleClass('is-open');
// });

// jQuery１３
// $(document).on('DOMContentLoaded', () => {
//   $(".site-header-logo").css("border-bottom", "2px solid black");
// });

// $(window).on('load', () => {
//   console.log('window load');
// })

// jQuery１４/*
// $('.faq-list *').on('click', e => {
//   console.log(e);
//   e.stopPropagation();
// })

// const mouseFollow = $(".mouse-follow");
// $(window).on('mousemove', e => {
//   console.log(e.clientX, e.clientY);
//   mouseFollow.css({
//     'left': e.clientX,
//     'top': e.clientY,
//   });
// })

// jQuery 15
// $(".mv-copy").on("click", e => {
//   $(e.target)
//     .animate({
//       "font-size": 40
//     })
//     .animate({
//       'font-weight': '700'
//     })
//     .animate({
//       'height': 'hide'
//     });
// });

// $('.pagetop').on("click", () => {
//   $('html').animate({
//     'scrollTop': 0
//   });
// });

// jQuery１６
// $(".tweet-show").on("click", () => {
//   $(".tweet-content-ls16").fadeIn(1000, function () {
//     $(this).css("background-color", "yellow");
//   });
// });

// $(".tweet-hide").on("click", () => {
//   $(".tweet-content-ls16").fadeOut();
// });

// jQuery１７
// $(".faq-openclose").on("click", e => {
//   const $dd = $(e.target).parent().next();

//     $(e.target).toggleClass('is-open');
//     $dd.stop().slideToggle(!$dd.is(':visible'));

// $dd.toggle(!$dd.is(':visible'));

// if ($dd.is(":visible")) {
//   $dd.hide();
// } else {
//   $dd.show();
// }

// });

// jQuery１９
// const tweets = ["「DX支援」に当社のサービスがお役に立てるかもしれません。", "良いデザインはどっち？ クイズを解くだけで、デザインの知識がどんどん身につく画期的なデザイン手法を紹介", "現場監督からWebデザイナーに転職。建築現場責任者として活躍されていた川本さんのキャリアチェンジの理由は？", "Webデザインの勉強やトレンドキャッチに役立つSNSアカウントおすすめ25選"];

// const tweetContent = $(".tweet-content-ls19");
// let counter = 0;
// tweetContent.text(tweets[counter]).fadeIn();

// setInterval(() => {
//   tweetContent.text(tweets[counter]).fadeOut(400, () => {
//   //   console.log("フェードアウト完了");

//   counter++;

//   if( counter === tweets.length ) {
//       counter = 0;
//     }

//   tweetContent.text(tweets[counter]).fadeIn();
//   });
// }, 3000);

// jQuery２０（jQuery inView設定）
// window.addEv {entListener
const $serviceList = $(".service-list");
$(window).on("scroll", () => {
  if ($serviceList.hasClass("in-view")) return;

  let isInView = $(".service-list").inView("topOnly", 150);
  // 👆例えばメソッドの第２引数（150）に200と指定すると、上に200pxずらすことができます。その逆をやる場合はマイナス値を指定すればOKです。
  if (isInView) {
    $serviceList.addClass("in-view");
    // （既に追加されていれば追加しない）
  }
});

// $(".works-container").slick();
//  👇追加したもの

// - 自動スライドを有効化 ／ ページネーションを表示
$(".works-container").slick({
  autoplay: true,
  speed: 800,
  dots: true,
});

// lax.jsの基本設定//
// 1. windowのload後にlax.jsを起動し、設定を行う
$(window).on("load", () => {
  // 2. lax.jsの起動
  lax.init();

  // 3. ドライバーの設定（アニメーションの基礎となるものの設定）
  lax.addDriver(
    // ドライバー名（なんでもOK）
    "parallaxY",
    // アニメーションの基礎となるデータを出力(関数)
    () => {
      return window.scrollY;
    }

    //👇 ダウンロード版ではなくCDN版を使う場合は下記のとおりに設定します。
    // オプション（）: https://github.com/alexfoxy/lax.js#driver-options
    // {
    //   inertiaEnabled: true/false,
    //   frameSteps: number = 1,
    // }
  );

  // 4. 対象の要素に３で作成したドライバーの値を適用（設定）
  // アニメーション対象の要素の設定
  lax.addElements(
    // 対象要素のセレクタ
    ".lax-target",

    // アニメーション
    {
      // 3で設定したドライバー名
      parallaxY: {
        // アニメーションするcssプロパティ名を設定（複数可）
        translateY: [
          // ドライバーマップ値(3で設定したデータや要素の位置)
          ["elInY", "elOutY"], // ドライバーの数値
          // 👇上記のマップ値に対応させる値
          // [-80, 100],  // 要素の数値

          // ブレイクポイントでデータを変更する場合はオブジェクトで指定
          {
            767: [-80, 60], // スクリーンサイズ < 768（以下？）
            768: [-80, 100], // スクリーンサイズ >= 768
          },

          // アニメーションオプション
          // {
          // Inertia option
          // inertia: 10
          // Inertia mode
          // inertiaMode: normal | absolute
          // CSS Fn
          // cssFn: () => {}
          // },
        ],

        // 2つ目のプロパティ
        opacity: [
          ["elInY", "elInY+300"],
          [0, 1],
        ],

        // 3つ目~
      },
    }

    // 5. Options(未設定でもOK): https://github.com/alexfoxy/lax.js#options
    // {},
  );
});

// jQuery２１
/* ナビゲーションの開閉 */
$(".site-header-navbtn").on("click", () => {
  $("body").toggleClass("is-nav-open");
});

$(".site-header-nav").on("click", "a", () => {
  $("body").toggleClass("is-nav-open", !$("body").hasClass("is-nav-open"));
});
