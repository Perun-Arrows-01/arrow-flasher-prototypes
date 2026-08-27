# Arrow Flasher — HTML Prototypes vs TSX Implementation: Discrepancy Report

**Date:** 2026-08-27
**Scope:** 8 HTML prototypes in this directory (`app.html`, `dashboard.html`, `diag.html`, `history.html`, `index.html`, `license.html`, `rxbind.html`, `setup.html`) compared against the real React implementation in `/home/roma/projects/arrow-flasher/apps/web/src/` (23 files: 5 pages, 16 components, `App.tsx`, `api.ts`).
**Verdict up front:** the TSX implementation has evolved well past the prototypes. Prototypes are broadly aligned on page structure and core terminology, but are stale on slot-state coverage, safety flow, error surfacing, and several label strings. The License prototype page has **no TSX counterpart at all**.

---

## 1. Navigation

| # | TSX (real app) | Prototype | Recommendation |
|---|---|---|---|
| N1 | 5 tabs: `Dashboard`, `History`, `RX Bind`, `Settings`, `Diagnostics` (`Nav.tsx`) | 6 links: `Dashboard`, `Setup`, `History`, `RX Bind`, `Diagnostics`, `License 🔒` (`app.html`) | Remove `License 🔒` from prototype nav (no license UI exists in the app), or mark it clearly as "planned". |
| N2 | Tab order: Dashboard → History → RX Bind → Settings → Diagnostics | Order: Dashboard → Setup → History → RX Bind → Diagnostics → License | Align order with TSX: History second, Settings fourth. |
| N3 | Nav label **"Settings"** (matches page h1) | Nav link says **"Setup"** but the page h1/title says "Settings" | Rename prototype nav link to "Settings" — the prototype contradicts itself. |
| N4 | No standalone landing page; `App.tsx` renders Dashboard by default | `index.html` is a prototype index/landing page | Acceptable — `index.html` is prototype scaffolding, not a product page. Keep it prototype-only. |

---

## 2. Dashboard (`dashboard.html` vs `pages/Dashboard.tsx` + `components/SlotCard.tsx`)

### 2.1 Toolbar / status strip

| # | TSX term | Prototype term | Recommendation |
|---|---|---|---|
| D1 | h1 `Dashboard` + `● live` / `○ connecting…` WS indicator | h1 `Dashboard` + static `live` badge | Add the disconnected state (`○ connecting…`) to the prototype. |
| D2 | Template `<select>` with aria-label **"Active firmware template"**, title "Switch active template" / "Disabled while a slot is active"; no visible text label | Visible label **"Active template"** | Pick one term. "Active template" is shorter and matches Settings; if kept, update the TSX aria-label to match. |
| D3 | **"Silent mode"** checkbox + tooltip "When on, USB plug events auto-claim as the next free slot (no banner)." | "Silent mode" checkbox, no explanation | Add the tooltip/help text to the prototype so the term is self-explanatory. |
| D4 | `Rescan` (title: "Re-enumerate plugged STM32 devices without unplug/replug") | `Rescan` | ✅ Match. |
| D5 | Sort options `slot #` / `recently plugged` (aria "Slot sort order") | `Sort`: `slot #` / `recently plugged` | ✅ Match. |
| D6 | Toggle button **"Hide empty" / "Show empty (N)"** (state-dependent) | Static button `Hide empty` | Prototype should show both toggle states. |
| D7 | Tally: `{n} slots — {d} done, {b} busy, {e} error, {x} empty` | `6 slots` + `done 1` `busy 3` `error 1` `empty 1` (chips) | Same data, different format. Acceptable; sync format if pixel parity matters. |
| D8 | Session strip: `Session: {d} done, {f} failed, {t} total` + `Reset session` + `Export CSV` | `Reset session` + `Export CSV` only; no session counter line | Add the session summary line to the prototype. |
| D9 | Batch banner: **"✓ Rack complete — {done} flashed, {failed} failed"** + chime + title pulse | Absent | Add to prototype (operator-facing feature). |
| D10 | No positive health banner — `HealthBanner` renders **only** when checks fail | Green banner: **"✅ Server ready — All subsystems operational."** + a `Ready.` status line | Remove the permanent green banner from the prototype or gate it to appear-then-fade; the real UI stays quiet when healthy. |
| D11 | No-slots empty state instructs: `pnpm -C packages/cli slot-wizard … data/slots.json` | Absent (prototype always has slots) | Add an empty-slots state to the prototype. |
| D12 | Document title aggregates rack state: `Arrow — {busy}⚙ {done}✓ {error}✗` | Static `<title>` | Optional; document as dynamic-title behavior. |

