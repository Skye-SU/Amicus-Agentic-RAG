const $ = (s) => document.querySelector(s);
const $$ = (s) => document.querySelectorAll(s);

let currentMode = 'chat';
let isLoading = false;
let inConversation = false;
let conversationHistory = [];
let homeStateToken = 0;

const welcomeEl      = $('#welcome');
const chatAreaEl      = $('#chat-area');
const messagesEl      = $('#messages');
const quizAreaEl      = $('#quiz-area');
const chatFooterEl    = $('#chat-footer');
const chatInputEl     = $('#chat-input');
const sendBtnEl       = $('#send-btn');
const inputBoxEl      = $('#input-box');
const welcomeSlot     = $('#welcome-input-slot');
const footerSlot      = $('#footer-input-slot');
const sidebarPanel    = $('#sidebar-panel');
const sidebarOverlay  = $('#sidebar-overlay');
const homeBrandEl     = $('#home-brand');
const sidebarHomeBrandEl = $('#sidebar-home-brand');
const quizTopicEl     = $('#quiz-topic');
const quizCountEl     = $('#quiz-count');
const quizResultEl    = $('#quiz-result');

const DEFAULT_SOURCE_PRESENTATION = {
    panelTitle: 'Retrieved materials',
    panelNote: 'These excerpts were retrieved for this response and may be relevant context rather than proof that every statement above was grounded in them.',
    excerptLabel: 'Retrieved excerpt',
    confidenceState: 'retrieved',
    statusLabel: 'Retrieved context',
};

const RELATED_MATERIALS_PRESENTATION = {
    panelTitle: 'Related materials',
    panelNote: 'These materials were retrieved as potentially relevant context. They were not verified as the evidence used to produce the answer.',
    excerptLabel: 'Related excerpt',
    confidenceState: 'related',
    statusLabel: 'Related only',
};

const GROUNDED_SOURCE_PRESENTATION = {
    panelTitle: 'Grounding materials',
    panelNote: 'The backend marked these excerpts as grounding evidence for this answer.',
    excerptLabel: 'Grounding excerpt',
    confidenceState: 'grounded',
    statusLabel: 'Reliable grounding',
};

const RELIABLE_GROUNDING_MODES = new Set([
    'agent_intermediate_steps',
    'direct_rag_context',
    'grounded',
    'grounding',
    'grounded_answer',
    'grounded_response',
    'answer_grounded',
    'response_grounded',
    'verified_grounding',
    'direct_grounding',
]);

const RELATED_ONLY_GROUNDING_MODES = new Set([
    'related_materials_only',
]);

const ALLOWED_MARKDOWN_TAGS = new Set([
    'a',
    'blockquote',
    'br',
    'code',
    'del',
    'em',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'hr',
    'input',
    'li',
    'ol',
    'p',
    'pre',
    'strong',
    'table',
    'tbody',
    'td',
    'th',
    'thead',
    'tr',
    'ul',
]);

const DROP_CONTENT_TAGS = new Set([
    'embed',
    'iframe',
    'link',
    'meta',
    'object',
    'script',
    'style',
]);

document.addEventListener('DOMContentLoaded', () => {
    setDynamicGreeting();
    welcomeSlot.appendChild(inputBoxEl);
    setupModeToggle();
    setupHomeNavigation();
    setupChatInput();
    setupQuickActions();
    setupQuiz();
    setupSidebar();
});

function setDynamicGreeting() {
    const line1 = document.getElementById('greeting-line1');
    const line2 = document.getElementById('greeting-line2');

    const hkHour = parseInt(
        new Intl.DateTimeFormat('en-US', {
            hour: 'numeric',
            hour12: false,
            timeZone: 'Asia/Hong_Kong'
        }).format(new Date())
    );
    let timeGreeting;
    if (hkHour >= 5 && hkHour < 12) timeGreeting = 'Good morning';
    else if (hkHour >= 12 && hkHour < 18) timeGreeting = 'Good afternoon';
    else timeGreeting = 'Good evening';

    const iconHtml = '<img src="/static/amicus-avatar.jpeg" alt="Amicus Avatar" style="height:36px; width:auto; vertical-align:middle; margin-right:12px; margin-bottom:6px;">';

    line1.innerHTML = iconHtml + timeGreeting;
    line2.textContent = 'Begin your computational law journey';
}

// ─── Sidebar ───

function setupSidebar() {
    const toggle  = $('#sidebar-toggle');
    const close_  = $('#sidebar-close');
    const mobile  = $('#mobile-menu-btn');

    function open()  { sidebarPanel.classList.add('open');    sidebarOverlay.classList.add('active'); }
    function shut()  { sidebarPanel.classList.remove('open'); sidebarOverlay.classList.remove('active'); }

    toggle.addEventListener('click', () => sidebarPanel.classList.contains('open') ? shut() : open());
    close_.addEventListener('click', shut);
    sidebarOverlay.addEventListener('click', shut);
    mobile.addEventListener('click', open);
}

function syncModeButtons(mode) {
    $$('.mode-btn').forEach(btn => {
        const isActive = btn.dataset.mode === mode;
        btn.classList.toggle('active', isActive);
        btn.setAttribute('aria-selected', String(isActive));
    });
}

function renderCurrentView() {
    if (currentMode === 'quiz') {
        welcomeEl.classList.add('hidden');
        chatAreaEl.classList.add('hidden');
        chatFooterEl.classList.add('hidden');
        quizAreaEl.classList.remove('hidden');
        return;
    }

    quizAreaEl.classList.add('hidden');
    if (inConversation) {
        welcomeEl.classList.add('hidden');
        chatAreaEl.classList.remove('hidden');
        chatFooterEl.classList.remove('hidden');
        footerSlot.appendChild(inputBoxEl);
    } else {
        welcomeEl.classList.remove('hidden');
        welcomeEl.classList.remove('fade-out');
        chatAreaEl.classList.add('hidden');
        chatFooterEl.classList.add('hidden');
        welcomeSlot.appendChild(inputBoxEl);
    }
}

