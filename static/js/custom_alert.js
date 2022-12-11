const toast = document.querySelector(".toast_alert");
(closeIcon = document.querySelector(".close")),
(progress = document.querySelector(".progress"));

let timer1, timer2;

if(closeIcon !=null){
  
  timer1 = setTimeout(() => {
    toast.classList.remove("active");
  }, 10000); 

  timer2 = setTimeout(() => {
    progress.classList.remove("active");
  }, 5300);


  closeIcon.addEventListener("click", () => {
    toast.classList.remove("active");

    setTimeout(() => {
      progress.classList.remove("active");
    }, 300);

    clearTimeout(timer1);
    clearTimeout(timer2);
  });
}