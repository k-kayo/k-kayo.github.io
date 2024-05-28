$(function () {
  //ページ内スクロール
  var navHeight = $(".header").outerHeight();

  $('a[href^="#"]').on("click", function () {
    var href = $(this).attr("href");
    var target = $(href == "#" || href == "" ? "html" : href);
    var position = target.offset().top - navHeight;
    $("html, body").animate({ scrollTop: position }, 300, "swing");
    return false;
  });

  //ページトップ
  $("#js-page-top").on("click", function () {
    $("body,html").animate({ scrollTop: 0 }, 300);
    return false;
  });
});

//3. 画像のモーダル
$(".gallery").modaal({
  type: "image",
  overlay_close: true, //モーダル背景クリック時に閉じるか
  before_open: function () {
    // モーダルが開く前に行う動作
    $("html").css("overflow-y", "hidden"); /*縦スクロールバーを出さない*/
  },
  after_close: function () {
    // モーダルが閉じた後に行う動作
    $("html").css("overflow-y", "scroll"); /*縦スクロールバーを出す*/
  },
});

$(function () {
  //alert();
  var qrtext = "ポートフォーリオサイトQRコード";
  var utf8qrtext = unescape(encodeURIComponent(qrtext));
  $("#img-qr").html("");
  $("#img-qr").qrcode({ text: utf8qrtext });
});

var canvas = $("#img-qr canvas");
