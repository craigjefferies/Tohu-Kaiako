function app() {
  const text = window.APP_TEXT;
  return {
    text,
    form: { theme: "", level: "ECE", keywords: "" },
    loading: false,
    result: null,
    error: "",
    async generate() {
      if (this.loading) return;
      this.loading = true;
      this.result = null;
      this.error = "";
      try {
        const response = await fetch("/api/generate_pack", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.form),
        });
        if (!response.ok) {
          throw new Error(await response.text());
        }
        this.result = await response.json();
      } catch (err) {
        console.error("Generation failed", err);
        this.error = text.errorMessage;
      } finally {
        this.loading = false;
      }
    },
    async downloadPDF() {
      window.print();
    },
  };
}
