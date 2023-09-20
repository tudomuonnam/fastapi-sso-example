
//check image valid (file type && fileSize) then process convert

let fileInput = document.getElementById("file");
let fileResult1 = document.getElementById("display1");
let fileResult2 = document.getElementById("display2");
let fileResult3 = document.getElementById("display3");
let fileSubmit = document.getElementById("file-submit");

function getExtension(filename) {
    var parts = filename.split('.');
    return parts[parts.length - 1];
    }
    
function isImage(filename) {
    var ext = getExtension(filename);
    switch (ext.toLowerCase()) {
        case 'jpg':
        case 'gif':
        case 'bmp':
        case 'png':
        //etc
        return true;
    }
    return false;
    }
function checkRemainConvert(data){
    fetch("/data", {
  method: "POST",
  body: JSON.stringify({
    userId: 1,
    title: "Fix my bugs",
    completed: false
  }),
  headers: {
    "Content-type": "application/json; charset=UTF-8"
  }
})
  .then((response) => response.json())
  .then((json) => console.log(json));


}
function refreshPage() {
  setTimeout(function(){
    fileInput = '';
    window.location.reload();
 }, 5000);
}
// $(document).ready(function () {
//     $.getJSON('https://api.ipify.org/?format=json', function(data){
//         //$("#gfg").html(data.ip);
//         //$(".display").html(display);
//         console.log(data.ip);
    
//   });

// });
fileInput.addEventListener("change", function () {
    if (fileInput.files.length > 0) {
        //Check file type
//https://stackoverflow.com/questions/7977084/check-file-type-when-form-submit
        var fileName = fileInput.files.item(0).name;
        console.log(fileName);
        if(isImage(fileName)){
            //Nếu file nhập lên là file ảnh
            fileResult1.classList.add("bg-green-200", "border-green-600", "text-green-600");
            fileResult1.innerHTML = "Tuyệt vời! file " + fileName + " của bạn có thể chuyển đổi được ";
        }else{
            //Không phải file ảnh
            fileResult1.classList.add("bg-red-200", "border-red-600", "text-red-600");
            fileResult1.innerHTML = "Rất tiếc! file " + fileName + " của bạn không thể chuyển đổi. File ảnh hỗ trợ: jpg, png, gif";
            fileSubmit.disabled = true;
        }
    
        const fileSize = fileInput.files.item(0).size;
        const fileMb = fileSize / 1024 ** 2;
        if (fileMb >= 2) {
        fileResult2.classList.add("bg-red-200", "border-red-600", "text-red-600");
        fileResult2.innerHTML = "Vui lòng lựa chọn file nhỏ hơn 2MB.";
        fileSubmit.disabled = true;
        } else {
        fileResult2.classList.add("bg-green-200", "border-green-600", "text-green-600");
        fileResult2.innerHTML = "Tuyệt vời! file "+fileName+" của bạn nằm trong giới hạn miễn phí (< 2MB)";
        }

        if (isImage(fileName) && (fileMb < 2)){fileSubmit.disabled=false}
        else {
         // fileSubmit.innerHTML = "Load ảnh mới";
         // fileSubmit.setAttribute( "onClick", "window.location.reload()" )
          fileSubmit.onclick = refreshPage(); //reload page after 5s
         // fileSubmit.disabled= false;
      }
      fileResult3.classList.add("bg-green-200", "border-green-600", "text-orange-600");
      fileResult3.innerHTML = "Bạn có 2 lần convert miễn phí, hãy <a href='/login' rel='/upload'> Đăng Nhập </a> để tăng thêm lượt convert";

    }
    
    });