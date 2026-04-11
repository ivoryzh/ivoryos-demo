
const socket = io();

// ── DOM refs ────────────────────────────────────────────────
const statusEl   = document.getElementById('connection-status');
const logList    = document.getElementById('log-list');
const armOrb     = document.getElementById('arm-orb');
const armLabel   = document.getElementById('arm-label');
const trayActive = document.getElementById('tray-active');
const floatVial  = document.getElementById('float-vial');
const fvSolid    = floatVial.querySelector('.fv-solid');
const fvLiquid   = floatVial.querySelector('.fv-liquid');
const btnReset   = document.getElementById('btn-reset');

btnReset.addEventListener('click', () => {
    socket.emit('reset_state');
});

// ── Build 15-slot tray (5 cols × 3 rows) ───────────────────
const grid = document.getElementById('tray-grid');
for (let i = 1; i <= 15; i++) {
    const slot = document.createElement('div');
    slot.className = 'vial-slot';
    slot.id = `slot-${i}`;
    slot.innerHTML =
        `<div class="slot-vial" id="vial-${i}">` +
            `<div class="v-rim"></div>` +     // vial opening (mouth rim)
            `<div class="v-cap"></div>` +     // cap (pops off when uncapped)
            `<div class="v-solid"></div>` +   // powder fill (bottom)
            `<div class="v-liquid"></div>` +  // liquid fill (above solid)
        `</div>` +
        `<span class="slot-num">${i}</span>`;
    grid.appendChild(slot);
}

// ── Workbench reference for coordinate calculations ─────────
const workbench = document.querySelector('.workbench');

// Helper: get center of an element relative to .workbench
function getCenter(elId) {
    const el = document.getElementById(elId);
    if (!el || !workbench) return null;
    const er = el.getBoundingClientRect();
    const wr = workbench.getBoundingClientRect();
    return {
        x: er.left - wr.left + er.width  / 2,
        y: er.top  - wr.top  + er.height / 2,
    };
}

// Helper: move float vial to a coordinate
function placeVial(x, y) {
    floatVial.style.left = `${x}px`;
    floatVial.style.top  = `${y}px`;
}

// Helper: show float vial immediately at element center (no transition)
function showVialAt(elId) {
    const pos = getCenter(elId);
    if (!pos) return;
    // Disable transition briefly so it snaps to origin before animating
    floatVial.style.transition = 'none';
    floatVial.style.left = `${pos.x}px`;
    floatVial.style.top  = `${pos.y}px`;
    floatVial.classList.remove('hidden');
    // Re-enable transition on next frame
    requestAnimationFrame(() => {
        floatVial.style.transition = '';
    });
}

// Helper: move float vial to element center (animated)
function moveVialTo(elId) {
    const pos = getCenter(elId);
    if (!pos) return;
    placeVial(pos.x, pos.y);
}

// Helper: fade out float vial in place — no position slide
function hideVialAfterMove() {
    setTimeout(() => {
        // Freeze position, only allow opacity to transition
        floatVial.style.transition = 'opacity 0.35s ease';
        floatVial.style.opacity = '0';
        setTimeout(() => {
            // Snap to hidden, restore transition for next use
            floatVial.classList.add('hidden');
            floatVial.style.opacity = '';
            floatVial.style.transition = '';
        }, 380);
    }, 820);  // wait for move animation (~750ms) to finish first
}

// ── Logging ─────────────────────────────────────────────────
function log(text) {
    const li = document.createElement('li');
    li.textContent = `[${new Date().toLocaleTimeString()}] ${text}`;
    logList.prepend(li);
    while (logList.children.length > 50) logList.removeChild(logList.lastChild);
}

// Flash a station module once
function flash(id) {
    const el = document.getElementById(id);
    if (!el) return;
    el.classList.remove('flash');
    void el.offsetWidth;
    el.classList.add('flash');
    setTimeout(() => el.classList.remove('flash'), 500);
}

// ── Socket connection ────────────────────────────────────────
socket.on('connect', () => {
    statusEl.textContent = 'Connected';
    statusEl.classList.add('connected');
    socket.emit('request_sync_state');
});
socket.on('disconnect', () => {
    statusEl.textContent = '···';
    statusEl.classList.remove('connected');
});

// ── sync_state: update tray slots + float vial fills ────────
socket.on('sync_state', (state) => {
    console.log("State restored:", state);
    const {
        is_held_by_arm = false,
        vial_location  = 'tray',
        current_vial   = null,
        vial_contents  = {},
        solid_added    = 0,
        liquid_added   = 0,
        cap_is_on      = true,
    } = state;

    // Arm indicator
    armOrb.classList.toggle('busy', !!is_held_by_arm);
    armLabel.textContent = is_held_by_arm
        ? `Arm · Slot ${current_vial ?? '?'}`
        : 'Arm · Idle';
    trayActive.textContent = current_vial
        ? (is_held_by_arm ? `#${current_vial} held` : `#${current_vial}`)
        : '';

    // Float vial fills (live while arm is holding or at a station)
    if (is_held_by_arm || (vial_location && vial_location !== 'tray')) {
        const sp = solid_added  > 0 ? Math.max(8, Math.min(68, solid_added  / 10)) : 0;
        const lp = liquid_added > 0 ? Math.max(8, Math.min(68, liquid_added * 15)) : 0;
        fvSolid.style.height  = `${sp}%`;
        fvLiquid.style.height = `${lp}%`;
        fvLiquid.style.bottom = `${sp}%`;
        floatVial.classList.toggle('uncapped', !cap_is_on);
    }

    // Render float vial explicitly at the arm or the specific station
    if (is_held_by_arm) {
        showVialAt('arm-module');
    } else if (vial_location && vial_location !== 'tray') {
        showVialAt(vial_location);
    } else {
        floatVial.classList.add('hidden');
    }

    // Update all 15 tray slots
    for (let i = 1; i <= 15; i++) {
        const slotEl = document.getElementById(`slot-${i}`);
        const vialEl = document.getElementById(`vial-${i}`);
        if (!slotEl || !vialEl) continue;

        const isActive  = (i === current_vial);
        const info      = vial_contents[String(i)] || {};
        const processed = !!info.processed;

        // The tray slot should permanently reflect the saved state; it updates only when the vial is placed back
        const solidMg  = info.solid_mg  || 0;
        const liquidMl = info.liquid_ml || 0;
        const capOn    = processed ? info.cap_is_on : true;

        slotEl.classList.toggle('slot-active', isActive);
        slotEl.classList.toggle('slot-done',   processed && !isActive);
        // Ghost the tray mini-vial when it's being held by arm
        vialEl.classList.toggle('away',     isActive && (!!is_held_by_arm || vial_location !== 'tray'));
        vialEl.classList.toggle('uncapped', !capOn);

        const solidPct  = solidMg  > 0 ? Math.max(8, Math.min(68, solidMg  / 10)) : 0;
        const liquidPct = liquidMl > 0 ? Math.max(8, Math.min(68, liquidMl * 15)) : 0;
        vialEl.querySelector('.v-solid').style.height  = `${solidPct}%`;
        const liqEl = vialEl.querySelector('.v-liquid');
        liqEl.style.height = `${liquidPct}%`;
        liqEl.style.bottom = `${solidPct}%`;
    }
});

