$(document).ready(function () {
  toggle();
});

function toggle() {
  // $(".toggle-trigger").click(function (e) {
  //   e.preventDefault();
  //   $(".bottom").slideToggle();
  // });

  $(".toggle-trigger").click(function (e) {
    e.preventDefault();
    // $(this).closest(".item").find(".bottom").toggle();
    // // for slide animation
    $(this).closest(".item").find(".bottom").slideToggle("fast");
  });
}

// for show and hide password / pin

$(document).click(function () {
  $(".show-hide").on("click", function (e) {
    e.preventDefault();
    var passInput = $(this).closest(".item").find("#passInput");
    if (passInput.attr("type") === "password") {
      passInput.attr("type", "text");
    } else {
      passInput.attr("type", "password");
    }
  });
});

// for copy password / pin

$(document).click(function () {
  $(".copy-icon").on("click", function (e) {
    e.preventDefault();
    var $temp = $("<input>");
    var copyItem = $(this).closest(".copy-item-container").find(".copy-item");
    $("body").append($temp);
    $temp.val($(copyItem).text()).select();
    document.execCommand("copy");
    $temp.remove();
  });
});

// for Special Card Effect

document.getElementById("special-cards").onmousemove = (e) => {
  for (const card of document.querySelectorAll(".special-hover-card")) {
    const rect = card.getBoundingClientRect(),
      x = e.clientX - rect.left,
      y = e.clientY - rect.top;

    card.style.setProperty("--mouse-x", `${x}px`);
    card.style.setProperty("--mouse-y", `${y}px`);
  }
};
console.log("hey");

// for warning/alert message

setTimeout(function () {
  if ($(".msg").length > 0) {
    $(".alert").remove();
  }
}, 2000);

$(".close-btn").click(function () {
  $(".alert").removeClass("show");
  $(".alert").addClass("hide");
});
