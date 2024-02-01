const year = document.querySelector("#year");
const date = new Date();

year.textContent = date.getFullYear();

console.dir(date);
console.log(date.getFullYear()); //年
console.log(date.getDay()); //曜日
console.log(date.getHours()); //時

// year.innerHTML = "あいうえお";
// year.innerText = "かきくけこ";
// year.textContent = "さしすせそ"; // 👈　処理が他の二つに比べて重くない