function closeSidebar() {
    sidebarPanel.classList.remove('open');
    sidebarOverlay.classList.remove('active');
}

function resetComposer() {
    chatInputEl.value = '';
    chatInputEl.style.height = 'auto';
    chatInputEl.placeholder = 'How can I help you learn today?';
    sendBtnEl.classList.remove('active');
}

function returnToHome() {
    homeStateToken += 1;
    currentMode = 'chat';
    isLoading = false;
    inConversation = false;
    conversationHistory = [];
    messagesEl.innerHTML = '';
    if (quizTopicEl) quizTopicEl.value = '';
    if (quizCountEl) quizCountEl.value = '1';
    if (quizResultEl) quizResultEl.innerHTML = '';
    resetComposer();
    syncModeButtons('chat');
    renderCurrentView();
    closeSidebar();
}

function setupHomeNavigation() {
    [homeBrandEl, sidebarHomeBrandEl].filter(Boolean).forEach(node => {
        node.addEventListener('click', returnToHome);
        if (node.tagName !== 'BUTTON') {
            node.addEventListener('keydown', (event) => {
                if (event.key === 'Enter' || event.key === ' ') {
                    event.preventDefault();
                    returnToHome();
                }
            });
        }
    });
}

// ─── Mode Toggle ───

function setupModeToggle() {
    $$('.mode-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const mode = btn.dataset.mode;
            if (mode === currentMode) return;
            currentMode = mode;
            syncModeButtons(mode);
            renderCurrentView();
        });
    });
}

// ─── Chat Input ───

function setupChatInput() {
    chatInputEl.addEventListener('input', () => {
        chatInputEl.style.height = 'auto';
        chatInputEl.style.height = Math.min(chatInputEl.scrollHeight, 180) + 'px';
        sendBtnEl.classList.toggle('active', chatInputEl.value.trim().length > 0);
    });
    chatInputEl.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
    });
    sendBtnEl.addEventListener('click', () => sendMessage());
}

function setupQuickActions() {
    $$('.pill').forEach(p => p.addEventListener('click', () => sendMessage(p.dataset.question)));
}

async function transitionToChat() {
    if (inConversation) return;
    inConversation = true;
    currentMode = 'chat';
    syncModeButtons('chat');
    welcomeEl.classList.add('fade-out');
    await sleep(280);
    welcomeEl.classList.add('hidden');
    chatAreaEl.classList.remove('hidden');
    chatFooterEl.classList.remove('hidden');
    footerSlot.appendChild(inputBoxEl);
    chatInputEl.placeholder = 'Ask Amicus';
    chatInputEl.focus();
}

// ─── Send Message ───

async function sendMessage(textOverride) {
    const message = textOverride || chatInputEl.value.trim();
    if (!message || isLoading) return;
    const requestToken = homeStateToken;

    chatInputEl.value = '';
    chatInputEl.style.height = 'auto';
    sendBtnEl.classList.remove('active');

    await transitionToChat();
    appendUserMessage(message);

    conversationHistory.push({ role: 'user', content: message });

    isLoading = true;
    const thinkingEl = appendThinking();

    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message,
                history: conversationHistory.slice(0, -1),
            }),
        });
        const data = await res.json();
        if (requestToken !== homeStateToken) {
            clearThinking(thinkingEl);
            return;
        }
        clearThinking(thinkingEl);

        let answer = data.answer || '';
        if (answer.includes('Agent stopped due to') || answer.includes('iteration limit') || answer.includes('time limit')) {
            answer = "🪶 I took a bit too long searching — let me give you a shorter answer. Could you try rephrasing your question more specifically? For example, instead of a broad topic, ask about one particular concept.";
        }

        const materialPanelState = extractMaterialPanelState(data);
        await appendAssistantMessage(answer, materialPanelState.materials, materialPanelState.sourcePresentation);

        conversationHistory.push({ role: 'assistant', content: answer });
    } catch {
        if (requestToken !== homeStateToken) {
            clearThinking(thinkingEl);
            return;
        }
        clearThinking(thinkingEl);
        await appendAssistantMessage('A network error occurred. Please check your connection and try again.', []);
    } finally {
        if (requestToken === homeStateToken) {
            isLoading = false;
        }
    }
}

// ─── Messages ───

function appendUserMessage(text) {
    const msg = mk('div', 'message user');
    const body = mk('div', 'message-content');
    body.textContent = text;
    msg.appendChild(body);
    messagesEl.appendChild(msg);
    scrollToBottom();
}

async function appendAssistantMessage(text, sources, sourcePresentation = DEFAULT_SOURCE_PRESENTATION) {
    const msg = mk('div', 'message assistant');
    const body = mk('div', 'message-content');
    const textEl = mk('div', 'markdown-body');
    body.appendChild(textEl);
    msg.appendChild(body);
    messagesEl.appendChild(msg);

    await streamingTypewriter(textEl, text);

    if (sources && sources.length) {
        const sw = buildSourcesWidget(sources, sourcePresentation);
        sw.style.opacity = '0';
        sw.style.transition = 'opacity 0.35s ease';
        body.appendChild(sw);
        await sleep(30);
        sw.style.opacity = '1';
    }
}

// ─── Streaming Markdown Typewriter ───

