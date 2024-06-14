//ドロワー
document.querySelector("#js-drawer-button").addEventListener("click", function (e) {
  e.preventDefault();

  document.querySelector("#js-drawer-button").classList.toggle("is-checked");
  document.querySelector("#js-drawer-content").classList.toggle("is-checked");
});

document.querySelectorAll('#js-drawer-content a[href^="#"]').forEach(function (link) {
  link.addEventListener("click", function (e) {
    document.querySelector("#js-drawer-button").classList.remove("is-checked");
    document.querySelector("#js-drawer-content").classList.remove("is-checked");
  });
});
