
//check image valid (file type && fileSize) then process convert

let fileInput = document.getElementById("file");
let fileResult1 = document.getElementById("display1");
let fileResult2 = document.getElementById("display2");
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
fileInput.addEventListener("change", function () {
    if (fileInput.files.length > 0) {
    //https://stackoverflow.com/questions/7977084/check-file-type-when-form-submit
        var fileName = fileInput.files.item(0).name;
        var fileType = getExtension(fileName)
        if(isImage(fileName)){
            //Nếu file nhập lên là file ảnh
            fileResult1.classList.add("bg-green-200", "border-green-600", "text-green-600");
            fileResult1.innerHTML = "Tuyệt vời! file " + fileName + " của bạn có thể chuyển đổi được ";
        }else{
            //Không phải file ảnh
            fileResult1.classList.add("bg-red-200", "border-red-600", "text-red-600");
            fileResult1.innerHTML = "Rất tiếc! file " + fileName + " của bạn không thể chuyển đổi. File ảnh hỗ trợ: jpg, png, gif";
          //  fileSubmit.disabled = true;
        }
    
        const fileSize = fileInput.files.item(0).size;
        const fileMb = fileSize / 1024 ** 2;

        if (fileMb >= 2) {
        fileResult2.classList.add("bg-red-200", "border-red-600", "text-red-600");
        fileResult2.innerHTML = "Vui lòng lựa chọn file nhỏ hơn 2MB.";
      //  fileSubmit.disabled = true;
        } else {
        fileResult2.classList.add("bg-green-200", "border-green-600", "text-green-600");
        fileResult2.innerHTML = "Tuyệt vời! file "+fileName+" của bạn nằm trong giới hạn miễn phí (< 2MB)";
        }

        if (isImage(fileName) && (fileMb < 2))
                {fileSubmit.disabled=false}
        else {
            fileSubmit.innerHTML = "Load ảnh mới";
            fileSubmit.onclick = window.location.reload();
            fileSubmit.disabled= false;
        }
        console.log(fileSubmit.innerHTML);

    }
    });