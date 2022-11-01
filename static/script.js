const modalWrapper = document.getElementById("modals-container");
const home = document.getElementById("card-container");
// var start = document.getElementById("start");
// console.log(modalWrapper)
if (modalWrapper) {
  function displayModal(id) {
    const modal = document.getElementById(id);
    modalWrapper.style.display = "flex";
    // start.style.display = "none";
    modal.style.display = "flex";
    home.style.display = "none";

    const close = document.getElementById("close-modal");
    close.addEventListener("click", () => {
      modalWrapper.style.display = "none";
      modal.style.display = "none";
      home.style.display = "block";
    });
  }
}

// function closeModal() {

//   // start.style.display = "block";
// }

//coping the password

const copies = document.querySelectorAll(".copy");
copies.forEach((copy) => {
  copy.onclick = () => {
    let elemntToCopy = copy.previousElementSibling;
    elemntToCopy.select();
    document.execCommand("copy");
  };
});
