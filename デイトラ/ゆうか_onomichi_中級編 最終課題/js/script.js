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

// jQueryの場合 --ドロワーコンテンツ
jQuery("#js-drawer-icon").on("click", function (e) {
  e.preventDefault();
  jQuery("#js-drawer-icon").toggleClass("is-checked");
  jQuery("#js-drawer-content").toggleClass("is-checked");
});

// JavaScriptの場合 --ドロワーコンテンツ
// const drawerIcon = document.querySelector("#js-drawer-icon");
// const drawerContent = document.querySelector("#js-drawer-content");
// if (drawerIcon) {
//   drawerIcon.addEventListener("click", function (e) {
//     e.preventDefault();
//     drawerIcon.classList.toggle("is-checked");
//     drawerContent.classList.toggle("is-checked");
//   });
// };

// Q&A --アコーディオン
jQuery(".js-accordion").on("click", function (e) {
  e.preventDefault(); //buttonには特にデフォルトの動きはないが、念のための無効化

  if (jQuery(this).parent().hasClass("is-open")) {
    //is-openが付いているかhasClassで確認
    jQuery(this).parent().removeClass("is-open"); //持っていればis-openを削除する
    jQuery(this).next().slideUp();
  } else {
    jQuery(this).parent().addClass("is-open"); //持っていなければ付ける
    jQuery(this).next().slideDown();
  }
});

// swiper
const swiper = new Swiper("#js-gallery-swiper", {
  spaceBetween: 82,
  // Optional parameters
  loop: true,

  // If we need pagination
  pagination: {
    el: "#js-gallery-pagination",
  },

  // Navigation arrows
  navigation: {
    nextEl: "#js-gallery-next",
    prevEl: "#js-gallery-prev",
  },
});

// モーダルウィンドウ--jQuery版
jQuery(".js-modal-open").on("click", function (e) {
  e.preventDefault();

  jQuery("#js-about-modal")[0].showModal();
});

jQuery(".js-modal-close").on("click", function (e) {
  e.preventDefault();

  jQuery("#js-about-modal")[0].close();
});

// モーダルウィンドウ--JavaScript版
// const modalOpenItems = document.querySelectorAll(".js-modal-open");
// const modalCloseItems = document.querySelectorAll(".js-modal-close");
// const aboutModal = document.querySelector("#js-about-modal");

// modalOpenItems.forEach(function (modalOpenItem) {
//   modalOpenItem.addEventListener("click", function (e) {
//     e.preventDefault();

//     if (aboutModal) {
//       aboutModal.showModal();
//     };
//   });
// });

// modalCloseItems.forEach(function (modalCloseItem) {
//   modalCloseItem.addEventListener("click", function (e) {
//     e.preventDefault();
//     if (aboutModal) {
//       aboutModal.close();
//     }
//   });
// });

// スマホSPのスムーススクロールを実装
jQuery('#js-drawer-content a[href^="#"]').on("click", function (e) {
  jQuery("#js-drawer-icon").removeClass("is-checked");
  jQuery("#js-drawer-content").removeClass("is-checked");
});

// PCのスムーススクロールを実装
jQuery('a[href^="#"]').on("click", function (e) {
  const speed = 300;
  const id = jQuery(this).attr("href"); // クリックされたリンクのhref属性の値を取得
  const target = jQuery("#" == id ? "html" : id); // href属性の値に基づいてスクロール先の要素を取得
  const position = jQuery(target).offset().top; // スクロール先要素の上端の位置を取得
  jQuery("html, body").animate(
    {
      scrollTop: position, // スクロール位置をアニメーション化
    },
    speed, // アニメーションの時間（ミリ秒）
    "swing" //swing or linear / スクロールのイージング（ease-in-out, linearなど）
  );
});

// スクロールに合わせてトップへ戻るボタンを表示する--jQuery版
// jQuery(window).on("scroll", function () {
//   if (100 < jQuery(window).scrollTop()) {
//     jQuery("#js-pagetop").addClass("is-show");
//   } else {
//     jQuery("#js-pagetop").removeClass("is-show");
//   }
// });

// スクロールに合わせてトップへ戻るボタンを表示する--JavaScript版
const pageTop = document.querySelector("#js-pagetop");
window.addEventListener("scroll", function () {
  if (100 < window.scrollY) {
    pageTop.classList.add("is-show");
  } else {
    pageTop.classList.remove("is-show");
  }
});

// スクロールに応じて要素を「フワッ」と登場させる/IntersectionObserverを使った実装例//
const intersectionObserver = new IntersectionObserver(function (entries) {
  entries.forEach(function (entry) {
    if (entry.isIntersecting) {
      entry.target.classList.add("is-in-view");
    } else {
      // entry.target.classList.remove("is-in-view");
      // 👆コメントアウト外すと何回も表示される。コメントアウトしておくと表示は１回のみ
    }
  });
});

const inViewItems = document.querySelectorAll(".js-in-view");
inViewItems.forEach(function (inViewItem) {
  intersectionObserver.observe(inViewItem);
});
