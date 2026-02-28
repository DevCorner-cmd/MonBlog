
const toggle = document.getElementById("theme-toggle");

// Charger le thème sauvegardé
const savedTheme = localStorage.getItem("theme");

if (savedTheme) {
document.documentElement.setAttribute("data-theme", savedTheme);
toggle.checked = savedTheme === "synthwave";
}

toggle.addEventListener("change", function () {
if (this.checked) {
    document.documentElement.setAttribute("data-theme", "synthwave");
    localStorage.setItem("theme", "synthwave");
} else {
    document.documentElement.setAttribute("data-theme", "light");
    localStorage.setItem("theme", "light");
}
});

