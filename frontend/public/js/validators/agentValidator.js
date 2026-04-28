export const agentValidator = {
  validate(name, instruction, token) {
    const errors = {};

    if (!name.trim()) {
      errors.name = "O nome é obrigatório.";
    }

    if (!instruction.trim()) {
      errors.instruction = "As instruções são obrigatórias.";
    }

    const tokenRegex = /^[0-9]{8,10}:[a-zA-Z0-9_-]{35,}$/;
    if (!token.trim()) {
      errors.tokenTelegram = "O token do Telegram é obrigatório.";
    } else if (!tokenRegex.test(token)) {
      errors.tokenTelegram = "Token inválido.";
    }

    return errors;
  },
};
