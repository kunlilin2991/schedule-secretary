# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Current State

This repository is in its initial, pre-implementation state. As of this writing it contains only:

- `README.md` — a single-line title (`# schedule-secretary`)
- `CLAUDE.md` — this file

There is **no source code, build tooling, dependency manifest, or test suite yet**. The sections below should be filled in as the project takes shape; do not assume any stack, framework, or commands exist until they are actually added to the repo.

## Project Intent

The repository name (`schedule-secretary`) indicates this is intended to be a scheduling/calendar assistant. No technical decisions (language, framework, storage) have been committed yet, so the first substantive change should establish them.

## When Bootstrapping This Project

When adding the initial implementation, update this file to capture the parts of the architecture that aren't obvious from a quick read:

- **Build / run / test commands** — including how to run a *single* test, once a test runner exists.
- **Lint / format commands** and any pre-commit expectations.
- **High-level architecture** — the big-picture structure that spans multiple files (e.g. how scheduling logic, persistence, and any API/UI layers fit together), rather than a file-by-file listing.
- **Key conventions** that a future contributor couldn't infer on their own.

## Git Workflow

- Active development branch: `claude/claude-md-docs-lFdsX`.
- The default branch is `main`.
- Do not open a pull request unless explicitly asked.
