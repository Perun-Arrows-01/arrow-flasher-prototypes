# Arrow Flasher — UI Prototypes

Static HTML/CSS/JS prototypes for the Arrow Flasher web UI. These are **presentation-only** mockups — no firmware, USB, flashing, licensing, bind, server, API, or persistence logic.

## How to Open

Open any `.html` file directly in a browser:

```bash
# From the repository root
open app.html        # macOS
xdg-open app.html    # Linux
start app.html       # Windows
```

Or serve locally:

```bash
python3 -m http.server 8080
# Then visit http://localhost:8080/app.html
```

## Pages

| File | Description |
|---|---|
| `app.html` | Main app shell with navigation, slot grid, and session summary |
| `dashboard.html` | Slot cards with all 15 pipeline states, safety banner, batch banner |
| `setup.html` | Settings page: FC/ESC firmware, motor directions, ELRS, motor test, slots table |
| `history.html` | Flash history with filters (result, date range), expandable row details |
| `rxbind.html` | RX binding: scan, select receivers, bind progress |
| `diag.html` | Diagnostics: USB tree, health checks, severity breakdown, quick fixes |
| `license.html` | License configuration (locked state — no TSX counterpart yet) |
| `index.html` | Prototype index with links to all pages |

## Interaction Flows

### Dashboard Slot States (15 total)

The dashboard demonstrates all slot states from the real pipeline (`@arrow-flasher/core`):

| State | Visual | Description |
|---|---|---|
| `EMPTY` | Gray badge | No device connected |
| `ENTERING_DFU` | Blue badge | Requesting DFU mode |
| `DFU_READY` | Green badge | Device in DFU, ready to flash |
| `FLASHING_FC` | Blue badge | Flashing firmware |
| `REBOOTING` | Yellow badge | Rebooting to application mode |
| `HANDSHAKE_MSP` | Blue badge | Establishing MSP connection |
| `WAIT_BATTERY` | Yellow badge | Waiting for battery connection |
| `ENTER_PASSTHROUGH` | Blue badge | Entering passthrough mode |
| `MOTOR_TEST` | Blue badge | Testing motor outputs |
| `BF_AUTOCONFIG` | Blue badge | Betaflight auto-configuration |
| `ELRS_BIND` | Blue badge | ELRS binding in progress |
| `ABORTED` | Orange badge | Flash aborted by user |
| `ERROR` | Red badge + ErrorHint | Failed with recovery hints |
| `DONE` | Green badge + chips | Flash complete |
| Stuck watchdog | Yellow chip | No progress for N seconds |

### Safety Banner

Dashboard includes a **Safety Banner** with 3-second hold-to-confirm bypass (matches TSX `SafetyBanner` component). Hold the "Bypass Safety" button for 3s to bypass safety checks.

### Confirm Dialogs

All destructive actions show confirm dialogs with impact summaries:
- **Reset session**: "This will reset N active slots and clear all session data."
- **Restart server**: "Server restart will interrupt all active flashes."
- **Delete template**: "This will delete template 'X' and cannot be undone."

### History Filters

History page supports:
- **Result filter**: All / Success / Failure
- **Date range**: All time / Last 7 days / Last 24 hours
- **Filter count**: "Showing X of Y sessions"
- **Expandable details**: Click row to show MCU UID, duration, error message

### RX Bind Flow

1. Click "Scan" to discover receivers (2s loading overlay)
2. Select receivers with checkboxes (or "Select all")
3. Click "Bind selected (N)" to start binding
4. Progress bar shows bind status with live counter

### Diagnostics

- **USB tree**: Shows connected devices with VID/PID
- **Health checks**: Lists checks with pass/fail status
- **Severity breakdown**: "Critical: N | Warning: N"
- **Quick fixes**: Actionable suggestions for common issues

## Known Limitations

1. **No real backend**: All data is static mock data. No USB detection, flashing, or persistence.
2. **License page**: No TSX counterpart exists in the real app. Marked as "planned" in navigation.
3. **Navigation order**: Prototype nav order (Dashboard → Setup → History → RX Bind → Diagnostics → License) differs from TSX (Dashboard → History → RX Bind → Settings → Diagnostics).
4. **Slot state coverage**: Prototypes show all 15 states, but real pipeline may have additional sub-states not represented.
5. **No responsive breakpoints**: Layout is desktop-first; mobile/tablet not tested.
6. **No dark/light theme toggle**: Uses GitHub-dark color scheme only.
7. **ErrorHintCard**: Simplified version; real TSX has stage-specific recovery hints with detailed troubleshooting.
8. **SoftDfuFailedToast**: Mock toast shown after 2s on dashboard load for demo purposes.

## Accessibility

All prototypes pass WCAG 2.1 AA static analysis:
- Skip links to main content
- Proper heading hierarchy (h1 → h2 → h3)
- ARIA labels on interactive elements
- Focus-visible rings on all interactive elements
- `prefers-reduced-motion` media query support
- Semantic HTML (tables with `<th scope>`, buttons with `aria-pressed`)

Run the audit:

```bash
python3 a11y-audit.py
```

## TSX Comparison

See `COMPARISON_REPORT.md` for detailed comparison between prototypes and the real React implementation in `apps/web/src/`. Key findings:

- **Terminology gaps**: "Setup" (prototype) vs "Settings" (TSX), missing slot states
- **Missing components**: SafetyBanner, ErrorHintCard, SoftDfuFailedToast, "Mark as DONE" chip
- **Prototype-only features**: License page, History filters, Diag severity counts

## File Structure

```
.
├── app.html              # Main app shell
├── dashboard.html        # Slot cards with all states
├── setup.html            # Settings/configuration
├── history.html          # Flash history
├── rxbind.html           # RX binding
├── diag.html             # Diagnostics
├── license.html          # License (locked)
├── index.html            # Prototype index
├── a11y-audit.py         # WCAG 2.1 AA static analyzer
├── a11y-report.json      # Latest audit results
├── COMPARISON_REPORT.md  # TSX vs HTML comparison
└── README.md             # This file
```

## Design Tokens

Colors (CSS variables):
- `--bg-primary`: `#0d1117` (GitHub dark background)
- `--bg-card`: `#161b22` (Card background)
- `--border`: `#30363d` (Border color)
- `--text-primary`: `#c9d1d9` (Primary text)
- `--text-dim`: `#8b949e` (Dimmed text)
- `--green`: `#4caf50` (Success)
- `--red`: `#ff4444` (Error)
- `--yellow`: `#ffc107` (Warning)
- `--blue`: `#2196f3` (Info)
- `--orange`: `#ff9800` (Caution)

## License

Internal prototype for Arrow Flasher project. Not for distribution.
