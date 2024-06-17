//ドロワー こちらは動きます
document.querySelector("#js-drawer-button").addEventListener("click", function (e) {
  e.preventDefault();

  document.querySelector("#js-drawer-button").classList.toggle("is-checked");
  document.querySelector("#js-drawer-content").classList.toggle("is-checked");
});

//
document.querySelectorAll('#js-drawer-content a[href^="#"]').forEach(function (link) {
  link.addEventListener("click", function (e) {
    document.querySelector("#js-drawer-button").classList.remove("is-checked");
    document.querySelector("#js-drawer-content").classList.remove("is-checked");
  });
});

//👇上手くいきませんでした
// ドロワーメニューを開くためのボタン（トグルボタン）をクリックしたときの処理
// document.getElementById("#js-drawer-button").addEventListener("click", function () {
//   var drawerNav = document.getElementById("#js-drawer-content");
//   if (drawerNav.classList.contains("is-checked")) {
//     // ドロワーメニューが既に表示されている場合は閉じる
//     drawerNav.classList.remove("is-checked");
//   } else {
//     // ドロワーメニューが非表示の場合は開く
//     drawerNav.classList.add("is-checked");
//   }
// });

// $(function () {
//   $("#menu").css("display", "none");
//   $("#menu-bt").on("click", function () {
//     $("#menu").slideToggle(300);
//     $(this).toggleClass("active");
//     if ($(this).hasClass("active")) {
//       $("#drower").attr("src", "https://webmist.info/image/spmenu2.png");
//     } else {
//       $("#drower").attr("src", "https://webmist.info/image/spmenu.png");
//     }
//   });
// });