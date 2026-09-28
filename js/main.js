// ===== 1. Mobile menu: show/hide the nav links =====
const menuToggle = document.getElementById("menuToggle");
const navLinks = document.getElementById("navLinks");

function setMenu(open) {
  navLinks.classList.toggle("open", open);
  menuToggle.setAttribute("aria-expanded", open);
  menuToggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
}

menuToggle.addEventListener("click", function () {
  setMenu(!navLinks.classList.contains("open"));
});

// Close the menu after a link is clicked, or when Escape is pressed
navLinks.querySelectorAll("a").forEach(function (link) {
  link.addEventListener("click", function () {
    setMenu(false);
  });
});

document.addEventListener("keydown", function (event) {
  if (event.key === "Escape") setMenu(false);
});


// ===== 2. Copy-to-clipboard for AI prompts =====
const copyStatus = document.getElementById("copyStatus");

document.querySelectorAll(".copy-btn").forEach(function (button) {
  button.addEventListener("click", function () {
    const text = button.closest(".prompt-box").querySelector(".prompt-text").textContent.trim();

    copyText(text).then(function () {
      button.textContent = "Copied!";
      button.classList.add("copied");
      copyStatus.textContent = "Prompt copied to clipboard";

      // Reset the button after 2 seconds
      setTimeout(function () {
        button.textContent = "Copy";
        button.classList.remove("copied");
        copyStatus.textContent = "";
      }, 2000);
    });
  });
});

// Uses the modern Clipboard API, with a fallback for older browsers / file:// pages
function copyText(text) {
  if (navigator.clipboard && window.isSecureContext) {
    return navigator.clipboard.writeText(text);
  }
  const helper = document.createElement("textarea");
  helper.value = text;
  helper.setAttribute("readonly", "");
  helper.style.position = "absolute";
  helper.style.left = "-9999px";
  document.body.appendChild(helper);
  helper.select();
  document.execCommand("copy");
  helper.remove();
  return Promise.resolve();
}

// ===== 3. Screenshot placeholders =====
// If a design screenshot hasn't been added yet, show the placeholder text instead
document.querySelectorAll(".work-shot img").forEach(function (img) {
  function markMissing() {
    img.closest(".work-shot").classList.add("missing");
  }
  if (img.complete && img.naturalWidth === 0) {
    markMissing();
  } else {
    img.addEventListener("error", markMissing);
  }
});
