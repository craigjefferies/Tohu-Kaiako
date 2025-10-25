const PACK_STORAGE_KEY = "tohu-kaiako-history";

const state = {
  currentView: "generator",
  generating: false,
  currentPack: null,
  history: [],
  firebaseReady: false,
  config: window.__APP_CONFIG__ || {},
};

const sparkLibrary = [
  {
    category: "Daily Life",
    icon: "🌞",
    theme: "Tidying the sandpit together",
    focus: "collaborative verbs, sequencing, hygiene, routines",
  },
  {
    category: "Daily Life",
    icon: "🌞",
    theme: "Washing hands before kai time",
    focus: "collaborative verbs, sequencing, hygiene, routines",
  },
  {
    category: "Daily Life",
    icon: "🌞",
    theme: "Packing toys away after play",
    focus: "collaborative verbs, sequencing, hygiene, routines",
  },
  {
    category: "Outdoors & Nature",
    icon: "🐚",
    theme: "Feeding ducks at the school pond",
    focus: "environment, movement verbs, nature vocabulary",
  },
  {
    category: "Outdoors & Nature",
    icon: "🐚",
    theme: "Planting seeds in the garden bed",
    focus: "environment, movement verbs, nature vocabulary",
  },
  {
    category: "Outdoors & Nature",
    icon: "🐚",
    theme: "Jumping in puddles after the rain",
    focus: "environment, movement verbs, nature vocabulary",
  },
  {
    category: "Community & Movement",
    icon: "🚲",
    theme: "Walking to the library together",
    focus: "community places, collective action, sustainability",
  },
  {
    category: "Community & Movement",
    icon: "🚲",
    theme: "Visiting the marae for kapa haka",
    focus: "community places, collective action, sustainability",
  },
  {
    category: "Community & Movement",
    icon: "🚲",
    theme: "Taking the recycling to the bins",
    focus: "community places, collective action, sustainability",
  },
  {
    category: "Kai and Whānau",
    icon: "🍎",
    theme: "Sharing fruit at morning tea time",
    focus: "gratitude, turn-taking, family and food routines",
  },
  {
    category: "Kai and Whānau",
    icon: "🍎",
    theme: "Baking muffins with mum or dad",
    focus: "gratitude, turn-taking, family and food routines",
  },
  {
    category: "Kai and Whānau",
    icon: "🍎",
    theme: "Saying thank you after kai time",
    focus: "gratitude, turn-taking, family and food routines",
  },
  {
    category: "Feelings & Relationships",
    icon: "🧤",
    theme: "Comforting a friend who is sad",
    focus: "emotions, empathy, social connection",
  },
  {
    category: "Feelings & Relationships",
    icon: "🧤",
    theme: "Saying sorry after bumping someone",
    focus: "emotions, empathy, social connection",
  },
  {
    category: "Feelings & Relationships",
    icon: "🧤",
    theme: "Waving goodbye to whānau in morning",
    focus: "emotions, empathy, social connection",
  },
  {
    category: "Seasons & Aotearoa Life",
    icon: "🐑",
    theme: "Making Matariki stars with our whānau",
    focus: "seasonal traditions, Te Ao Māori, whānau connection",
  },
  {
    category: "Seasons & Aotearoa Life",
    icon: "🐑",
    theme: "Wearing gumboots on a frosty morning",
    focus: "seasonal traditions, Te Ao Māori, whānau connection",
  },
  {
    category: "Seasons & Aotearoa Life",
    icon: "🐑",
    theme: "Collecting leaves in the autumn wind",
    focus: "seasonal traditions, Te Ao Māori, whānau connection",
  },
];

let lastSparkIndex = -1;
let sparkTimerId = null;

