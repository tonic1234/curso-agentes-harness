// OpenCode: un plugin es un módulo que devuelve ganchos. Lanzar un error bloquea.
export const BloquearMigraciones = async () => {
  return {
    "tool.execute.before": async (input, output) => {
      const ruta = output.args?.filePath ?? output.args?.path ?? "";
      if (["edit", "write"].includes(input.tool) && String(ruta).includes("migrations/")) {
        throw new Error("Bloqueado: no se editan migraciones. Usá: npm run migrate:nueva -- <nombre>");
      }
    },
  };
};
