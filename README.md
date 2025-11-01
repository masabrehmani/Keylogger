Overview

This repository provides detection heuristics, analysis workflows, reporting templates, and defensive code snippets (non-malicious) that help security practitioners identify and respond to keylogger activity. The materials are intended for incident responders, SOC analysts, and students working in authorized environments.

Important: This project contains no keylogger payloads or instructions to build them. It focuses on detection, analysis and prevention.

Key Features

Hunting playbook: prioritized detection steps for Windows and Linux hosts

Indicators of Compromise (IOCs) checklist and telemetry sources to inspect (processes, autoruns, drivers, DLL hooks)

Forensic collection guidance (memory images, process lists, network captures) and safe handling notes

Example EDR/OS query patterns (high-level) and logging guidance for Splunk/ELK/OSQuery (no exploit code)

Mitigation & hardening checklist: secure input handling, least privilege, MFA, endpoint protection configuration

Report templates (JSON/CSV) and sample incident timeline formats

Why this is useful in cybersecurity

Keyloggers capture credentials and sensitive data; quick detection dramatically reduces risk.

A standard playbook improves triage speed and evidence quality for investigations and audits.

Useful training material for SOC analysts, DFIR engineers, and blue teams.

Detection Guidance (high-level)

Telemetry to monitor

Process creation events (Windows Event 4688) with new/unsigned binaries in user profiles or temp folders.

Unexpected persistent autoruns (registry Run keys, scheduled tasks).

Unusual DLL injection or hooking behavior (keyboard API hooks — detect via EDR heuristics).

Outbound network connections from non-standard processes, especially encrypted streams to unknown endpoints.

Abnormal reading of input devices (rare, but kernel drivers hooking keyboard APIs).

Search examples (conceptual; adapt for your stack)

Splunk: look for ProcessName creating schtasks / writing to HKCU\Software\Microsoft\Windows\CurrentVersion\Run

OSQuery: list autoruns and binaries in %APPDATA% or temp folders, then check file hashes and signatures

EDR: flag processes that call SetWindowsHookEx, GetAsyncKeyState, or use undocumented keyboard drivers (behavioral signature, not implementation)

Forensic & Analysis Workflow (safe)

Isolate the affected host from networks (preserve evidence).

Collect volatile data: process list, open handles, loaded modules, network connections, RAM image (use trusted forensic tools).

Preserve disk: create a forensic copy and record hashes.

Analyze memory image: identify injected modules, suspicious hooks, and unsaved strings. (Use Volatility/Volatility3 — example commands and scripts in this repo.)

Triage: map evil process -> parent process -> persistence mechanism -> exfil target.

Remediate: remove persistence, patch vulnerable vectors, rotate credentials, and rebuild if necessary.

Report: produce a structured incident timeline and evidence package.

Mitigation & Hardening (recommended)

Enforce EDR/antivirus with behavioral blocking and curated telemetry alerts.

Apply principle of least privilege; avoid running daily tasks as admin.

Enable MFA for all sensitive accounts to reduce impact of credential capture.

Harden application whitelisting and block execution from roaming/temporary folders.

Regularly audit autoruns and scheduled tasks.

Safe Tools & References

Volatility 3 — memory analysis workflows (examples in this repo)

OSQuery — endpoint telemetry collection

Sysinternals — Autoruns, Process Monitor, Strings (for triage)

EDR vendor docs for hunting and prevention
