function Copy(color) {
 var cb = document.getElementById(color);
  cb.value = color;
  cb.style.display='block';
  cb.select();
  document.execCommand('copy');
  cb.style.display='none';
}