// ── Map action strings to station element IDs ────────────────
function stationIdOf(action) {
    if (action.includes('weigh_balance'))    return 'weigh_balance';
    if (action.includes('stir_plate'))       return 'stir_plate';
    if (action.includes('capping'))          return 'capping_station';
    if (action.includes('solid'))            return 'solid_addition_station';
    if (action.includes('liquid'))           return 'liquid_addition_station';
    if (action.includes('analysis'))         return 'analysis_station';
    return null;
}

// ── instrument_event ─────────────────────────────────────────
socket.on('instrument_event', ({ instrument, action, args }) => {
    switch (instrument) {
        case 'robotic_arm':             onArm(action, args);     break;
        case 'weigh_balance':           onBalance(action, args); break;
        case 'stir_plate':              onStir(action);          break;
        case 'capping_station':         onCapping(action);       break;
        case 'solid_addition_station':  onSolid(args);           break;
        case 'liquid_addition_station': onLiquid(args);          break;
        case 'sample_analysis_station': onAnalysis(args);        break;
        default: log(`? ${instrument}.${action}()`);
    }
});

// ── Robotic arm handler — drives float vial movement ─────────
function onArm(action, args) {
    log(`Arm: ${action.replace(/_/g, ' ')}`);

    if (action.startsWith('pick_up')) {
        if (action.includes('tray')) {
            // Vial picked up from a specific slot
            const n = args && args[0] ? parseInt(args[0]) : null;
            if (n) {
                // Reset float vial fills to empty before pickup
                fvSolid.style.height  = '0%';
                fvLiquid.style.height = '0%';
                fvLiquid.style.bottom = '0%';
                floatVial.classList.remove('uncapped');
                showVialAt(`slot-${n}`);
                flash(`slot-${n}`);
            }
        } else {
            // Picking up from a station — vial already there visually
            const sid = stationIdOf(action);
            if (sid) flash(sid);
        }

    } else if (action.startsWith('place')) {
        if (action.includes('tray')) {
            // Return vial to its slot
            const n = args && args[0] ? parseInt(args[0]) : null;
            const slotId = n ? `slot-${n}` : null;
            if (slotId) {
                moveVialTo(slotId);
                // After animation: hide float vial (tray slot will now show filled)
                hideVialAfterMove();
                setTimeout(() => flash(slotId), 400);
            }
        } else {
            // Placing at a station
            const sid = stationIdOf(action);
            if (sid) {
                moveVialTo(sid);
                flash(sid);
            }
        }
    }
}

// ── Instrument handlers ──────────────────────────────────────
function onBalance(action, args) {
    const el = document.getElementById('weigh-val');
    if (action === 'zero') {
        el.textContent = '0 mg';
        log('Balance: zeroed');
    } else if (action === 'get_weight_mg') {
        const v = args && args[0] != null ? Number(args[0]).toFixed(1) : '--';
        el.textContent = `${v} mg`;
        log(`Balance: ${v} mg`);
    }
    flash('weigh_balance');
}

function onStir(action) {
    const icon = document.getElementById('stir-icon');
    if (action === 'start_stirring') { icon.classList.add('spin-active');    log('Stir: on'); }
    else                             { icon.classList.remove('spin-active'); log('Stir: off'); }
}

function onCapping(action) {
    const capped = action === 'cap_vial';
    document.getElementById('capping-val').textContent = capped ? 'Capped' : 'Open';
    log(`Capping: ${capped ? 'capped' : 'uncapped'}`);
    flash('capping_station');
}

function onSolid(args) {
    const m = args && args[0] != null ? args[0] : '?';
    log(`Solid: +${m} mg`);
    // Fill animation is driven by sync_state updates
    flash('solid_addition_station');
}

function onLiquid(args) {
    const v = args && args[0] != null ? args[0] : '?';
    log(`Liquid: +${v} mL`);
    flash('liquid_addition_station');
}

function onAnalysis(args) {
    const val = args && args[0] != null ? Number(args[0]).toFixed(3) : '--';
    log(`Analysis: ${val}`);
    const st = document.getElementById('analysis_station');
    st.classList.add('active');
    setTimeout(() => {
        st.classList.remove('active');
        document.getElementById('analysis-val').textContent = val;
    }, 1800);
}
