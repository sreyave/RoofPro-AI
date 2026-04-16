/* ═══════════════════════════════════════════════════════════
   ROOFPRO ASSISTANT · script.js
   Handles: welcome menu, chat flow, API integration,
            UI rendering, auto-scroll, Enter-to-send
   ═══════════════════════════════════════════════════════════ */

'use strict';

/* ──────────────────────────────────────────
   DOM REFERENCES
────────────────────────────────────────── */
const chatMessages    = document.getElementById('chatMessages');
const messageInput    = document.getElementById('messageInput');
const sendBtn         = document.getElementById('sendBtn');
const typingIndicator = document.getElementById('typingIndicator');

/* ──────────────────────────────────────────
   STATE
────────────────────────────────────────── */
let isWaiting = false; // Prevents double-sends while API responds

/* ──────────────────────────────────────────
   WELCOME MENU DEFINITION
   Shown on page load as the first bot message
────────────────────────────────────────── */
const WELCOME_MENU = {
  text: `👋 Welcome to <strong>RoofPro Assistant</strong>!<br><br>
         I'm here to help you with all your roofing needs.<br>
         How can I assist you today?`,
  options: [
    { label: '🏠 1 · Our Services',          value: '1' },
    { label: '🚨 2 · Emergency Repair Guide', value: '2' },
    { label: '📐 3 · Get a Roof Estimate',    value: '3' },
    { label: '👤 4 · Contact a Human',        value: '4' },
  ],
};

/* ──────────────────────────────────────────
   UTILITY: FORMAT TIME (HH:MM am/pm)
────────────────────────────────────────── */
function formatTime(date = new Date()) {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

/* ──────────────────────────────────────────
   UTILITY: SCROLL TO BOTTOM SMOOTHLY
────────────────────────────────────────── */
function scrollToBottom() {
  chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: 'smooth' });
}

/* ──────────────────────────────────────────
   RENDER: DATE DIVIDER
────────────────────────────────────────── */
function appendDateDivider(label = 'Today') {
  const divider = document.createElement('div');
  divider.className = 'date-divider';
  divider.textContent = label;
  chatMessages.appendChild(divider);
}

/* ──────────────────────────────────────────
   RENDER: BOT MESSAGE (optionally with quick-reply buttons)
   @param {string} htmlText       - Inner HTML for bubble content
   @param {Array}  [options]      - Quick-reply option objects { label, value }
   @param {boolean} [hideAvatar]  - If true, hides repeated bot avatar
────────────────────────────────────────── */
function appendBotMessage(htmlText, options = [], hideAvatar = false) {
  const row = document.createElement('div');
  row.className = `message-row bot${hideAvatar ? ' no-avatar' : ''}`;

  /* ── Mini avatar ── */
  const avatar = document.createElement('div');
  avatar.className = 'bot-mini-avatar';
  avatar.innerHTML = `
    <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M4 16 L16 5 L28 16" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M7 14 L7 27 L25 27 L25 14" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>`;

  /* ── Bubble ── */
  const bubble = document.createElement('div');
  bubble.className = 'bubble';

  /* Message text */
  const textEl = document.createElement('p');
  textEl.innerHTML = htmlText;
  bubble.appendChild(textEl);

  /* Quick-reply buttons (if any) */
  if (options.length > 0) {
    const qrContainer = document.createElement('div');
    qrContainer.className = 'quick-replies';

    options.forEach(opt => {
      const btn = document.createElement('button');
      btn.className = 'qr-btn';
      btn.textContent = opt.label;
      btn.addEventListener('click', () => handleQuickReply(opt.value, opt.label, qrContainer));
      qrContainer.appendChild(btn);
    });

    bubble.appendChild(qrContainer);
  }

  /* Timestamp */
  const time = document.createElement('span');
  time.className = 'bubble-time';
  time.textContent = formatTime();
  bubble.appendChild(time);

  row.appendChild(avatar);
  row.appendChild(bubble);
  chatMessages.appendChild(row);
  scrollToBottom();
}

