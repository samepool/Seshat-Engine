let debounceTimer;

const editor = document.getElementById('editor');
const filenameInput = document.getElementById('filename');
const statusDisplay = document.getElementById('status-bar');

//Listen for Typing
editor.addEventListener('input', () => {
    statusDisplay.innerText = "Status: Typing...";

    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        syncWithSeshat();
    }, 1500);
});

async function syncWithSeshat() {
    const content = editor.value;
    const filename = filenameInput.value;

    if (!content.trim()) return;
    statusDisplay.innerText = "Status: Seshat is thinking...";

    try {
        const response = await fetch('http://127.0.0.1:8000/process_session', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename, content })
        })

            const data = await response.json();
            renderBible(data.analysis);
            statusDisplay.innerText = "Status: Synced & Organied";
        } catch (err) {
            statusDisplay.innerText = "Status: Connection Error";
            console.error("Backend unreachable:", err);
        }
    }
function renderBible (analysis) {
    const charList = document.getElementById('char-list');
    const placeList = document.getElementById('place-list');
    const eventList = document.getElementById('event-list');

    // Update Characters
    charList.innerHTML = analysis.characters.map(c => `<li>${c}</li>`).join('');

    //Update places
       placeList.innerHTML = analysis.places.map(p => `<li>${p}</li>`).join('');

    //Update Events
       eventList.innerHTML = analysis.events.map(e => `<li class="action-tag">${e.main_action || 'context'}</span>
        <p>${e.context}</p>
        </li>
        `).join('');
}