### 2.2 Banners / toasts

| # | TSX | Prototype | Recommendation |
|---|---|---|---|
| D13 | **MismatchToast**: "Slot {n}: Betaflight device plugged, but active template `{name}` flashes the FC." Buttons: `Reboot into DFU`, `Switch to “{escTemplate}”`, `Dismiss` | "ℹ Mismatch — Slot 3 plugged drone matches template quad-x-default." Buttons: `Switch to quad-x-default`, `Dismiss`, `Reboot to DFU` | Different detection semantics (TSX fires when a BF-mode device meets an FC-flashing template; prototype implies template-to-drone matching) and different button copy: **"Reboot into DFU"** (TSX) vs "Reboot to DFU" (prototype). Sync message and button label. |
| D14 | **UnclaimedPlugBanner**: shows device personality (`DFU bootloader` / `Betaflight CDC`), VID:PID chip, editable slot-label input, `Claim as Slot {n}`; success: "Claimed as Slot {n} — ready to flash." or "…Restart the server … to activate." | "⚠ Unclaimed plug — USB 1-4.1 unrecognized." + `Claim` + `Dismiss` | Prototype is much simpler. Add VID:PID, device personality, and the "Claim as Slot N" label to the prototype. |
| D15 | **SoftDfuFailedToast**: "Slot {n}: … (reason: {reason})" amber toast | Absent | Add to prototype. |
| D16 | **Safety BYPASSED** global banner (App-level): "⚠ Safety BYPASSED — `ARROW_SAFETY_BYPASS=1` at server start. WiFi bind will not check anything…" | Absent | Add to prototype (all pages). |

### 2.3 Slot actions