const elements = {
  navButtons: Array.from(document.querySelectorAll(".tk-nav-button")),
  errorMessage: document.getElementById("error-message"),
  userId: document.getElementById("user-id-display"),
  generatorView: document.getElementById("generator-view"),
  revisitView: document.getElementById("revisit-view"),
  printView: document.getElementById("print-view"),
  placeholder: document.getElementById("placeholder-message"),
  packDisplay: document.getElementById("pack-display"),
  packTitle: document.getElementById("pack-title"),
  packDate: document.getElementById("pack-date"),
  nzslGloss: document.getElementById("nzsl-gloss"),
  englishSentence: document.getElementById("english-sentence"),
  packCards: document.getElementById("pack-cards"),
  teacherTip: document.getElementById("teacher-tip-text"),
  revisitList: document.getElementById("revisit-list"),
  themeInput: document.getElementById("theme-input"),
  levelSelect: document.getElementById("level-select"),
  keywordsInput: document.getElementById("keywords-input"),
  subjectSelect: document.getElementById("subject-select"),
  generateButton: document.getElementById("generate-button"),
  generateButtonLabel: document.getElementById("generate-button-label"),
  loadingSpinner: document.getElementById("loading-spinner"),
  downloadPdf: document.getElementById("download-pdf"),
  openPrintView: document.getElementById("open-print-view"),
  closePrintView: document.getElementById("close-print-view"),
  printButton: document.getElementById("print-button"),
  printContainer: document.getElementById("print-container"),
  printTitle: document.getElementById("print-title"),
  printSubtitle: document.getElementById("print-subtitle"),
  printNzsl: document.getElementById("print-nzsl"),
  printEnglish: document.getElementById("print-english"),
  printPackCards: document.getElementById("print-pack-cards"),
  sparkChip: document.getElementById("spark-chip"),
  sparkFocus: document.getElementById("spark-focus"),
  surpriseMe: document.getElementById("surprise-me"),
};

const chooseSparkSuggestion = (excludeCurrent = false) => {
  if (!sparkLibrary.length) return null;
  let index = Math.floor(Math.random() * sparkLibrary.length);
  if (excludeCurrent && sparkLibrary.length > 1) {
    let attempts = 0;
    while (index === lastSparkIndex && attempts < 6) {
      index = Math.floor(Math.random() * sparkLibrary.length);
      attempts += 1;
    }
  }
  lastSparkIndex = index;
  return sparkLibrary[index];
};

const applySparkSuggestion = (spark, { updatePlaceholder = true } = {}) => {
  if (!spark || !elements.sparkChip) return;
  const labelParts = [spark.icon, spark.category].filter(Boolean).join(" ");
  elements.sparkChip.textContent = `${labelParts || spark.category} — ${spark.theme}`;
  elements.sparkChip.dataset.category = spark.category;
  elements.sparkChip.dataset.theme = spark.theme;
  elements.sparkChip.dataset.icon = spark.icon || "";
  elements.sparkChip.dataset.focus = spark.focus || "";
  if (elements.sparkFocus) {
    elements.sparkFocus.textContent = spark.focus ? `(Focus: ${spark.focus})` : "";
  }
  if (updatePlaceholder && elements.themeInput && !elements.themeInput.value) {
    elements.themeInput.placeholder = spark.theme;
  }
};

const rotateSparkPrompt = (forceChange = false) => {
  const spark = chooseSparkSuggestion(forceChange);
  applySparkSuggestion(spark);
};

const handleSurpriseMe = () => {
  const spark = chooseSparkSuggestion(true);
  applySparkSuggestion(spark, { updatePlaceholder: true });
  if (spark && elements.themeInput) {
    elements.themeInput.value = spark.theme;
    elements.themeInput.focus({ preventScroll: true });
  }
  setError("");
};

const formatDateTime = (iso) => {
  if (!iso) return "";
  try {
    const date = new Date(iso);
    return date.toLocaleString(undefined, {
      dateStyle: "medium",
      timeStyle: "short",
    });
  } catch {
    return iso;
  }
};

