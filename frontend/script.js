// URL de base de l'API. Doit pointer vers votre backend Flask.
// En développement local, ce sera typiquement http://127.0.0.1:5000
const API_BASE_URL = 'http://127.0.0.1:5000';

// ==============================================================================
// Gestion des onglets
// ==============================================================================
function openTab(event, tabName) {
    // Cacher tous les contenus d'onglets
    const tabContents = document.getElementsByClassName('tab-content');
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].style.display = 'none';
    }

    // Désactiver tous les liens d'onglets
    const tabLinks = document.getElementsByClassName('tab-link');
    for (let i = 0; i < tabLinks.length; i++) {
        tabLinks[i].classList.remove('active');
    }

    // Afficher le contenu de l'onglet courant et activer le lien
    document.getElementById(tabName).style.display = 'block';
    event.currentTarget.classList.add('active');
}

// ==============================================================================
// Gestion de l'état (chargement et erreurs)
// ==============================================================================
const loadingIndicator = document.getElementById('loading-indicator');
const errorBox = document.getElementById('error-box');

function showLoading(show) {
    loadingIndicator.classList.toggle('hidden', !show);
}

function showError(message) {
    errorBox.textContent = message;
    errorBox.classList.remove('hidden');
}

function hideError() {
    errorBox.classList.add('hidden');
}

// ==============================================================================
// Logique d'appel à l'API
// ==============================================================================
async function callApi(endpoint, body) {
    showLoading(true);
    hideError();
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Erreur HTTP: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        showError(`Erreur de communication avec l'API: ${error.message}`);
        return null;
    } finally {
        showLoading(false);
    }
}

// ==============================================================================
// Logique spécifique à chaque onglet
// ==============================================================================

// --- Analyse de Sentiment ---
const sentimentBtn = document.getElementById('sentiment-btn');
const sentimentInput = document.getElementById('sentiment-input');
const sentimentOutput = document.getElementById('sentiment-output');

sentimentBtn.addEventListener('click', async () => {
    const text = sentimentInput.value.trim();
    if (!text) return;
    const result = await callApi('/predict/sentiment', { text });
    if (result) {
        // Formatte le résultat pour un affichage clair
        const formattedResult = Object.entries(result.prediction)
            .map(([label, score]) => `${label}: ${score.toFixed(4)}`)
            .join('\n');
        sentimentOutput.textContent = formattedResult;
    }
});

// --- Question-Réponse ---
const qaBtn = document.getElementById('qa-btn');
const qaContext = document.getElementById('qa-context');
const qaQuestion = document.getElementById('qa-question');
const qaOutput = document.getElementById('qa-output');

qaBtn.addEventListener('click', async () => {
    const context = qaContext.value.trim();
    const question = qaQuestion.value.trim();
    if (!context || !question) return;
    const result = await callApi('/predict/qa', { context, question });
    if (result) {
        qaOutput.textContent = result.answer;
    }
});

// --- Génération de Texte ---
const generateBtn = document.getElementById('generate-btn');
const generatePrompt = document.getElementById('generate-prompt');
const generateOutput = document.getElementById('generate-output');
const maxLengthSlider = document.getElementById('max-length');
const maxLengthValue = document.getElementById('max-length-value');

// Mettre à jour la valeur affichée du slider
maxLengthSlider.addEventListener('input', (e) => {
    maxLengthValue.textContent = e.target.value;
});

generateBtn.addEventListener('click', async () => {
    const prompt = generatePrompt.value.trim();
    if (!prompt) return;
    const max_length = parseInt(maxLengthSlider.value, 10);
    // Note: la température est laissée à sa valeur par défaut du backend
    const result = await callApi('/predict/generate', { prompt, max_length });
    if (result) {
        generateOutput.textContent = result.generated_text;
    }
}); 