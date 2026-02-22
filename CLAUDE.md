# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

1. Copy `settings.py.template` → `settings.py` and configure preferences
2. Copy `.env.template` → `.env` and fill in API credentials (`VULTR_API_KEY`, `CLOUDFLARE_EMAIL`, `CLOUDFLARE_API_KEY`)
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python main.py`

There are no automated tests, build scripts, or linting configurations in this project.

## Architecture

PyVultr is a menu-driven CLI for managing Vultr cloud instances and Cloudflare DNS. It has three layers:

**API Layer (`api/`)** — Base `Api` class provides HTTP methods; `Vultr` and `Cloudflare` subclasses add provider-specific auth and response handling.

**Endpoint Layer (`endpoints/`)** — Business logic organized by provider (`vultr/`, `cloudflare/`) and resource type. Each module handles a specific resource (instances, firewall, plans, regions, snapshots, DNS zones).

**UI Layer** — `menu.py` is the central CLI router (~600 lines) that coordinates all user interactions. `util.py` provides shared helpers for printing menus, handling user input, formatting output, and timezone conversion.

**Entry point:** `main.py` loads `.env`, validates required runtime variables, instantiates API clients, and launches `Menu`.

**Data caching:** `data.py` loads cached JSON from `data/*.json` (plans, regions, OS, applications). These files are pre-populated from the Vultr API and used to avoid repeated API calls for static data. Cloud-init profiles (`data/*.yml`) can be loaded locally or from HTTP URLs.

**Settings:** `settings.py` controls preference filtering (e.g., `PREFERRED_PLANS_ONLY`, `PREFERRED_PLAN_IDS`) and optional features like email notifications and cloud-init profiles.

## Key Files

- [main.py](main.py) — Entry point; runtime config validation
- [menu.py](menu.py) — CLI menu router; coordinates all user flows
- [util.py](util.py) — Shared UI helpers, input handling, formatting
- [data.py](data.py) — Data cache loading
- [api/api.py](api/api.py) — Base HTTP client
- [api/vultr.py](api/vultr.py) — Vultr API v2 client
- [api/cloudflare.py](api/cloudflare.py) — Cloudflare v4 API client
- [endpoints/vultr/instance.py](endpoints/vultr/instance.py) — Instance lifecycle (~580 lines)
- [endpoints/vultr/firewall.py](endpoints/vultr/firewall.py) — Firewall rules (~600 lines)
- [settings.py.template](settings.py.template) — Reference for all available settings
- [.env.template](.env.template) — Reference for required environment variables
