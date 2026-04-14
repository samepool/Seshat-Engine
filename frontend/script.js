let debounceTimer;

const editor = document.getElementById('editor');
const filenameInput = document.getElementById('filename');
const projectNameInput = document.getElementById('project-name')
const subFolderInput = document.getElementById('sub-folder');
const statusDisplay = document.getElementById('status-bar');

// --- 1. THE AUTO-SAVE ENGINE (Debounce) ---
// We wait 1.5 seconds after you stop typing to save. 
// This prevents the server from being overwhelmed.
editor.addEventListener('input', () => {
    statusDisplay.innerText = "Status: Writing...";
    
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        syncWithSeshat();
    }, 1500); 
});

async function syncWithSeshat() {
    const content = editor.value;
    const filename = filenameInput.value;
    const project = projectNameInput.value;
    const subfolder = subFolderInput.value;

    if (!content.trim()) return;

    statusDisplay.innerText = "Status: Seshat is thinking...";

    try {
        const response = await fetch('http://127.0.0.1:8000/process_session', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                project,
                subfolder,
                filename,
                content 
            })
        });

        if (response.ok) {
            const data = await response.json();
            renderBible(data.analysis);

            refreshLibrary();
            statusDisplay.innerText = "Status: Manuscript Saved & Synced";
        }
    } catch (err) {
        statusDisplay.innerText = "Status: Connection Lost";
        console.error("Backend Error:", err);
    }
}

// --- 2. THE LORE REGISTRY (The 'Galbark' Fix) ---
// This sends manual overrides to the Python "Entity Ruler"
async function registerCustomLore() {
    const name = document.getElementById('custom-name').value;
    const type = document.getElementById('custom-type').value;

    if (!name) return;

    statusDisplay.innerText = `Status: Teaching Seshat about ${name}...`;

    try {
        const response = await fetch('http://127.0.0.1:8000/register_lore', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, type })
        });

        if (response.ok) {
            document.getElementById('custom-name').value = '';
            statusDisplay.innerText = `Status: Learned ${name}`;
            // Re-sync immediately to update the sidebar with the new knowledge
            syncWithSeshat();
        }
    } catch (err) {
        console.error("Lore Registration failed:", err);
    }
}

// --- 3. THE LIBRARY (File Access) ---
async function refreshLibrary() {
    try {
        const response = await fetch('http://127.0.0.1:8000/list_chapters');
        const data = await response.json();
        const list = document.getElementById('chapter-list');
        
        // Creates clickable list items for every .md file found
        list.innerHTML = data.chapters.map(file => 
            `<li onclick="loadChapter('${file}')" class="chapter-link">📄 ${file}</li>`
        ).join('');
        
    } catch (err) {
        console.error("Could not load library:", err);
    }
}

async function loadChapter(fullPath) {
    statusDisplay.innerText = `Status: Opening ${fullPath}...`;
    try {
        const response = await fetch(`http://127.0.0.1:8000/load_chapter/${fullPath}`);
        const data = await response.json();

        const parts = fullPath.split('/');
        const fileNameWithExt =  parts.pop();
        const projectName = parts.shift() || "default";
        const subFolder = parts.join('/');

        projectNameInput.value = projectName;
        subFolderInput.value = subFolder;
        filenameInput.value = fileNameWithExt.replace('.md', '');
        editor.value = data.content;
        
        statusDisplay.innerText = `Status: Loaded ${fileNameWithExt}`;
        // Immediately run analysis so the sidebar matches the loaded text
        syncWithSeshat();
    } catch (err) {
        console.error("Load failed:", err);
    }
}

// --- 4. The UI UTILITIES ---
function newDocument() {
    if (confirm("Start a new document?")) {
        editor.value = "";
        filenameInput.value = "New_Chapter";
        statusDisplay.innerText = "Status: New Scroll Ready";
        renderBible({ characters: [], places: [], events: [] });
    }
}

// --- 5. THE SIDEBAR RENDERER ---
function renderBible(analysis) {
    const charList = document.getElementById('char-list');
    const placeList = document.getElementById('place-list');
    const eventList = document.getElementById('event-list');

    // Update Characters and Places with simple icons
    charList.innerHTML = analysis.characters.map(c => `<li>✨ ${c}</li>`).join('');
    placeList.innerHTML = analysis.places.map(p => `<li>📍 ${p}</li>`).join('');
    
    // Update the Significance timeline
    eventList.innerHTML = analysis.events.map(e => `
        <li class="event-item">
            <span class="action-tag">${e.main_action || 'context'}</span>
            <p>${e.context}</p>
        </li>
    `).join('');
}

// Automatically populate the library when the page first opens
window.onload = refreshLibrary;