| # | TSX | Prototype | Recommendation |
|---|---|---|---|
| D17 | Busy states → `Cancel` only | Busy → `Cancel`; WAIT_BATTERY → `Retry` + `Cancel` | Remove `Retry` from WAIT_BATTERY in prototype, or confirm intended UX. |
| D18 | DONE / ERROR → `Retry` only | DONE → `Eject`; ERROR → `Skip` + `Cancel` | **"Eject" and "Skip" do not exist in the real app.** Replace with `Retry`; drop `Cancel` from terminal cards (they're not busy). |
| D19 | "Already flashed with …" info chip + **"Mark as DONE"** button | Absent | Add to prototype. |
| D20 | Per-slot template `<select>` + amber **"next: {name}"** badge when a hot-swapped template applies on next plug | Per-slot template dropdown present; no `next:` badge | Add the `next:` badge to the prototype. |

---

## 3. Slot states & workflow

### 3.1 State machine coverage

The real pipeline (`packages/core/src/pipeline/slot-state.ts`) defines **15 states**:

```
EMPTY → ENTERING_DFU → DFU_READY → FLASHING_FC → REBOOTING → HANDSHAKE_MSP
      → WAIT_BATTERY → ENTER_PASSTHROUGH → ESC_PHASE → MOTOR_TEST
      → BF_AUTOCONFIG → ELRS_BIND → DONE | ERROR | ABORTED
```

The prototype shows only **6**: `EMPTY`, `FLASHING_FC`, `ESC_PHASE`, `WAIT_BATTERY`, `DONE`, `ERROR`.

| # | Missing in prototype | TSX rendering | Recommendation |
|---|---|---|---|
| S1 | `ENTERING_DFU` | "🔄 Rebooting to DFU…" | Add state card example. |
| S2 | `DFU_READY` | State chip (amber #bf8700) | Add state card example. |
| S3 | `REBOOTING`, `HANDSHAKE_MSP`, `ENTER_PASSTHROUGH` | State chip (purple/blue) | Add at least one intermediate-state example. |
| S4 | `MOTOR_TEST` | "Spinning motor {n} ({phase})" (green text) | Add state card example — safety-relevant (motors spin). |
| S5 | `BF_AUTOCONFIG`, `ELRS_BIND` | State chip only (default grey — not in `STATE_COLORS`) | Add to prototype; also consider adding explicit colors in `STATE_COLORS`. |
| S6 | `ABORTED` | State chip (grey #8b949e) | Add state card example. |
| S7 | `PREP ESC` relabel: in ESC-only templates (`skipFcFlash`), `FLASHING_FC` displays as **"PREP ESC"** | Absent | Document/add to prototype — operator-visible relabel. |

### 3.2 Per-state content wording

| # | State | TSX term | Prototype term | Recommendation |
|---|---|---|---|---|
| S8 | EMPTY | State chip only (no body text) | **"Waiting for drone…"** | Either add the helper text to `SlotCard` (better UX) or remove from prototype. |
| S9 | FLASHING_FC | **"FC flash · {pct}%"** | "STM32F405 — arrowflight-f405-1.14.0.hex 62%" | Prototype shows MCU + filename; TSX shows only %. Decide which is canonical (TSX is truth today). |
| S10 | Stuck watchdog | **"⚠ possibly stuck ({n}s)"** — measured from last progress tick, per-state thresholds (FLASHING_FC 60 s, ESC_PHASE 120 s, …) | "possibly stuck (12 s)" | Add ⚠ and the `(Ns)` format; note threshold semantics in prototype annotations. |
| S11 | Auto-retry | **"Retry {attempt}/{total}"** chip with reason tooltip | Absent | Add to prototype. |
| S12 | ESC_PHASE | "ESC {motor} · {phase} · {done}/{total}" + progress bar | "ESC 2 · phase · 2/4 38%" | ✅ Format matches (prototype uses literal "phase" as placeholder — replace with a real phase name like `flash`/`verify`). |
| S13 | WAIT_BATTERY | "🔋 {V} V" + "plug battery…" + "⏳ {m}:{ss} left" | "Connect battery now" + "2:35 left" + "Device in DFU, awaiting power for motor test." | Sync copy: TSX uses "plug battery…"; countdown format matches (`m:ss left`). Prototype's explanatory second line doesn't exist in TSX. |
| S14 | DONE | MCU UID truncated to 12 chars + click-to-copy; duration `8.3s` (no space); banner "✅ READY — DISCONNECT" | Full MCU UID; "8.3 s"; "first seen 14:21"; same banner | Match duration format (`8.3s` vs `8.3 s`); prototype's "first seen" line has no TSX equivalent. |
| S15 | ERROR | `{failureStage}: {failureMessage}` + 💡 ErrorHintCard (up to 5 recovery bullets per stage) | "DFU flash failed — check USB cable, hold BOOT0 longer" (single line) | Prototype must show the stage prefix (`fc_flash: …`) and the hint card — see §6. |
| S16 | Repeat failures | **"⚠ this board failed {n}× before — consider setting it aside"** (shown at ≥2) | "repeat failure #3" | Sync copy to the TSX string. |
| S17 | First-seen (ESC-only) | **"⚠ first time seen — no FC history"** | Absent | Add to prototype. |

---

## 4. Settings (`setup.html` vs `pages/Setup.tsx` + section components)

| # | TSX term | Prototype term | Recommendation |
|---|---|---|---|
| P1 | h1 `Settings`; per-section saves: **"Save template"** / **"Save slots"** + `Discard`; result banner "Saved. **Restart required.** {reason}" or error + validation issue list | Global save bar: "No unsaved changes", "Edits stay local to this mock UI.", `Save`, `Discard` | Prototype's global Save doesn't exist — saves are per-section. Update prototype; drop "No unsaved changes" (no dirty-tracking in TSX). |
| P2 | `TemplatesBar` (aria "Templates bar"): `+ New`, `+ New (FC-only)`, `Delete template`, active-template select; section h2 is **"Template: {activeName}"** | h2 `Templates` + "Template controls" + same buttons | ✅ Buttons match exactly. Prototype's h2 "Templates" vs TSX "Template: {name}" — minor. |
| P3 | FC firmware: "Flash FC firmware", "FC firmware (.bin)", "Verify after flash" (hint: STM32CubeProgrammer only), "Force DFU if FC in normal mode", "DFU loader" (`stm32cube`/`dfu-util`), "STM32 programmer path", library select "— select from library —", "…or paste an absolute path", **"Upload .bin"**, sha256 display | Same labels; button is **"+ Upload .bin"** | Mostly ✅. Button label differs: "Upload .bin" (TSX) vs "+ Upload .bin" (prototype). |
| P4 | ESC firmware: "Flash ESC firmware", "ESC firmware (.hex)", **"Browse Bluejay…"** opens a catalog browser (version select, Layout/MCU/Deadtime/PWM filters, `Load` fetches the GitHub release index, per-asset download), "Always re-flash (force mode)" (skips the "ESC already matches" check), "PWM frequency" 24/48/96 kHz | Same core labels; no catalog browser detail | Add the Bluejay catalog browser to the prototype or annotate it as out of scope. ✅ core labels match. |
| P5 | "Motor directions" (Motor 1–4: normal / reversed / bidirectional / bidirectional-reversed) + "Motor → ESC index map" | Identical | ✅ Match. |
| P6 | ELRS: "Write ELRS bind phrase", **"Required (fail the flash if RX stays silent)"**, "Auto-discover UART", "UART identifier:" + BF identifier hint "(20=USB_VCP, 51=USART1, 52=USART2, … on STM32F4)", "Bind phrase:" placeholder "any 1-255 char string", "Advanced timings" ▸ **"ping timeout (ms):" / "ping retries:"** (lowercase) | "Required", "UART identifier", "Bind phrase", **"Ping timeout (ms)" / "Ping retries"** (capitalized) | Sync: extend "Required" with the failure-semantics suffix; lowercase labels in TSX vs capitalized in prototype — pick one. |
| P7 | Motor test: "Motor direction-verification spin", throttle **slider** "Throttle ({n}%):", "Duration per motor (ms):", "Delay between motors (ms):", warning "⚠ Each motor will spin briefly… Remove props or secure the airframe before enabling." | Same fields; throttle is a numeric input "Throttle (%)"; no safety warning | Change prototype throttle to a slider + add the props warning (safety-relevant). |
| P8 | Betaflight autoconfig: label **"Betaflight autoconfig (Serial RX / CRSF)"**; help: "Sets `feature SERIALRX` + `serialrx_provider=CRSF` on the UART used by the ELRS section, then EEPROM-saves and reboots. Skipped if ELRS is not enabled." | Label "Betaflight autoconfig"; help: "Applies mixer, motor outputs, serial ports, and receiver protocol after FC flash." | **Prototype overstates scope** (mixer/motor outputs are not applied). Sync to the TSX text. |
| P9 | Slots: h2 `Slots`, table `Slot # / USB path / Label`, `Remove`, `+ Add slot`, **"Save slots"** | Identical | ✅ Match. |
| P10 | System section: help mentions `git pull` + "Linux/systemd only — on macOS dev, stop and re-run `pnpm dev`"; inline confirm "Confirm: restart the server now? The dashboard will briefly disconnect and reload itself." → `Yes, restart` / `Cancel`; 409 → `Force restart`; states "Asking server to restart…", "Server restarting — waiting for it to come back online…", "Back online. Reloading dashboard…", error "server did not come back within 30s. Check `journalctl -u arrow-flasher` on the bench." | "Restart is allowed only when all slots are idle. You may force restart if stuck." + generic confirm modal | **Stale copy.** Sync prototype to the TSX confirm flow and messages. |
| P11 | No license-lock notice anywhere | Top banner: "🔒 License activation is temporarily locked…" | Remove from prototype (no license feature in app). |

---

## 5. RX Bind (`rxbind.html` vs `pages/RxBind.tsx` + `AutobindPanel` + `SafetyBanner`)

| # | TSX term | Prototype term | Recommendation |
|---|---|---|---|
| R1 | h1 **"RX Bind (WiFi)"** | h1 "RX Bind" | Sync h1 (or drop "(WiFi)" in TSX). |
| R2 | **SafetyBanner — 4-state interactive gate**: (a) bypassed warning; (b) blocked: "cannot start WiFi bind while slot {n} is mid-pipeline. Wait for the pipeline to finish."; (c) **3-second hold-to-confirm**: "Safety: confirm all batteries are disconnected from airframes before starting WiFi bind."; (d) confirmed: "✓ Safety: batteries confirmed disconnected. WiFi bind enabled." | Static line: "✅ Safety gate OK — System disarmed, no busy slots, binding allowed." | **Major gap.** Prototype must show the hold-to-confirm flow and the blocked/bypassed states. |
| R3 | Autobind panel: `Mode:` (managed/…), "· last scan: {Ns ago}", Start/Stop, "Use template phrase", validation "Phrase is required."; default poll **8000 ms** | h2 "Autobind", "Mode: off", "**Poll interval: 5000 ms**", "Detected RXs: 0", Start/Stop | Poll interval mismatch (8000 real vs 5000 prototype); mode value "managed" vs "off"; add "last scan" relative time. |
| R4 | Scan section h2 **"Discovered RX APs"** (no "Manual bind" heading); button `Scan for RX APs`; table columns **SSID / Signal only** | h2 "Manual bind"; table **SSID / Signal / Protocol** (ELRS 3.0, CRSF) | Drop the `Protocol` column from the prototype (backend doesn't supply it) and rename heading, or add protocol support to the backend first. |
| R5 | "wifi backend not supported" degraded state (nmcli note, recent binds still browsable) | Absent | Add degraded state to prototype. |
| R6 | Bind row: label "Bind phrase", `Use template phrase` (title "Fill from active template's elrs.bindPhrase"), **"Bind selected ({n})"**, validation **"Select at least one RX."**, busy guard "A batch is in progress — wait for it to finish." | h2 "Bind phrase" section, "Bind selected (0)", **"Select at least one receiver."** | Terminology: TSX says "RX", prototype says "receiver" — unify on "RX". Add busy-guard message. |
| R7 | Cycle table h2 **"In-progress / latest cycle"**, columns **SSID / Step / Message**; steps: queued → connecting → posting → verifying → rebooting → disconnected → done | h2 "Latest cycle", columns **RX / Bind phrase / Status / Started** (phrase masked `******`) | Different table shape — sync columns and heading to TSX. |
| R8 | Recent binds: columns **When / SSID / HW id / OK / Failure** (OK = yes/no, Failure = message); empty: "No binds recorded yet." | Columns **When / RX / Result** (OK / timeout) | Sync columns; prototype's "Result: timeout" conflates status+message — TSX splits them. |

---

## 6. Error handling

| # | TSX | Prototype | Recommendation |
|---|---|---|---|
| E1 | **ErrorHintCard**: stage-specific recovery hints for `fc_flash`, `msp` ("port wait timeout"/"no_betaflight_boot"/"cannot open"), `passthrough` ("escount=0"), `esc_0..3`, `motor_test`, `bf_autoconfig`, `elrs_*` — titled "💡 {title}" + bullet list, e.g. "FC firmware flash failed", "RELEASE BOOT0…", "No ESCs detected on 4-way" | One-line error text only ("DFU flash failed — check USB cable, hold BOOT0 longer") | Prototype should show at least one expanded hint card to represent the real error UX. |
| E2 | Failure line format: `{failureStage}: {failureMessage}` (e.g. `fc_flash: DFU erase timeout…`) | Free-text message, no stage prefix | Add stage prefix in prototype. |
| E3 | ESC error dumps surfaced on Diagnostics with download links | ✅ Present (diag.html) — columns match exactly (When/Slot/ESC/UID/Size/File) | ✅ Match. |
| E4 | Health failures: `HealthBanner` "⚠ Server not ready" + per-check `name: reason — remediation` (checks: `usbDetection`, `db`, `dataDir`, `slotTable`); shown on Dashboard **and** Diag | Diag shows the same check names/reasons/remediations + extra "Quick fixes" list + "Critical: 2 / Warning: 2" counts + "4 checks failing; flashing is unavailable." | Check names and remediation strings **match exactly** ✅. Prototype adds severity counts and a quick-fix list that don't exist in TSX — either implement severity in `/api/ready` or drop from prototype. |
| E5 | Settings save errors: red banner with Zod issue list | Generic "Confirm action" modal: "This is a simulated prototype action." | Prototype's generic modal is scaffolding; TSX uses inline confirms (System section) and result banners. Annotate modals as prototype-only. |
| E6 | Toasts: MismatchToast, SoftDfuFailedToast (amber, role="alert") | Mismatch + Unclaimed banners only | Add soft-DFU-fail toast to prototype. |

---

## 7. History (`history.html` vs `pages/History.tsx`)

| # | TSX | Prototype | Recommendation |
|---|---|---|---|
| H1 | **No filters** — table renders all rows | Filter buttons `All / Success / Failure` + time range `All time / Last 7 days / Last 24h` + "Showing 3 of 3 sessions" | **Prototype promises filters that don't exist.** Either implement filters in TSX or remove them from the prototype. |
| H2 | Columns: `Slot / Started / Duration / MCU UID / Result` | Columns: `# / Slot / Started / Duration / MCU UID / Result` | Drop the `#` column or add it in TSX. |
| H3 | Row expands on click ("Click to toggle row detail"), detail rows: `✓ ok`, `profile: {name}`, `fc hash: sha256:…`, `esc hash: sha256:…`, `full MCU UID: …`, `started:`, `finished:`, `({ms}ms raw)`, `(no message)` | `details` button; detail labels without colons ("profile arrow-flight-f405", "duration ms 8300", "esc signatures 4 ESCs detected", "esc actions flash, verify") | TSX lacks "esc signatures"/"esc actions" detail rows that the prototype shows — either add to TSX or remove from prototype. Label punctuation differs (colon vs none). |
| H4 | Empty state: **"No flashes yet."** | "No entries match the selected filter." | Sync (TSX text is canonical; prototype's implies filters). |
| H5 | Result cell: `✓ ok` / failure styling | "success" / "failure" text | Unify result vocabulary. |

---

## 8. Diagnostics (`diag.html` vs `pages/Diag.tsx`)

| # | TSX | Prototype | Recommendation |
|---|---|---|---|
| G1 | h1 `Diagnostics` + HealthBanner (only when failing) | h1 `Diagnostics` + failure summary + Quick fixes | See E4 — severity/quick-fix extras. |
| G2 | USB tree line: `{name} — VID 0x… PID 0x… loc 0x…`; empty: "No devices found." | Identical format | ✅ Match. |
| G3 | ESC error dumps: identical columns; empty: "No dumps recorded." | Identical | ✅ Match. |
| G4 | Server control: idle-gated `Restart server` (titles: "Restart the server (idle-gated)" / "Wait until all slots are idle"); feedback "Restart requested at uptime {u}s — accepted/{error}"; **no uptime display, no confirm dialog** | Shows "Uptime: 2 h 14 m 33 s" + "This action requires confirmation…" + confirm modal | Prototype shows uptime and a confirm step that this page doesn't have (the confirm flow lives in Settings → System). Sync or annotate. |

---

## 9. License page — NO TSX COUNTERPART

`license.html` (activation key input, license details, feature flags `flash.fc`/`flash.esc`/`live_usb`/`templates.manage`/`history.export`/`wifi.bind`, offline grace, "Unlock activation (admin only)") has **zero** corresponding code in `apps/web/src` — a repo-wide search for `licen[cs]e` in the web app returns nothing, and `Nav.tsx` has no license route. (Licensing exists as a server-side gate design, but no web UI was built.)

**Recommendation:** either
1. mark `license.html` as "planned / not implemented" in `index.html` and the prototype nav, or
2. if licensing UI is on the roadmap, file an implementation task and keep the prototype as the spec — but then feature-flag terminology must be settled against the server-side license schema first.

---

## 10. Missing-component summary

**In TSX but absent (or severely understated) in prototypes:**

1. `SafetyBanner` hold-to-confirm flow + global "Safety BYPASSED" banner (App.tsx)
2. `SoftDfuFailedToast`
3. `ErrorHintCard` stage-specific recovery hints
4. "Mark as DONE" / "Already flashed" chip
5. "next: {template}" per-slot badge
6. `PREP ESC` relabel for ESC-only templates
7. Stuck watchdog with real thresholds + `Retry {n}/{total}` auto-retry chip
8. "⚠ first time seen — no FC history" and "⚠ this board failed N× before" chips
9. "✓ Rack complete" batch banner + chime + dynamic document title
10. Bluejay catalog browser (filters, GitHub release index)
11. `MOTOR_TEST`/`BF_AUTOCONFIG`/`ELRS_BIND`/`ABORTED`/`DFU_READY`/`REBOOTING`/`HANDSHAKE_MSP`/`ENTER_PASSTHROUGH`/`ENTERING_DFU` state examples
12. Session summary strip ("Session: X done, Y failed, Z total")
13. No-slots empty state (slot-wizard instructions); "wifi backend not supported" degraded state
14. `Show empty (N)` toggle state; `Force restart` on 409; System-section restart lifecycle banners

**In prototypes but not in TSX (stale or unimplemented):**

1. License page (entire) + license-lock banners on Settings
2. History filters (result + time range), `#` column, "esc signatures"/"esc actions" detail rows
3. `Eject` (DONE) and `Skip` (ERROR) slot buttons; `Retry` on WAIT_BATTERY
4. Diag severity counts / "Quick fixes" / uptime display / restart confirm modal
5. RX-scan `Protocol` column; "Latest cycle" table shape (RX/Bind phrase/Status/Started)
6. Permanent "✅ Server ready — All subsystems operational" banner; "Ready." status line; "No unsaved changes" indicator
7. EMPTY-state helper text "Waiting for drone…"; "first seen" line on DONE
8. Betaflight-autoconfig description overstating scope (mixer/motor outputs)

---

## 11. Synchronization recommendations (priority order)

1. **Decide source of truth per surface.** Recommendation: TSX is truth for Dashboard/Settings/RX Bind/Diagnostics/History; prototypes are refreshed to match. Exception: License page stays a design spec, clearly labeled "not implemented".
2. **High-priority prototype updates (operator safety/truthfulness):**
   - Remove `Eject`/`Skip` buttons and the license-lock banners (features that don't exist).
   - Add the SafetyBanner hold-to-confirm flow to `rxbind.html`.
   - Fix Betaflight-autoconfig description and History filters (prototype currently promises behavior the app doesn't have).
   - Sync copy: "Reboot into DFU", "Select at least one RX.", "plug battery…", "⚠ this board failed N× before", stage-prefixed error lines.
3. **Medium priority:** add missing slot-state examples (at minimum `MOTOR_TEST`, `ENTERING_DFU`, `ABORTED`, and a `PREP ESC` ESC-only card), the ErrorHintCard, batch-complete banner, and per-slot `next:` badge.
4. **Low priority (pixel/format parity):** tally format, duration `8.3s` vs `8.3 s`, colon punctuation in History detail rows, capitalisation of "ping timeout (ms)", "Upload .bin" vs "+ Upload .bin".
5. **Process:** add a checklist item to the prototype-refresh workflow — after any `apps/web/src` string/label change, diff against these prototypes. Consider generating the terminology table of this report mechanically (JSX string extraction) in CI to catch future drift.