async function streamingTypewriter(container, fullText) {
    const words = fullText.split(/(\s+)/);
    let acc = '';
    let userScrolled = false;
    let wordCount = 0;
    let lastRenderTime = 0;

    function onScroll() { userScrolled = !isNearBottom(); }
    chatAreaEl.addEventListener('scroll', onScroll);

    for (let i = 0; i < words.length; i++) {
        acc += words[i];
        if (!words[i].trim()) continue;

        wordCount++;
        const now = performance.now();

        if (now - lastRenderTime > 45 || i >= words.length - 1) {
            container.innerHTML = renderMarkdown(acc);
            decorateAssistantMarkdown(container);
            lastRenderTime = now;
            if (!userScrolled) scrollToBottom();
        }
        await sleep(10);
    }

    container.innerHTML = renderMarkdown(fullText);
    decorateAssistantMarkdown(container);

    if (typeof hljs !== 'undefined') {
        container.querySelectorAll('pre code').forEach(block => {
            hljs.highlightElement(block);
        });
    }

    if (!userScrolled) scrollToBottom();
    chatAreaEl.removeEventListener('scroll', onScroll);
}

function isNearBottom() {
    return chatAreaEl.scrollHeight - chatAreaEl.scrollTop - chatAreaEl.clientHeight < 80;
}

// ─── Calm Thinking Indicator ───

const TRIVIA_FACTS = [
    'Did you know? Python was named after Monty Python\'s Flying Circus, not the snake.',
    'Fun fact: In Python, indentation isn\'t just style — it\'s syntax. One wrong space can break your entire program.',
    'In case you wondered: The "else" clause on a Python for-loop only runs if the loop completes without hitting "break."',
    'Good to know: The first computer bug was an actual moth found in a Harvard Mark II computer in 1947.',
    'Here\'s a good one: Python\'s creator, Guido van Rossum, was called the "Benevolent Dictator for Life" of the language — until he stepped down in 2018.',
    'Quick aside: A list in Python is mutable, but a tuple is not. Think of it as a draft contract vs. a signed one.',
    'Did you know? The "f" in f-strings stands for "formatted." They were introduced in Python 3.6.',
    'For the record: Python uses zero-based indexing — the first item is at position 0, not 1. This trips up almost every beginner.',
    'Fun fact: A p-value of 0.05 does not mean there is a 5% chance the null hypothesis is true.',
    'Good to know: The term "regression" in statistics comes from Francis Galton\'s observation that children\'s heights tend to "regress" toward the population mean.',
    'Here\'s a good one: "Correlation does not imply causation" was first articulated by Karl Pearson in the early 1900s.',
    'Quick aside: The standard deviation tells you how spread out your data is — a small value means the data points cluster tightly around the mean.',
    'In case you wondered: The normal distribution is sometimes called the "bell curve," but not all bell-shaped distributions are normal.',
    'For the record: A Type I error means convicting an innocent person. A Type II error means letting a guilty person go free.',
    'Did you know? The "degrees of freedom" in a statistical test is roughly the number of values free to vary after constraints are applied.',
    'Fun fact: Chinese text has no spaces between words, making tokenization fundamentally harder than in English.',
    'Good to know: The word "tokenization" in NLP has nothing to do with cryptocurrency tokens.',
    'Here\'s a good one: spaCy can process over 10,000 documents per second — faster than most humans can read a single paragraph.',
    'Quick aside: Named Entity Recognition (NER) can automatically identify people, places, and organizations in legal texts.',
    'In case you wondered: Stop words like "the," "is," and "at" are often removed in NLP because they carry little meaning on their own.',
    'For the record: TF-IDF stands for "Term Frequency–Inverse Document Frequency" — it measures how important a word is to a document in a collection.',
    'Did you know? The first known legal code, the Code of Ur-Nammu, was written around 2100 BCE in ancient Sumer.',
    'Fun fact: The Chinese judiciary publishes over 20 million court rulings online — one of the largest legal open datasets in the world.',
    'Good to know: Computer-assisted legal research can process more court rulings in one hour than a paralegal can read in an entire year.',
    'Did you know? In common law, the "reasonable person" standard has no single agreed-upon definition across all jurisdictions.',
    'Here\'s a good one: The concept of "precedent" — following earlier court decisions — dates back to 12th-century English law.',
    'In case you wondered: Legal NLP researchers often build "blacklists" of common boilerplate terms to filter noise from court ruling datasets.',
    'Quick aside: Regular expressions, or regex, were invented by mathematician Stephen Kleene in the 1950s and are still used in modern NLP pipelines.',
    'For the record: "Amicus" is Latin for "friend" — the same root as "amicus curiae," meaning a friend of the court.',
    'Fun fact: In legal informatics, a single misplaced comma in a statute has led to multi-million dollar lawsuits over differing interpretations.',
];

function appendThinking() {
    const msg = mk('div', 'message assistant');
    msg.innerHTML = `<div class="message-content">
        <span class="thinking-text">Amicus is thinking<span class="animated-dots"><span>.</span><span>.</span><span>.</span></span></span>
        <div class="trivia-text"></div>
    </div>`;
    messagesEl.appendChild(msg);
    scrollToBottom();

    const triviaNode = msg.querySelector('.trivia-text');

    const usedIndices = new Set();
    function showRandomTrivia() {
        if (usedIndices.size >= TRIVIA_FACTS.length) usedIndices.clear();
        let ri;
        do { ri = Math.floor(Math.random() * TRIVIA_FACTS.length); } while (usedIndices.has(ri));
        usedIndices.add(ri);
        triviaNode.style.opacity = '0';
        setTimeout(() => {
            triviaNode.textContent = TRIVIA_FACTS[ri];
            triviaNode.style.opacity = '1';
        }, 300);
    }

    msg._triviaTimeout = setTimeout(() => {
        showRandomTrivia();
        msg._triviaInterval = setInterval(showRandomTrivia, 5000);
    }, 2000);

    return msg;
}

