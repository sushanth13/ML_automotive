function toggleTheme() {
    const body = document.body;
    const ball = document.getElementById("theme-ball");
    const isLight = body.classList.toggle("light-theme");

    // Save preference to localStorage — all pages will pick this up automatically
    localStorage.setItem("theme", isLight ? "light" : "dark");

    if (!ball) return;

    if (isLight) {
        ball.style.transform = "translateX(24px)";
    } else {
        ball.style.transform = "translateX(0px)";
    }
}
