import { API_URL } from "./config.js";
import { authValidator } from "./validators/authValidator.js";

const togglePassword = document.getElementById("togglePassword");
const password = document.getElementById("password");

togglePassword.addEventListener("click", function () {
  const type =
    password.getAttribute("type") === "password" ? "text" : "password";

  password.setAttribute("type", type);

  this.classList.toggle("fa-eye");
  this.classList.toggle("fa-eye-slash");
});

function cleanErrors() {
  document.querySelectorAll(".error-text").forEach((el) => {
    el.textContent = "";
  });
  document.querySelectorAll(".invalid").forEach((el) => {
    el.classList.remove("invalid");
  });
}

function showErrors(errors) {
  cleanErrors();

  Object.keys(errors).forEach((key) => {
    const spanError = document.getElementById(`${key}-error`);
    if (spanError) {
      spanError.textContent = errors[key];
    }

    const inputField = document.getElementById(key);
    if (inputField) {
      inputField.classList.add("invalid");
    }
  });
}

async function register(name, email, password) {
  const btnRegister = document.getElementById("submit");

  const errors = authValidator.register(name, email, password);

  if (Object.keys(errors).length) {
    showErrors(errors);
    return;
  }

  const userData = {
    full_name: name,
    email: email,
    password: password,
  };

  btnRegister.classList.add("loading");
  btnRegister.disabled = true;

  try {
    const response = await fetch(`${API_URL}/api/v1/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userData),
    });

    if (!response.ok) {
      const data = await response.json();
      cleanErrors();
      btnRegister.classList.remove("loading");
      btnRegister.disabled = false;
      return;
    }

    window.location.href = "login.html";
  } catch (error) {
    console.error("Falha ao registar:", error);

    btnRegister.classList.remove("loading");
    btnRegister.disabled = false;
  }
}

document
  .getElementById("register-form")
  .addEventListener("submit", function (e) {
    e.preventDefault();
    const nameValue = document.getElementById("name").value;
    const emailValue = document.getElementById("email").value;
    const passwordValue = document.getElementById("password").value;

    register(nameValue, emailValue, passwordValue);
  });
