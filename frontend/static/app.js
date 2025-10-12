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
        try {
          // Try to parse the error response for more specific message
          const errorData = JSON.parse(err.message);
          this.error = errorData.detail || text.errorMessage;
        } catch {
          // Fallback to generic message if parsing fails
          this.error = text.errorMessage;
        }
      } finally {
        this.loading = false;
      }
    },
    previewPDF() {
      if (!this.result?.pdf_base64) return;
      const pdfWindow = window.open("");
      if (pdfWindow) {
        pdfWindow.document.write(
          `<iframe src="data:application/pdf;base64,${this.result.pdf_base64}" ` +
            'title="Preview" style="border:none;width:100%;height:100%;"></iframe>'
        );
      }
    },
    downloadPDF() {
      if (!this.result?.pdf_base64) return;
      const link = document.createElement("a");
      const safeTheme = (this.result.theme || "tohu-kaiako").replace(/[^a-z0-9]+/gi, "-").toLowerCase();
      link.href = `data:application/pdf;base64,${this.result.pdf_base64}`;
      link.download = `${safeTheme || "learning-pack"}.pdf`;
      link.click();
    },
  };
}