function clearThinking(node) {
    if (node._triviaInterval) clearInterval(node._triviaInterval);
    if (node._triviaTimeout) clearTimeout(node._triviaTimeout);
    node.remove();
}

// ─── Sources ───

const SOURCE_MOJIBAKE_REPLACEMENTS = [
    ['â€™', '\''],
    ['â€œ', '"'],
    ['â€\u009d', '"'],
    ['â€˜', '\''],
    ['â€“', '-'],
    ['â€”', '-'],
    ['â€¦', '...'],
    ['Â£', '£'],
    ['Â¥', '¥'],
    ['Â', ''],
];

function repairSourceEncoding(value) {
    let text = String(value || '').replace(/\u00a0/g, ' ').replace(/\ufeff/g, '');
    SOURCE_MOJIBAKE_REPLACEMENTS.forEach(([broken, fixed]) => {
        text = text.replaceAll(broken, fixed);
    });
    return text.normalize ? text.normalize('NFC') : text;
}

function cleanSourceText(text) {
    return repairSourceEncoding(text)
        .replace(/\*\*(.*?)\*\*/g, '$1')
        .replace(/__(.*?)__/g, '$1')
        .replace(/`([^`]+)`/g, '$1')
        .replace(/\\_/g, '_');
}

function normalizeSourceText(text) {
    return cleanSourceText(text).replace(/\s+/g, ' ').trim();
}

function truncateSourceText(text, limit = 280) {
    const normalized = normalizeSourceText(text);
    if (normalized.length <= limit) return normalized;

    const clipped = normalized.slice(0, limit);
    const sentenceStop = Math.max(clipped.lastIndexOf('. '), clipped.lastIndexOf('; '));
    const wordStop = clipped.lastIndexOf(' ');
    const stop = sentenceStop > limit * 0.55 ? sentenceStop + 1 : (wordStop > limit * 0.7 ? wordStop : limit);
    return `${clipped.slice(0, stop).trim()}...`;
}

function humanizeIdentifier(value) {
    const stem = String(value || '')
        .replace(/\.[a-z0-9]+$/i, '')
        .split(/[\\/]/)
        .pop();
    const tokens = stem.split(/[_\-\s]+/).filter(Boolean);

    return tokens.map(token => {
        const lowered = token.toLowerCase();
        if (['nlp', 'uk', 'cn', 'etl'].includes(lowered)) return token.toUpperCase();
        if (lowered === 'py4e') return 'PY4E';
        if (/^\d+$/.test(token)) return token;
        return token.charAt(0).toUpperCase() + token.slice(1).toLowerCase();
    }).join(' ') || 'Reference';
}

function looksLikeSourceNoise(text) {
    const value = normalizeSourceText(text).toLowerCase();
    if (!value) return true;
    if (value.startsWith('xml version=') || value.startsWith('<?xml') || value.startsWith('function ') || value.startsWith('var ')) {
        return true;
    }
    if ((value.match(/[a-z]/g) || []).length < 3) {
        return true;
    }
    return /[{}<>]{2,}/.test(value);
}

function prettifySectionTitle(text) {
    const cleaned = normalizeSourceText(text).replace(/^#{1,6}\s*/, '');
    if (!cleaned || looksLikeSourceNoise(cleaned)) return '';
    if (cleaned.length <= 88) return cleaned;
    return `${cleaned.slice(0, 85).trim()}...`;
}

function parseSourceFields(text) {
    const fields = {};
    const plainLines = [];

    repairSourceEncoding(text)
        .split(/\n+/)
        .map(line => cleanSourceText(line).trim())
        .forEach(line => {
            if (!line) return;

            const fieldMatch = line.match(/^([A-Za-z][A-Za-z ]{1,30}):\s*(.+)$/);
            if (fieldMatch) {
                const key = fieldMatch[1].toLowerCase().replace(/\s+/g, '_');
                fields[key] = fieldMatch[2].trim();
                return;
            }

            if (!looksLikeSourceNoise(line)) {
                plainLines.push(line);
            }
        });

    return { fields, plainText: plainLines.join(' ') };
}

function dedupeItems(items) {
    const seen = new Set();
    return items.filter(item => {
        const normalized = normalizeSourceText(item);
        if (!normalized || seen.has(normalized)) return false;
        seen.add(normalized);
        return true;
    });
}

function normalizeGroundingMode(value) {
    return normalizeSourceText(value).toLowerCase().replace(/[\s-]+/g, '_');
}

function isExplicitGroundingSignal(value) {
    return RELIABLE_GROUNDING_MODES.has(normalizeGroundingMode(value));
}

function normalizeMaterialList(materials) {
    if (!Array.isArray(materials)) return [];
    return materials.filter(item => item && typeof item === 'object' && (item.source || item.text));
}

function extractGroundingMode(payload) {
    const rawMode = [
        payload?.grounding_mode,
        payload?.groundingMode,
        payload?.source_mode,
        payload?.sourceMode,
    ].find(value => typeof value === 'string' && value.trim());

    return normalizeGroundingMode(rawMode || '');
}

function extractHasReliableSources(payload, groundingMode) {
    if (typeof payload?.has_reliable_sources === 'boolean') {
        return payload.has_reliable_sources;
    }
    if (typeof payload?.hasReliableSources === 'boolean') {
        return payload.hasReliableSources;
    }
    return RELIABLE_GROUNDING_MODES.has(groundingMode);
}

function buildSourcePresentation({
    hasReliableSources,
    groundingMode,
    showingRelatedMaterialsOnly,
    sourceBasis,
}) {
    let presentation;

    if (hasReliableSources) {
        presentation = { ...GROUNDED_SOURCE_PRESENTATION };
    } else if (showingRelatedMaterialsOnly || RELATED_ONLY_GROUNDING_MODES.has(groundingMode)) {
        presentation = { ...RELATED_MATERIALS_PRESENTATION };
    } else {
        presentation = { ...DEFAULT_SOURCE_PRESENTATION };
    }

    if (typeof sourceBasis === 'string' && sourceBasis.trim()) {
        presentation.panelNote = sourceBasis.trim();
    }

    return presentation;
}

function extractMaterialPanelState(payload) {
    const sources = normalizeMaterialList(payload?.sources);
    const relatedMaterials = normalizeMaterialList(payload?.related_materials || payload?.relatedMaterials);
    const materials = sources.length ? sources : relatedMaterials;
    const groundingMode = extractGroundingMode(payload);
    const hasReliableSources = extractHasReliableSources(payload, groundingMode);
    const showingRelatedMaterialsOnly = !sources.length && relatedMaterials.length > 0;
    const sourceBasis = payload?.source_basis || payload?.sourceBasis || '';
    const sourcePresentationOverride = [
        payload?.source_presentation,
        payload?.sourcePresentation,
    ].map(resolveSourcePresentation).find(Boolean);

    const sourcePresentation = buildSourcePresentation({
        hasReliableSources,
        groundingMode,
        showingRelatedMaterialsOnly,
        sourceBasis,
    });

    if (sourcePresentationOverride) {
        if (typeof sourcePresentationOverride.panelTitle === 'string' && sourcePresentationOverride.panelTitle.trim()) {
            sourcePresentation.panelTitle = sourcePresentationOverride.panelTitle.trim();
        }
        if (typeof sourcePresentationOverride.panelNote === 'string' && sourcePresentationOverride.panelNote.trim()) {
            sourcePresentation.panelNote = sourcePresentationOverride.panelNote.trim();
        }
        if (typeof sourcePresentationOverride.excerptLabel === 'string' && sourcePresentationOverride.excerptLabel.trim()) {
            sourcePresentation.excerptLabel = sourcePresentationOverride.excerptLabel.trim();
        }
    }

    return {
        materials,
        sourcePresentation,
    };
}

function resolveSourcePresentation(candidate) {
    if (typeof candidate === 'string') {
        return buildSourcePresentation({
            hasReliableSources: isExplicitGroundingSignal(candidate),
            groundingMode: normalizeGroundingMode(candidate),
            showingRelatedMaterialsOnly: false,
            sourceBasis: '',
        });
    }

    if (!candidate || typeof candidate !== 'object') {
        return null;
    }

    const groundingMode = normalizeGroundingMode(
        [
            candidate.mode,
            candidate.status,
            candidate.type,
            candidate.grounding_mode,
            candidate.groundingMode,
            candidate.source_mode,
            candidate.sourceMode,
        ].find(value => typeof value === 'string' && value.trim()) || ''
    );

    const hasReliableSources = typeof candidate.has_reliable_sources === 'boolean'
        ? candidate.has_reliable_sources
        : typeof candidate.hasReliableSources === 'boolean'
            ? candidate.hasReliableSources
            : typeof candidate.grounded === 'boolean'
                ? candidate.grounded
        : typeof candidate.is_grounded === 'boolean'
            ? candidate.is_grounded
            : typeof candidate.isGrounded === 'boolean'
                ? candidate.isGrounded
                : RELIABLE_GROUNDING_MODES.has(groundingMode);

    const showingRelatedMaterialsOnly = RELATED_ONLY_GROUNDING_MODES.has(groundingMode);
    const presentation = buildSourcePresentation({
        hasReliableSources,
        groundingMode,
        showingRelatedMaterialsOnly,
        sourceBasis: candidate.source_basis || candidate.sourceBasis || candidate.panel_note || candidate.panelNote || candidate.note || candidate.description || '',
    });

    const customTitle = candidate.panel_title || candidate.panelTitle || candidate.title || candidate.label;
    const customExcerptLabel = candidate.excerpt_label || candidate.excerptLabel;

    if (typeof customTitle === 'string' && customTitle.trim()) {
        presentation.panelTitle = customTitle.trim();
    }
    if (typeof customExcerptLabel === 'string' && customExcerptLabel.trim()) {
        presentation.excerptLabel = customExcerptLabel.trim();
    }

    return presentation;
}

function parseSourceReference(rawSource) {
    const info = {
        raw: normalizeSourceText(rawSource),
        title: 'Reference',
        badge: 'Source',
        meta: [],
        context: '',
        kind: 'generic',
    };

    let source = info.raw;
    if (!source) return info;

    const articleMatch = source.match(/^(.*?)(?:,\s*article:\s*([A-Za-z0-9_.-]+))$/i);
    if (articleMatch) {
        source = articleMatch[1].trim();
        info.meta.push(humanizeIdentifier(articleMatch[2]));
    }

    const pageMatch = source.match(/^(.*?)(?:,\s*page\s*(\d+))$/i);
    if (pageMatch) {
        source = pageMatch[1].trim();
        info.meta.push(`Page ${pageMatch[2]}`);
        info.badge = 'PDF';
        info.kind = 'pdf';
    }

    const cellMatch = source.match(/^(.*?)(?:,\s*cell\s*(\d+))$/i);
    if (cellMatch) {
        source = cellMatch[1].trim();
        info.meta.push(`Cell ${cellMatch[2]}`);
        info.badge = 'Notebook';
        info.kind = 'ipynb';
    }

    const sectionMatch = source.match(/^(.*?)(?:,\s*section:\s*(.+))$/i);
    if (sectionMatch) {
        source = sectionMatch[1].trim();
        info.kind = 'md';
        info.badge = 'Markdown';
        info.context = prettifySectionTitle(sectionMatch[2]);
    }

    const fileMatch = source.match(/^(.+)\.(pdf|docx?|ipynb|md|py)$/i);
    if (fileMatch) {
        const extension = fileMatch[2].toLowerCase();
        info.kind = extension;
        info.title = humanizeIdentifier(fileMatch[1]);
        if (extension === 'pdf') info.badge = 'PDF';
        else if (extension === 'ipynb') info.badge = 'Notebook';
        else if (extension === 'docx' || extension === 'doc') info.badge = 'Handout';
        else if (extension === 'md') info.badge = 'Markdown';
        else if (extension === 'py') info.badge = 'Authority';
    } else {
        info.title = source;
        info.badge = /act|code|article|guiding case|v\s/i.test(source) ? 'Authority' : 'Source';
    }

    info.meta = dedupeItems(info.meta);
    return info;
}

function selectSourcePreview(parsedText) {
    const { fields, plainText } = parsedText;
    const priority = [
        fields.text,
        fields.key_holding,
        fields.court_reasoning,
        fields.dispute,
        fields.financial_outcome,
        fields.outcome,
        fields.ratio,
        fields.quoted_passage,
        plainText,
    ];

    const chosen = priority.find(value => normalizeSourceText(value));
    return truncateSourceText(chosen || 'No excerpt available.');
}

function buildSourceCardData(source) {
    const parsedRef = parseSourceReference(source.source);
    const parsedText = parseSourceFields(source.text);
    const { fields } = parsedText;

    let title = parsedRef.title;
    if (fields.authority && parsedRef.kind === 'py') {
        title = fields.authority;
    }
    if (/^legal_data\.py\b/i.test(parsedRef.raw)) {
        title = fields.authority || fields.case || fields.title || title;
    }

    const context = dedupeItems([
        parsedRef.context,
        title !== fields.title ? fields.title : '',
    ])[0] || '';

    const meta = dedupeItems([
        fields.jurisdiction,
        fields.court,
        fields.year,
        ...parsedRef.meta,
    ]);

    const tags = (fields.tags || '')
        .split(',')
        .map(tag => normalizeSourceText(tag))
        .filter(Boolean)
        .slice(0, 2);

    return {
        badge: fields.material_type || parsedRef.badge,
        title: title || 'Reference',
        context,
        meta: dedupeItems([...meta, ...tags]),
        preview: selectSourcePreview(parsedText),
    };
}

function formatSourceName(rawName) {
    return parseSourceReference(rawName).title;
}

function buildSourcesWidget(sources, sourcePresentation = DEFAULT_SOURCE_PRESENTATION) {
    const wrapper = mk('section', 'sources-wrapper');
    wrapper.dataset.confidence = sourcePresentation.confidenceState || 'retrieved';
    const header = mk('div', 'sources-header');
    const summary = mk('div', 'sources-summary');
    const summaryTop = mk('div', 'sources-summary-top');
    const title = mk('div', 'sources-title');
    title.textContent = `${sourcePresentation.panelTitle} (${sources.length})`;
    const status = mk('span', 'sources-status');
    status.textContent = sourcePresentation.statusLabel || 'Retrieved context';
    const note = mk('div', 'sources-note');
    note.textContent = sourcePresentation.panelNote;

    const toggle = mk('button', 'sources-toggle');
    toggle.type = 'button';

    const list = mk('div', 'sources-list expanded');
    let isExpanded = true;

    function syncToggle() {
        toggle.textContent = isExpanded ? 'Hide' : 'Show';
        toggle.classList.toggle('expanded', isExpanded);
        toggle.setAttribute('aria-expanded', String(isExpanded));
        list.classList.toggle('expanded', isExpanded);
    }

    summaryTop.appendChild(title);
    summaryTop.appendChild(status);
    summary.appendChild(summaryTop);
    summary.appendChild(note);
    header.appendChild(summary);
    header.appendChild(toggle);

    sources.forEach(src => {
        const cardData = buildSourceCardData(src);
        const card = mk('article', 'source-card');
        const top = mk('div', 'source-card-top');
        const badge = mk('span', 'source-badge');
        badge.textContent = cardData.badge;

        const titleWrap = mk('div', 'source-title-wrap');
        const name = mk('div', 'source-name');
        name.textContent = cardData.title;
        titleWrap.appendChild(name);

        if (cardData.context) {
            const context = mk('div', 'source-context');
            context.textContent = cardData.context;
            titleWrap.appendChild(context);
        }

        top.appendChild(badge);
        top.appendChild(titleWrap);
        card.appendChild(top);

        if (cardData.meta.length) {
            const meta = mk('div', 'source-meta');
            cardData.meta.forEach(item => {
                const metaItem = mk('span', 'source-meta-item');
                metaItem.textContent = item;
                meta.appendChild(metaItem);
            });
            card.appendChild(meta);
        }

        const textLabel = mk('div', 'source-text-label');
        textLabel.textContent = sourcePresentation.excerptLabel;
        const text = mk('div', 'source-text');
        text.textContent = cardData.preview;

        card.appendChild(textLabel);
        card.appendChild(text);
        list.appendChild(card);
    });

    toggle.addEventListener('click', () => {
        isExpanded = !isExpanded;
        syncToggle();
    });

    syncToggle();
    wrapper.appendChild(header);
    wrapper.appendChild(list);
    return wrapper;
}

// ═══════════════════════════════════
//  QUIZ
// ═══════════════════════════════════

function setupQuiz() {
    const genBtn   = $('#quiz-generate');
    const topicIn  = $('#quiz-topic');
    const countSel = $('#quiz-count');
    const resultEl = $('#quiz-result');

    genBtn.addEventListener('click', run);
    topicIn.addEventListener('keydown', (e) => { if (e.key === 'Enter') run(); });

    async function run() {
        const topic = topicIn.value.trim();
        if (!topic || genBtn.disabled) return;

        genBtn.disabled = true;
        genBtn.textContent = 'Generating...';
        resultEl.innerHTML = '<span class="thinking-text">Generating quiz questions<span class="animated-dots"><span>.</span><span>.</span><span>.</span></span></span>';

        try {
            const res = await fetch('/api/quiz', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic, num_questions: parseInt(countSel.value) }),
            });
            const data = await res.json();
            const parsed = parseQuiz(data.quiz);
            resultEl.innerHTML = '';
            if (parsed.length > 0) {
                resultEl.appendChild(renderQuizCards(parsed));
            } else {
                const md = mk('div', 'markdown-body');
                md.innerHTML = renderMarkdown(data.quiz);
                resultEl.appendChild(md);
            }
        } catch {
            resultEl.innerHTML = '<p style="color:#C0392B;padding:12px 0;">Failed to generate quiz. Please try again.</p>';
        } finally {
            genBtn.disabled = false;
            genBtn.textContent = 'Generate';
        }
    }
}

// ─── Quiz Parser ───

function parseQuiz(text) {
    if (!text) return [];

    const blocks = text.split(/\n-{3,}\n/).filter(s => s.trim());
    const questions = [];

    for (const block of blocks) {
        const q = parseQuizBlock(block);
        if (q) questions.push(q);
    }
    return questions;
}

function parseQuizBlock(block) {
    const lines = block.split('\n').map(l => l.trim()).filter(l => l);

    let questionText = '';
    let options = [];
    let correct = null;
    let explanation = '';
    let source = '';

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];

        if (/^Question:\s*/i.test(line)) {
            questionText = line.replace(/^Question:\s*/i, '').trim();
            continue;
        }

        const optMatch = line.match(/^([A-D])\)\s*(.+)/);
        if (optMatch) {
            options.push({ letter: optMatch[1], text: optMatch[2].trim() });
            continue;
        }

        if (/^Correct\s*Answer:\s*/i.test(line)) {
            const m = line.match(/^Correct\s*Answer:\s*([A-D])/i);
            if (m) correct = m[1];
            continue;
        }

        if (/^Explanation:\s*/i.test(line)) {
            explanation = line.replace(/^Explanation:\s*/i, '').trim();
            while (i + 1 < lines.length && !/^(Source:|Correct\s*Answer:|Question:|[A-D]\))/i.test(lines[i + 1])) {
                i++;
                explanation += ' ' + lines[i].trim();
            }
            continue;
        }

        if (/^Source:\s*/i.test(line)) {
            source = line.replace(/^Source:\s*/i, '').trim();
            continue;
        }
    }

    if (options.length >= 2) {
        return { text: questionText, options, correct, explanation, source };
    }
    return null;
}

function renderQuizCards(questions) {
    const wrap = mk('div', 'quiz-cards');

    questions.forEach((q, i) => {
        const card = mk('div', 'quiz-card');

        const header = mk('div', 'quiz-card-header');
        const num = mk('span', 'quiz-number');
        num.textContent = `Question ${i + 1}`;
        header.appendChild(num);

        const qText = mk('p', 'quiz-question-text');
        qText.textContent = q.text;

        const optsDiv = mk('div', 'quiz-options');

        const answerDiv = mk('div', 'quiz-answer');
        answerDiv.style.display = 'none';

        const correctLabel = mk('div', 'quiz-correct-label');
        const explDiv = mk('div', 'quiz-explanation');
        let cleanExpl = (q.explanation || '').replace(/^#{1,4}\s*/gm, '').replace(/\*\*(.*?)\*\*/g, '$1');
        explDiv.textContent = cleanExpl;
        const srcDiv = mk('div', 'quiz-source');
        let cleanSrc = (q.source || '').replace(/^#{1,4}\s*/gm, '').replace(/\*\*(.*?)\*\*/g, '$1');
        srcDiv.textContent = formatSourceName(cleanSrc);
        answerDiv.appendChild(correctLabel);
        if (q.explanation) answerDiv.appendChild(explDiv);
        if (q.source) answerDiv.appendChild(srcDiv);

        q.options.forEach(opt => {
            const btn = mk('button', 'quiz-option');
            btn.dataset.value = opt.letter;
            const letter = mk('span', 'option-letter');
            letter.textContent = opt.letter;
            const txt = mk('span', 'option-text');
            txt.textContent = opt.text;
            btn.appendChild(letter);
            btn.appendChild(txt);

            btn.addEventListener('click', () => {
                if (card.classList.contains('answered')) return;
                card.classList.add('answered');

                const isRight = opt.letter === q.correct;
                btn.classList.add(isRight ? 'correct' : 'wrong');

                if (!isRight) {
                    const right = optsDiv.querySelector(`[data-value="${q.correct}"]`);
                    if (right) right.classList.add('correct');
                }

                correctLabel.textContent = isRight
                    ? 'Correct'
                    : `Incorrect \u2014 the answer is ${q.correct || '(unknown)'}`;
                correctLabel.classList.add(isRight ? 'is-correct' : 'is-wrong');
                answerDiv.style.display = 'block';
            });

            optsDiv.appendChild(btn);
        });

        card.appendChild(header);
        card.appendChild(qText);
        card.appendChild(optsDiv);
        card.appendChild(answerDiv);
        wrap.appendChild(card);
    });

    return wrap;
}

// ─── Utilities ───

function renderMarkdown(text) {
    if (typeof marked !== 'undefined') {
        marked.setOptions({
            gfm: true,
        });
        return sanitizeRenderedMarkdown(marked.parse(text || ''));
    }
    return escapeHtml(text || '').replace(/\n/g, '<br>');
}

function decorateAssistantMarkdown(container) {
    Array.from(container.querySelectorAll('.next-step-invite')).forEach(node => {
        node.classList.remove('next-step-invite');
    });

    const topLevelParagraphs = Array.from(container.children).filter(node => node.tagName === 'P');
    if (topLevelParagraphs.length < 2) {
        return;
    }

    const lastParagraph = topLevelParagraphs[topLevelParagraphs.length - 1];
    if (looksLikeNextStepInvitation(lastParagraph.textContent || '')) {
        lastParagraph.classList.add('next-step-invite');
    }
}

function looksLikeNextStepInvitation(text) {
    const normalized = String(text || '').replace(/\s+/g, ' ').trim().toLowerCase();
    if (!normalized || normalized.length > 220) {
        return false;
    }

    return /^(if you'd like|if you would like|if you want|if helpful|if that's helpful|i can(?: also)?|i'm happy to|i am happy to|we can(?: also)?|want me to|would you like me to|should i|shall i|could i)/.test(normalized);
}

function sanitizeRenderedMarkdown(html) {
    const template = document.createElement('template');
    template.innerHTML = html || '';

    const container = document.createElement('div');
    Array.from(template.content.childNodes).forEach(node => {
        const sanitized = sanitizeMarkdownNode(node);
        if (sanitized) {
            container.appendChild(sanitized);
        }
    });

    return container.innerHTML;
}

function sanitizeMarkdownNode(node) {
    if (node.nodeType === Node.TEXT_NODE) {
        return document.createTextNode(node.textContent || '');
    }

    if (node.nodeType !== Node.ELEMENT_NODE) {
        return null;
    }

    const tag = node.tagName.toLowerCase();

    if (DROP_CONTENT_TAGS.has(tag)) {
        return null;
    }

    if (!ALLOWED_MARKDOWN_TAGS.has(tag)) {
        const fragment = document.createDocumentFragment();
        Array.from(node.childNodes).forEach(child => {
            const sanitizedChild = sanitizeMarkdownNode(child);
            if (sanitizedChild) {
                fragment.appendChild(sanitizedChild);
            }
        });
        return fragment;
    }

    const clean = document.createElement(tag);

    if (tag === 'a') {
        const href = sanitizeHref(node.getAttribute('href'));
        if (href) {
            clean.setAttribute('href', href);
            if (/^https?:/i.test(href)) {
                clean.setAttribute('target', '_blank');
                clean.setAttribute('rel', 'noopener noreferrer');
            }
        }

        const title = node.getAttribute('title');
        if (title) {
            clean.setAttribute('title', title);
        }
    } else if (tag === 'code') {
        const className = sanitizeCodeClass(node.getAttribute('class'));
        if (className) {
            clean.setAttribute('class', className);
        }
    } else if (tag === 'input') {
        if (node.getAttribute('type') === 'checkbox') {
            clean.setAttribute('type', 'checkbox');
            clean.setAttribute('disabled', '');
            if (node.hasAttribute('checked')) {
                clean.setAttribute('checked', '');
            }
        } else {
            return null;
        }
    } else if (tag === 'th' || tag === 'td') {
        const colspan = sanitizeIntegerAttribute(node.getAttribute('colspan'));
        const rowspan = sanitizeIntegerAttribute(node.getAttribute('rowspan'));
        const align = sanitizeAlignment(node.getAttribute('align'));

        if (colspan) clean.setAttribute('colspan', colspan);
        if (rowspan) clean.setAttribute('rowspan', rowspan);
        if (align) clean.setAttribute('align', align);
    }

    Array.from(node.childNodes).forEach(child => {
        const sanitizedChild = sanitizeMarkdownNode(child);
        if (sanitizedChild) {
            clean.appendChild(sanitizedChild);
        }
    });

    return clean;
}

function sanitizeHref(href) {
    const value = String(href || '').trim();
    if (!value) return '';
    if (value.startsWith('#') || value.startsWith('/')) return value;
    if (value.startsWith('./') || value.startsWith('../')) return value;
    return /^(https?:|mailto:)/i.test(value) ? value : '';
}

function sanitizeCodeClass(className) {
    const tokens = String(className || '')
        .split(/\s+/)
        .filter(token => /^language-[a-z0-9_-]+$/i.test(token) || /^hljs[a-z0-9_-]*$/i.test(token));

    return tokens.join(' ');
}

function sanitizeIntegerAttribute(value) {
    const normalized = String(value || '').trim();
    return /^\d+$/.test(normalized) ? normalized : '';
}

function sanitizeAlignment(value) {
    const normalized = String(value || '').trim().toLowerCase();
    return ['left', 'center', 'right'].includes(normalized) ? normalized : '';
}

function escapeHtml(t) { const d = mk('span'); d.textContent = t; return d.innerHTML; }

function scrollToBottom() {
    requestAnimationFrame(() => { chatAreaEl.scrollTop = chatAreaEl.scrollHeight; });
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function mk(tag, cls) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    return e;
}