/* ──────────────────────────────────────────
   RENDER: USER MESSAGE
   @param {string} text - Plain text content
────────────────────────────────────────── */
function appendUserMessage(text) {
  const row = document.createElement('div');
  row.className = 'message-row user';

  const bubble = document.createElement('div');
  bubble.className = 'bubble';

  const textEl = document.createElement('p');
  // Escape HTML to prevent XSS from user input
  textEl.textContent = text;
  bubble.appendChild(textEl);

  const time = document.createElement('span');
  time.className = 'bubble-time';
  time.textContent = formatTime();
  bubble.appendChild(time);

  row.appendChild(bubble);
  chatMessages.appendChild(row);
  scrollToBottom();
}

/* ──────────────────────────────────────────
   TYPING INDICATOR: SHOW / HIDE
────────────────────────────────────────── */
function showTyping() {
  typingIndicator.classList.add('visible');
  scrollToBottom();
}

function hideTyping() {
  typingIndicator.classList.remove('visible');
}

/* ──────────────────────────────────────────
   QUICK-REPLY HANDLER
   Triggered when user clicks a menu button
   @param {string} value       - The option value sent to API
   @param {string} label       - Button label shown as user message
   @param {Element} container  - The quick-replies container to disable
────────────────────────────────────────── */
function handleQuickReply(value, label, container) {
  if (isWaiting) return;

  /* Disable all buttons in this menu after one is chosen */
  container.querySelectorAll('.qr-btn').forEach(btn => {
    btn.disabled = true;
    btn.style.opacity = '0.45';
    btn.style.cursor = 'default';
  });

  /* Show the chosen option as a user message */
  appendUserMessage(label);

  /* Send to API */
  sendToAPI(value);
}

/* ──────────────────────────────────────────
   API INTEGRATION
   POST /chat → { message } → { reply }
   @param {string} message - Text to send to the backend
────────────────────────────────────────── */
async function sendToAPI(message) {
  isWaiting = true;
  sendBtn.disabled = true;
  showTyping();

  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    hideTyping();

    /* Render the bot's reply */
    const replyText = data.reply ?? 'Sorry, I didn\'t catch that. Please try again.';
    appendBotMessage(replyText);

  } catch (err) {
    console.error('[RoofPro] API error:', err);
    hideTyping();

    /* Show a friendly error + retry menu */
    appendBotMessage(
      `⚠️ I had trouble connecting to the server.<br>
       Please try again or choose an option from the menu.`,
      WELCOME_MENU.options
    );
  } finally {
    isWaiting = false;
    sendBtn.disabled = false;
  }
}

/* ──────────────────────────────────────────
   SEND: triggered by button click or Enter key
────────────────────────────────────────── */
function handleSend() {
  const text = messageInput.value.trim();
  if (!text || isWaiting) return;

  /* Clear and reset textarea height */
  messageInput.value = '';
  autoResizeTextarea();

  /* Render user bubble */
  appendUserMessage(text);

  /* Forward to API */
  sendToAPI(text);
}

/* ──────────────────────────────────────────
   AUTO-RESIZE TEXTAREA (grows with content)
────────────────────────────────────────── */
function autoResizeTextarea() {
  messageInput.style.height = 'auto';
  messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
}

/* ──────────────────────────────────────────
   EVENT LISTENERS
────────────────────────────────────────── */

/* Send on button click */
sendBtn.addEventListener('click', handleSend);

/* Send on Enter (Shift+Enter for new line) */
messageInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    handleSend();
  }
});

/* Auto-resize textarea as user types */
messageInput.addEventListener('input', autoResizeTextarea);

/* ──────────────────────────────────────────
   INITIALISE: Show welcome message on load
────────────────────────────────────────── */
function init() {
  /* Date divider */
  appendDateDivider('Today');

  /* Welcome menu with quick-reply buttons */
  appendBotMessage(WELCOME_MENU.text, WELCOME_MENU.options);

  /* Focus input */
  messageInput.focus();
}

/* Run after DOM is ready */
document.addEventListener('DOMContentLoaded', init);