const setError = (message) => {
  if (!message) {
    elements.errorMessage.classList.add("hidden");
    elements.errorMessage.textContent = "";
    return;
  }
  elements.errorMessage.textContent = message;
  elements.errorMessage.classList.remove("hidden");
};

const setUserStatus = (text) => {
  elements.userId.textContent = text;
};

const setLoading = (isLoading, label) => {
  state.generating = isLoading;
  elements.generateButton.disabled = isLoading;
  elements.loadingSpinner.classList.toggle("hidden", !isLoading);
  elements.generateButtonLabel.textContent = isLoading ? label || "Generating pack…" : "Generate Pack";
};

const updateNav = (view) => {
  elements.navButtons.forEach((btn) => {
    const isActive = btn.dataset.view === view;
    btn.classList.toggle("bg-sky-700", isActive);
    btn.classList.toggle("text-white", isActive);
    btn.classList.toggle("shadow-lg", isActive);
    btn.classList.toggle("bg-gray-200", !isActive);
    btn.classList.toggle("text-gray-700", !isActive);
  });
};

const setView = (view) => {
  state.currentView = view;
  updateNav(view);
  elements.generatorView.classList.toggle("hidden", view !== "generator");
  elements.revisitView.classList.toggle("hidden", view !== "revisit");
  elements.printView.classList.toggle("hidden", view !== "print");
  if (view === "print") {
    elements.printContainer.classList.remove("hidden");
  } else {
    elements.printContainer.classList.add("hidden");
  }
  if (view === "revisit") {
    renderRevisitList();
  }
};

const sortPackContent = (pack) => [...pack.pack_content].sort((a, b) => (a.order || 0) - (b.order || 0));

const createCardMarkup = (item) => {
  const stepBadge = `${item.order}️⃣`;
  const imageSrc = item.image_data_url || "";
  return `
    <article class="rounded-xl border border-gray-200 bg-white shadow hover:shadow-lg transition flex flex-col">
      <div class="p-5 space-y-3 flex flex-col flex-grow">
        <div class="flex items-center gap-2">
          <span class="text-lg" aria-hidden="true">${stepBadge}</span>
          <h4 class="text-lg font-semibold text-gray-900">${item.phase}</h4>
        </div>
        <p class="text-sm text-gray-600">${item.pedagogical_purpose}</p>
        <figure class="relative aspect-square w-full overflow-hidden rounded-lg border border-gray-200 bg-gray-100">
          ${
            imageSrc
              ? `<img src="${imageSrc}" alt="${item.phase} illustration" class="h-full w-full object-cover" />`
              : `<span class="absolute inset-0 grid place-content-center text-xs text-gray-400">Image unavailable</span>`
          }
        </figure>
        <p class="text-xs font-medium text-sky-700 uppercase tracking-wide">${item.language_focus}</p>
      </div>
    </article>
  `;
};

const renderPackCards = (pack) => {
  const sorted = sortPackContent(pack);
  elements.packCards.innerHTML = sorted.map(createCardMarkup).join("");
};

const renderPrintCards = (pack) => {
  const sorted = sortPackContent(pack);
  elements.printPackCards.innerHTML = sorted
    .map(
      (item) => `
      <div class="rounded-lg border border-gray-200 p-4 bg-white shadow-sm">
        <header class="flex items-center gap-3 mb-2">
          <span class="text-lg font-bold text-sky-700">${item.order}</span>
          <p class="text-lg font-semibold text-gray-800">${item.phase}</p>
        </header>
        <p class="text-sm text-gray-600 italic mb-3">${item.pedagogical_purpose}</p>
        <div class="h-48 bg-gray-100 border border-gray-200 rounded-lg overflow-hidden flex items-center justify-center">
          ${
            item.image_data_url
              ? `<img src="${item.image_data_url}" alt="${item.phase} illustration" class="h-full w-full object-cover" />`
              : `<span class="text-xs text-gray-400 text-center px-2">Image unavailable</span>`
          }
        </div>
        <p class="text-xs text-sky-700 font-semibold uppercase tracking-wide mt-3">${item.language_focus}</p>
      </div>
    `
    )
    .join("");
};

