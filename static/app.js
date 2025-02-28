function pokazMenu() {
  const menu = document.querySelector(".hamburger_menu");
  menu.classList.toggle("visible");
}
const form = document.getElementById("registration-form");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());

  try {
    const response = await fetch("http://localhost:5500/users", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      alert(`Błąd: ${error.error}`);
    } else {
      alert("Użytkownik dodany pomyślnie!");
      form.reset();
    }
  } catch (error) {
    console.error("Błąd połączenia:", error);
    alert("Wystąpił problem z serwerem.");
  }
});

document.addEventListener("DOMContentLoaded", function () {
  document
    .querySelector("form[action='users']")
    .addEventListener("submit", function (e) {
      const password = document.getElementById("password").value;
      const confirmPassword = document.getElementById("confirm_password").value;

      if (password !== confirmPassword) {
        e.preventDefault();
        alert("Passwords do not match!");
      }
    });
});
