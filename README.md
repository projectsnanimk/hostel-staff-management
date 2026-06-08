# Mahesh Hostel Staff Core™ — Management & Attendance Ecosystem

A premium, highly responsive, and mobile-friendly **Mahesh Hostel Staff Management Website** designed with a full-stack Python Flask backend and an advanced Tailwind CSS frontend interface. Supports SQLite data synchronization, QR code employee ID card scanning, printable ID card layout formatting, dynamic salary PDF report exports, and an administrative onboarding approval queue.

---

## 🛠️ Tech Stack & Key Integrations

* **Backend Engine**: Python 3.14 + Flask (Fast, lightweight RESTful web API).
* **Database Layer**: SQLite 3 (Instant, file-based, preloaded with comprehensive seeding).
* **Frontend Framework**: Modern Single Page Application structure with native ES6 JavaScript.
* **Design & Styling**: **Tailwind CSS v3** (CDN-backed) with customized HSL glassmorphism, responsive grids, and micro-animations.
* **QR Scanner Engine**: `html5-qrcode` integration (utilizes the user's web camera or smartphone camera). Includes a **Scan Simulator Console** for local testing without physical cameras.
* **PDF Compiler**: Client-side **jsPDF** for professional structured budget sheets.
* **ID Card Layout**: Embedded **QR Server API** with custom `@media print` CSS isolating printable CR80 standard dimensions (2.125" × 3.375").

---

## 📂 Project Directory Structure

```text
project/
├── app.py                   # Main Flask Backend Server & SQLite Initializer
├── schema.prisma            # Prisma-compatible database representation model
├── README.md                # System Setup & Reference Guide
└── templates/
    └── index.html           # Premium responsive Single Page UI (Tailwind CSS)
```

---

## 🚀 Setup & Execution Guide

Follow these simple steps to install dependencies, initialize the database, and launch the server.

### Step 1: Install Flask Dependency
Since Python is already configured on your system, install the Flask package via `pip` from your terminal:
```bash
pip install flask
```

### Step 2: Launch the Web Application
Start the server in the project directory:
```bash
python app.py
```

Upon launching, the system will output:
```text
Seeding database with modern, premium mock data...
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.5000 (Press CTRL+C to quit)
```

### Step 3: Open in Browser
Visit the following URL to access the platform:
👉 **[http://localhost:5000](http://localhost:5000)**

---

## 💎 Features Walkthrough

### 1. Unified Sticky Role Switcher
* Located at the top right of the dashboard.
* Click **"Admin Access"** or **"Incharge Access"** to seamlessly toggle panels for fast, interactive local testing.

### 2. Module 1: Admin Panel Dashboard (Full Access)
* **Overview Dashboard**: Tracks statistics (Active Approved Staff, Pending Applications, Daily Scans, and Assets) alongside recent scans lists.
* **Staff Records**:
  * **Active Staff**: Interactive search bar with instant filter and detailed profile overview.
  * **Approval Queue**: Dynamic grid of incoming onboarding requests with **Approve** and **Reject** control actions.
* **Salary Tracker**: Complete monthly ledger displaying base salary, calculated allowances, calculated deductions, and final net payouts. Includes a **"Generate PDF Salary Report"** button downloading a legal financial budget audit.
* **ID Card Generator**: Pick any active employee to render a printable vertical identity card complete with high-res rounded photo and barcode. Clicking **"Print ID Card"** isolates the card, hides the website interface, and loads the native system print box scaled to credit-card size.
* **Asset Manager**: Complete CRUD operations to add new items, modify existing quantities or conditions, or delete depreciated inventory.

### 3. Module 2: Incharge Panel Dashboard (Restricted)
* **QR Attendance Scanner**: 
  * Live camera viewport bracket with an animated laser scanning bar.
  * **Webcam Simulator Console**: Select any employee from the simulated drop-down list to execute a virtual scan instantly, showing exactly how attendance records log, verify, and highlight duplication limits.
* **Quick Onboarding Form**: A form with Indian standard validations (e.g., Aadhar 12-digit format, phone number, salary limits) and a **Profile Avatar Picker** with high-resolution presets. Submissions log instantly in the SQLite database under `Pending` status.
