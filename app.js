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
    const response = await fetch("http://localhost:5000/users", {
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
  const form = document.querySelector("form");

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    const response = await fetch("/users", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();
    if (response.ok) {
      alert("Użytkownik dodany!");
      window.location.reload();
    } else {
      alert(result.error);
    }
  });
});
