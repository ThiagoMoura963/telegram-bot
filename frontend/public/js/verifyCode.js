import { API_URL } from "./config.js";
import { authValidator } from "./validators/authValidator.js";

function cleanErrors() {
  document.querySelectorAll(".error-text").forEach((el) => {
    el.textContent = "";
  });
  document.querySelectorAll(".invalid").forEach((el) => {
    el.classList.remove("invalid");
  });

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

async function verifyCode(code, email) {
  const btnSubmit = document.getElementById("submit");
  const generalError = document.getElementById("general-error");

  const errors = authValidator.verifyCode(code, email);

  if (Object.keys(errors).length) {
    showErrors(errors);
    return;
  }

  const verifyCodeData = {
    email: email,
    code: code,
  };

  btnSubmit.classList.add("loading");
  btnSubmit.disabled = true;

  try {
    const response = await fetch(`${API_URL}/api/v1/auth/verify-code`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(verifyCodeData),
    });

    const result = await response.json();

    if (!response.ok) {
      cleanErrors();

      generalError.textContent =
        result.detail || "Código incorreto. Tente novamente.";

      btnSubmit.classList.remove("loading");
      btnSubmit.disabled = false;

      return;
    }

    localStorage.setItem("reset_code", code);
    window.location.href = "resetPassword.html";
  } catch (error) {
    console.error("Falha ao verificar o código:", error);

    generalError.textContent = "Erro de conexão com o servidor.";

    btnSubmit.classList.remove("loading");
    btnSubmit.disabled = false;
  }
}

document.getElementById("submit").addEventListener("click", function (e) {
  e.preventDefault();

  const codeInputGroup = document.querySelector(".code-input-group");
  const codeInputs = codeInputGroup.querySelectorAll("input");

  const code = Array.from(codeInputs)
    .map((input) => {
      return input.value;
    })
    .join("");

  const email = localStorage.getItem("reset_email");

  verifyCode(code, email);
});