const renderPack = (pack) => {
  if (!pack) return;
  state.currentPack = pack;

  elements.packTitle.textContent = pack.theme;
  elements.packDate.textContent = `Generated: ${formatDateTime(pack.generated_at)}`;
  elements.nzslGloss.textContent = pack.sentence_nzsl;
  elements.englishSentence.textContent = pack.sentence_en;
  elements.teacherTip.textContent = pack.teacher_tip;

  renderPackCards(pack);
  renderPrintView(pack);

  elements.placeholder.classList.add("hidden");
  elements.packDisplay.classList.remove("hidden");
};

const renderPrintView = (pack) => {
  elements.printTitle.textContent = pack.theme;
  elements.printSubtitle.textContent = `Resource generated ${formatDateTime(pack.generated_at)}`;
  elements.printNzsl.textContent = pack.sentence_nzsl;
  elements.printEnglish.textContent = pack.sentence_en;
  renderPrintCards(pack);
};

const saveHistory = () => {
  try {
    const slimHistory = state.history.slice(0, 7);
    localStorage.setItem(PACK_STORAGE_KEY, JSON.stringify(slimHistory));
  } catch (error) {
    console.warn("Unable to save history to localStorage", error);
  }
};

const loadHistory = () => {
  try {
    const raw = localStorage.getItem(PACK_STORAGE_KEY);
    if (!raw) {
      state.history = [];
      return;
    }
    const parsed = JSON.parse(raw);
    if (Array.isArray(parsed)) {
      state.history = parsed;
    }
  } catch (error) {
    console.warn("Unable to load history from localStorage", error);
    state.history = [];
  }
};

const addPackToHistory = (pack) => {
  state.history = [pack, ...state.history.filter((item) => item.pack_id !== pack.pack_id)].slice(0, 7);
  saveHistory();
  renderRevisitList();
};

const loadPackById = (packId) => {
  const pack = state.history.find((item) => item.pack_id === packId);
  if (!pack) {
    setError("Unable to load saved pack. Please generate a new one.");
    return;
  }
  setView("generator");
  renderPack(pack);
  setError("");
};

const renderRevisitList = () => {
  const container = elements.revisitList;
  container.innerHTML = "";
  if (!state.history.length) {
    const empty = document.createElement("div");
    empty.className = "p-6 text-center text-gray-400 bg-white rounded-xl shadow";
    empty.textContent = "No packs saved yet. Generate one in the Daily Generator.";
    container.appendChild(empty);
    return;
  }

  state.history.forEach((pack) => {
    const card = document.createElement("div");
    card.className =
      "bg-white p-6 rounded-xl shadow-md border-l-4 border-sky-700 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4";

    const info = document.createElement("div");
    const title = document.createElement("p");
    title.className = "text-xl font-semibold text-gray-900";
    title.textContent = pack.theme;
    const date = document.createElement("p");
    date.className = "text-sm text-gray-500";
    date.textContent = `Generated: ${formatDateTime(pack.generated_at)}`;
    const gloss = document.createElement("p");
    gloss.className = "text-sm font-mono text-sky-700";
    gloss.textContent = pack.sentence_nzsl;
    info.append(title, date, gloss);

    const button = document.createElement("button");
    button.className = "bg-pink-600 text-white px-4 py-2 rounded-lg hover:bg-pink-700 transition font-medium";
    button.type = "button";
    button.textContent = "Revisit";
    button.addEventListener("click", () => loadPackById(pack.pack_id));

    card.append(info, button);
    container.appendChild(card);
  });
};

