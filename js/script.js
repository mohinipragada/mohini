// Mobile menu: show/hide the nav links when the ☰ button is clicked

const menuToggle = document.getElementById("menuToggle");
const navLinks = document.getElementById("navLinks");

// Toggle the "open" class on the menu (CSS shows it when "open" is present)
menuToggle.addEventListener("click", function () {
  navLinks.classList.toggle("open");
});

// Close the menu after a link is clicked
const links = navLinks.querySelectorAll("a");
links.forEach(function (link) {
  link.addEventListener("click", function () {
    navLinks.classList.remove("open");
  });
});
