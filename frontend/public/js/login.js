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
  document
    .querySelectorAll(".error-text")
    .forEach((el) => (el.textContent = ""));
  document
    .querySelectorAll(".invalid")
    .forEach((el) => el.classList.remove("invalid"));

  const generalError = document.getElementById("general-error");
  if (generalError) generalError.textContent = "";
}

function showErrors(errors) {
  cleanErrors();

  Object.keys(errors).forEach((key) => {
    const errorSpan = document.getElementById(`${key}-error`);
    if (errorSpan) {
      errorSpan.textContent = errors[key];
    }

    const inputField = document.getElementById(key);
    if (inputField) {
      inputField.classList.add("invalid");
    }
  });
}

async function login(email, password) {
  const btnLogin = document.getElementById("submit");

  const errors = authValidator.login(email, password);

  if (Object.keys(errors).length) {
    showErrors(errors);
    return;
  }

  const formData = new FormData();
  formData.append("username", email);
  formData.append("password", password);

  btnLogin.classList.add("loading");
  btnLogin.disabled = true;

  try {
    const response = await fetch(`${API_URL}/api/v1/auth/login`, {
      method: "POST",
      body: formData,
      credentials: "include",
    });

    const result = await response.json();

    if (!response.ok) {
      cleanErrors();

      document.getElementById("general-error").textContent =
        result.detail || "Erro ao logar";

      btnLogin.classList.remove("loading");
      btnLogin.disabled = false;

      return;
    }

    window.location.href = "dashboard.html";
  } catch (error) {
    console.error("Erro no login:", error);

    document.getElementById("general-error").textContent = "Erro de conexão.";
    btnLogin.classList.remove("loading");
    btnLogin.disabled = false;
  }
}

document.getElementById("login-form").addEventListener("submit", function (e) {
  e.preventDefault();
  const emailValue = document.getElementById("email").value;
  const passwordValue = document.getElementById("password").value;

  login(emailValue, passwordValue);
});
