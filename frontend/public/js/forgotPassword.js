import { authValidator } from "./validators/authValidator.js";
import { API_URL } from "./config.js";

function cleanErrors() {
  document
    .querySelectorAll(".error-text")
    .forEach((el) => (el.textContent = ""));
  document
    .querySelectorAll(".invalid")
    .forEach((el) => el.classList.remove("invalid"));
}

function showErrors(errors) {
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

async function forgotPassword(email) {
  const btnSubmit = document.getElementById("submit");

  const errors = authValidator.forgotPassword(email);

  if (Object.keys(errors).length) {
    showErrors(errors);
    return;
  }

  btnSubmit.classList.add("loading");
  btnSubmit.disabled = true;

  try {
    const response = await fetch(`${API_URL}/api/v1/auth/forgot-password`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email: email }),
    });

    const result = await response.json();

    if (!response.ok) {
      alert("Erro: " + (result.detail || "Falha ao enviar e-mail"));
      return;
    }

    localStorage.setItem("reset_email", email);
    window.location.href = "verifyCode.html";
  } catch (error) {
    console.error("Falha ao enviar o email:", error);
  }
}

document.getElementById("submit").addEventListener("click", function (e) {
  e.preventDefault();

  const emailValue = document.getElementById("email").value;

  forgotPassword(emailValue);
});
