
// display error limit service convert
let fileResult1 = document.getElementById("display1");
let fileResult2 = document.getElementById("display2");

$(document).ready(function () {
    fileResult1.classList.add("bg-red-200", "border-red-600", "text-red-600");
    fileResult1.innerHTML = "Rất tiếc! bạn đã dùng hết số lần miễn phí. Hãy <a href=/login class='text-yellow-700 underline-offset-auto'><button> Đăng nhập </button></a> để sử dụng nhiều hơn";
    fileResult1.classList.add("bg-red-200", "border-red-600", "text-red-600");
    fileResult2.innerHTML = "Thời gian bạn sử dụng tiếp theo:";
    fileSubmit.disabled = true;

});