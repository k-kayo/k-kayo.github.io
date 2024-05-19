// ハンバーガーボタンとドロワー
$("#js-button-drawer").on("click", function () {
  $(this).toggleClass("is-checked");
  $("#js-drawer").slideToggle();
  $("body").toggleClass("is-fixed");
});

// お問い合わせ完了メッセージ
$(document).ready(function () {
  $("#form").submit(function (event) {
    var formData = $("#form").serialize();
    $.ajax({
      url: "https://docs.google.com/forms/u/0/d/e/1FAIpQLSd_OMYyDyJgwGRxejU6_yv33egdk1vFn5L8BiM67RJ9pkf6nA/formResponse",
      data: formData,
      type: "POST",
      dataType: "xml",

      statusCode: {
        0: function () {
          $(".end-message").slideDown();
          $(".submit-btn").fadeOut();
          // window.location.href = "thanks.html";
        },
        200: function () {
          $(".false-message").slideDown();
        },
      },
    });
    event.preventDefault();
  });
});
