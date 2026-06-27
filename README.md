# Robot Order Automation — Robocorp / Python

![Demo](production-demo.gif)

An end-to-end RPA bot built with Robocorp and the rpaframework that fully automates a multi-step robot ordering workflow: reads order data from CSV, fills and submits a web form for each order, captures a screenshot of the configured robot, exports each receipt as a PDF with the screenshot embedded, and archives all output into a ZIP file.

---

## What It Does

1. **Opens the order portal** — navigates to [RobotSpareBin Industries](https://robotsparebinindustries.com/#/robot-order) and dismisses the modal
2. **Downloads order data** — fetches `orders.csv` via HTTP containing head, body, legs, and delivery address for each robot
3. **Processes each order** — for every row in the CSV:
   - Selects the correct head, body, and leg parts from the form
   - Enters the delivery address
   - Previews the assembled robot
   - Submits the order (with automatic retry on failure, up to 5 attempts)
   - Captures a PNG screenshot of the robot preview
   - Exports the HTML receipt to a PDF
   - Embeds the screenshot into the PDF
   - Clicks "Order another" to loop to the next order
4. **Archives output** — zips all receipts and screenshots into `output/receipts.zip`

---

## Project Structure

```
Production/
├── tasks.py          # Main bot logic (Robocorp task entry point)
├── orders.csv        # Sample order data (head, body, legs, address)
├── conda.yaml        # Python environment definition (RCC-managed)
├── robot.yaml        # Robocorp task configuration
├── .gitignore
└── LICENSE
```

**Output (generated at runtime, gitignored):**
```
output/
├── receipts/
│   ├── receipt_1.pdf     # PDF receipt with embedded robot screenshot
│   ├── receipt_2.pdf
│   └── ...
├── receipts.zip          # Final archive of all receipts
├── screenshots/
│   └── robot_1.png       # Robot preview screenshots
└── log.html              # Robocorp execution log
```

---

## Tech Stack

| Library | Role |
|---|---|
| `robocorp` 3.0.0 | Task runner and framework |
| `robocorp-browser` 2.3.5 | Playwright-based browser automation |
| `rpaframework` 30.0.2 | HTTP download, PDF generation, ZIP archive, CSV/table parsing |
| Python 3.12.8 | Runtime |
| RCC / conda.yaml | Reproducible environment management |

---

## Running the Bot

### Prerequisites
- [RCC](https://github.com/robocorp/rcc) (Robocorp's environment manager) — handles Python and all dependencies automatically

### VS Code
1. Install the [Robocorp Code extension](https://robocorp.com/docs/developer-tools/visual-studio-code/extension-features)
2. Open this folder in VS Code
3. Use the Robocorp side panel → **Run Task**

### Command Line
```bash
# Install RCC (one-time)
# https://github.com/robocorp/rcc?tab=readme-ov-file#getting-started

rcc run
```

RCC reads `conda.yaml` and builds an isolated environment automatically — no manual `pip install` needed.

---

## Key Implementation Details

- **Retry logic** — `submit_order()` retries up to 5 times if the server returns an error, making the bot resilient to transient failures
- **Dynamic output paths** — receipt and screenshot directories are created at runtime with `os.makedirs(exist_ok=True)`
- **PDF embedding** — `RPA.PDF` appends the robot screenshot PNG directly into the receipt PDF using `add_files_to_pdf()`
- **Environment isolation** — all dependencies are pinned in `conda.yaml`, making the bot fully reproducible across machines
- **Slow-mo enabled** — `browser.configure(slowmo=100)` adds a 100ms delay between actions for stability on the target site

---

## Author

**Jeremy Vargo** — Robocorp Certified RPA Developer (Level I, II & III)
- 📧 jeremy.e.vargo@gmail.com
- 💼 [LinkedIn](https://linkedin.com/in/jeremyevargo)
- 🐙 [GitHub](https://github.com/J3R3B3AR)
