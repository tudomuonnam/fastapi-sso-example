// decor display Imageconverttext


function copyText(){
    const text = document.getElementById("context");
    const button = document.createElement("copyText");

    let range = document.createRange();
    let selection = window.getSelection();

    range.selectNodeContents( text );
    selection.removeAllRanges();
    selection.addRange( range );
    document.execCommand( 'copy' );
    window.getSelection().removeAllRanges();
    alert("Đã copy vào clipboard!");
};

function downloadFile() {
    const link = document.createElement("a");
    const element = document.getElementById("context")//.innerHTML.replace(/\n|<.*?>/g,'');
    const content = element.innerText || element.textContent;
    const file = new Blob([content], { type: 'text/plain' });
    link.href = URL.createObjectURL(file);
    link.download = "sample.txt";
    link.click();
    URL.revokeObjectURL(link.href);
 };