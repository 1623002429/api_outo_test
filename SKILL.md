---
name: api-auto-test-framework-skill
description: Build, update, explain, and generate examples for a Python requests + pytest + Allure API automation framework using YAML test data, context extraction, Chinese assertion logs, module-based Allure reports, cURL-to-YAML conversion, skip cases, debug single cases, and reusable framework templates. Use when the user asks for interface automation scripts, adding modules or test data, generating examples from captured API requests/responses, packaging or updating this API test framework skill, or explaining how to run/debug/report this framework.
---

# API Auto Test Framework

Use this skill when helping the user work with their Python API automation framework.

## Bundled Assets

- Full framework template: `assets/framework-template`
- Framework package root inside the template: `assets/framework-template/api_auto_test`
- cURL/YAML converter: `assets/converter`
- Detailed workflow reference: `references/workflow.md`

When the user asks for a new framework copy or example, copy `assets/framework-template` as the starting project and edit the copied files. Do not edit runtime output into the skill package.

## Core Rules

- Keep the framework based on `requests + pytest + allure-pytest + loguru + PyYAML + jsonpath-ng`.
- Store test cases in YAML files under `api_auto_test/data`.
- Store shared config in `api_auto_test/config`.
- Put reusable request/assert/extract logic under `api_auto_test/common`.
- Put generated Allure output under `api_auto_test/reports` only at runtime.
- Put logs under `api_auto_test/logs` only at runtime.
- Use `data/runtime_context.json` only as runtime context cache; never package it as a fixed example.

## Before Acting

Read `references/workflow.md` when the user asks how to:

- add a new module or YAML case;
- convert captured cURL/request data into YAML;
- debug one case;
- skip cases;
- run all cases and generate reports;
- explain framework files;
- package or refresh this skill.

## Packaging Rule

When updating this skill, include the current full framework and examples, but exclude runtime-generated content:

- `api_auto_test/reports`
- `api_auto_test/logs`
- `api_auto_test/data/runtime_context.json`
- `__pycache__`
- `.pytest_cache`
- generated report/cache/temp files

The installable zip must be flat: the zip root must contain `SKILL.md`, `assets`, `references`, and optional `agents` directly.
