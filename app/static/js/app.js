document.addEventListener("DOMContentLoaded",()=>{
 const form=document.getElementById("uploadForm"),result=document.getElementById("result");
 form.addEventListener("submit",async e=>{
  e.preventDefault();result.innerHTML="⏳ جاري التحويل...";
  const fd=new FormData();
  fd.append("file",document.getElementById("fileInput").files[0]);
  fd.append("method",document.getElementById("method").value);
  fd.append("use_external",document.getElementById("useExternal").checked?"true":"false");
  const res=await fetch("/api/convert",{method:"POST",body:fd});
  const data=await res.json();
  if(data.url){
    result.innerHTML=`✅ تم التحويل!<br><a href='${data.url}' target='_blank'>تحميل الصورة</a><br>
    <img src='${data.url}' class='preview' alt='result'>`;
  } else result.textContent=JSON.stringify(data);
 });
});