const downloadPdf = () => {
  const pack = state.currentPack;
  if (!pack?.pdf_base64) return;
  const link = document.createElement("a");
  const safeTheme = (pack.theme || "tohu-kaiako").replace(/[^a-z0-9]+/gi, "-").toLowerCase();
  link.href = `data:application/pdf;base64,${pack.pdf_base64}`;
  link.download = `${safeTheme || "learning-pack"}.pdf`;
  link.click();
};

const generatePayload = () => {
  const theme = elements.themeInput.value.trim();
  const keywords = elements.keywordsInput.value.trim();
  const level = elements.levelSelect.value;
  const subject = elements.subjectSelect.value;
  const payload = {
    theme,
    level,
    keywords,
    subject,
  };
  if (subject === "math") {
    payload.activity = "name_the_number";
  }
  if (!keywords) {
    delete payload.keywords;
  }
  return payload;
};

const handleGeneratePack = async () => {
  if (state.generating) return;
  const payload = generatePayload();
  if (!payload.theme) {
    elements.themeInput.focus();
    setError("Please enter a theme or moment to generate your pack.");
    return;
  }

  setError("");
  setLoading(true);

  try {
    const response = await fetch("/api/generate_pack", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      let detail = "Generation failed. Please try again.";
      try {
        const errorData = await response.json();
        detail = errorData.detail || detail;
      } catch {
        const text = await response.text();
        detail = text || detail;
      }
      throw new Error(detail);
    }

    const pack = await response.json();
    addPackToHistory(pack);
    renderPack(pack);
    setError("");
  } catch (error) {
    console.error("Pack generation failed", error);
    setError(error.message || "Generation failed. Please try again.");
  } finally {
    setLoading(false);
  }
};

const initListeners = () => {
  elements.navButtons.forEach((btn) => {
    btn.addEventListener("click", () => setView(btn.dataset.view));
  });
  elements.generateButton.addEventListener("click", handleGeneratePack);
  elements.downloadPdf.addEventListener("click", downloadPdf);
  elements.openPrintView.addEventListener("click", () => {
    if (!state.currentPack) return;
    setView("print");
  });
  elements.closePrintView.addEventListener("click", () => setView("generator"));
  elements.printButton.addEventListener("click", () => window.print());
  elements.themeInput.addEventListener("focus", () => rotateSparkPrompt(true));
  elements.themeInput.addEventListener("blur", () => rotateSparkPrompt(false));
  elements.surpriseMe.addEventListener("click", handleSurpriseMe);
};

const initFirebase = async () => {
  const { firebaseConfig, firebaseAppId } = state.config;
  if (!firebaseConfig || Object.keys(firebaseConfig || {}).length === 0) {
    setUserStatus("Offline mode (Firebase not configured)");
    return;
  }
  try {
    const appModule = await import("https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js");
    const authModule = await import("https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js");

    const app = appModule.initializeApp(firebaseConfig);
    const auth = authModule.getAuth(app);

    if (state.config.firebaseInitialToken) {
      await authModule.signInWithCustomToken(auth, state.config.firebaseInitialToken);
    } else {
      await authModule.signInAnonymously(auth);
    }

    authModule.onAuthStateChanged(auth, (user) => {
      if (user) {
        setUserStatus(`User ID: ${user.uid}`);
        state.firebaseReady = true;
      } else {
        setUserStatus("Signed out");
      }
    });
  } catch (error) {
    console.warn("Firebase setup failed, continuing offline.", error);
    setUserStatus(`Offline mode (app: ${firebaseAppId || "local"})`);
  }
};

const restoreLatestPack = () => {
  if (!state.history.length) return;
  renderPack(state.history[0]);
};

const init = async () => {
  setView("generator");
  initListeners();
  loadHistory();
  renderRevisitList();
  restoreLatestPack();
  initFirebase();
  rotateSparkPrompt(true);
  if (sparkTimerId) {
    clearInterval(sparkTimerId);
  }
  sparkTimerId = setInterval(() => rotateSparkPrompt(true), 20000);
};

init();
