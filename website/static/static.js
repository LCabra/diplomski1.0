// script.js

const dropdown = document.getElementById("profileDropdown");

document.addEventListener("click", (event) => {
    console.log("Document click event");
    if (!dropdown.contains(event.target)) {
        dropdown.querySelector(".dropdown-content").style.display = "none";
    }
});

dropdown.addEventListener("click", (event) => {
    console.log("Dropdown click event");
    const dropdownContent = dropdown.querySelector(".dropdown-content");
    dropdownContent.style.display = dropdownContent.style.display === "block" ? "none" : "block";
});

