function validateEmail(email) {
  if (!email) return "O email é obrigatório.";
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) return "Email inválido.";
  return null;
}

export const authValidator = {
  login(email, password) {
    const errors = {};

    const emailErrors = validateEmail(email);
    if (emailErrors) errors.email = emailErrors;

    if (!password) errors.password = "A senha é obrigatória.";

    return errors;
  },

  register(name, email, password) {
    const errors = {};

    const emailErrors = validateEmail(email);
    if (emailErrors) errors.email = emailErrors;

    if (password.length < 6) errors.password = "Mínimo de 6 caracteres.";

    if (!name) errors.name = "O nome é obrigatório.";

    return errors;
  },

  forgotPassword(email) {
    const errors = {};

    const emailErrors = validateEmail(email);
    if (emailErrors) errors.email = emailErrors;

    return errors;
  },

  verifyCode(code, email) {
    const errors = {};

    const emailErrors = validateEmail(email);
    if (emailErrors) errors.email = emailErrors;

    if (code.length < 6) errors.code = "Código inválido.";

    return errors;
  },

  resetPassword(password, resetPassword) {
    const errors = {};

    if (password.length < 6) errors.password = "Mínimo de 6 caracteres.";
    if (password !== resetPassword)
      errors.confirmPassword = "As senhas não coincidem.";

    return errors;
  },
};
