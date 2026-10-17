---
title: "Claude Guide"
notion_id: 3fbebef13b8481db8f8bedf404616d42
notion_url: https://www.notion.so/3fbebef13b8481db8f8bedf404616d42
last_edited: 2026-10-16T07:16:46.324Z
icon: "📘"
---

[Architect](README.md)

# 📘 Claude Guide

> 🤖 **For Claude:** read this page before creating, moving, editing or deleting anything in the Architect workspace.

## What this workspace is

The Architect workspace is Gayashan's personal learning library. Almost everything in it is saved learning resources (videos, courses, articles, books) with checkboxes, plus a small number of pages with his own notes. It is organized into **8 hubs**. Every topic page sits directly under a hub, and nothing goes deeper than three levels (hub › page › subpage).

## The 8 hubs

- [Inbox](inbox.md) — quick capture only. New, unsorted links and notes land here and get sorted into a hub later.
- [Now Learning](now-learning/README.md) — what he is actively studying right now: Study Plan, Azure Exams, Learn C and C++, AutoCAD, Blog Site Project. Pages move out to their subject hub once finished.
- [AI](ai/README.md) — AI/ML fundamentals, building with LLMs (RAG, agents, LangChain ecosystem), AI coding tools, and careers in AI.
- [Software Engineering](software-engineering/README.md) — languages (JavaScript, Python), backend, frontend & design, mobile, architecture & system design, DevOps & testing, Microsoft Power Platform.
- [How Computers Work](how-computers-work/README.md) — CS fundamentals: computer architecture, C / C++, Assembly, data structures & algorithms, math, networking, Linux.
- [BISTEC (Work)](bistec-work/README.md) — employer training tracks (Senior Engineer, Tech Lead). Work material with links to company process docs.
- [Career & Business](career-and-business/README.md) — career planning, personal brand, public speaking, YouTube, startups, product & leadership, marketing.
- [Personal Growth](personal-growth/README.md) — learning how to learn, thinking, mind & behavior, better living, personal finance.

## Where new content goes

1. **Search first.** Before creating a page or adding a link, search the workspace for the topic. Add to an existing page whenever one fits; never create a second page for a subject that already has one.
2. **Pick the hub by subject**, using the list above. A few common cases:
   - Anything about LLMs, agents, RAG, MCP, LangChain or AI coding tools → **AI**
   - Low-level or theory topics (CPU, memory, OS internals, algorithms) → **How Computers Work**
   - Frameworks, tools and building apps (FastAPI, Next.js, Docker, Azure) → **Software Engineering**
   - Anything from BISTEC or its training tracks → **BISTEC (Work)**, even when the subject also exists elsewhere; link across instead of moving it.
   - Something he is starting to study now, with a plan or a project → **Now Learning**
3. **Not sure where it belongs?** Put it in **Inbox** and say so, rather than guessing.
4. **Asked to sort the Inbox?** Move each item into its hub, merge it into an existing page if one covers the subject, and list what went where in the reply.

## How pages are written

- **Resource lists use to-do checkboxes:** `- [ ] **Title**` followed by the link, so he can tick off what he has finished. Keep new resources in the same format.
- **Group with headings** (`#`) inside a page, e.g. Tutorials, Courses, Books. Don't create a subpage for a single link; add a heading section instead.
- **Hub pages** hold a one-line description, then `##` headings that group their subpages. When adding a page to a hub, place it under the right heading on the hub page.
- **Page titles** are short and plain ("Next.js", "System Design"), with no emoji in the title. Only hubs have icons.
- **Don't duplicate links.** If the same resource already exists elsewhere, link to that page instead.

## Rules for changing things

- **Read before editing.** Fetch a page before changing it, and make the smallest edit that does the job.
- **Move, don't copy, whenever possible.** Some blocks (bookmark cards, embeds, link previews) are invisible to Claude through the Notion connector and are lost if content is copied into a new page. Moving a whole page keeps them safe.
- **Never delete or trash without an explicit yes.** List the exact pages first and wait for a clear confirmation. Trashing a page also trashes everything under it.
- **Protect his own notes.** These pages contain his own writing, not just links; never rewrite or reorganize their content without asking: Computer Architecture (and First Bug, ENIAC - 1945), Learn C and C++, Power Apps, PL 900, AZ 204, How to break into AIML Engineering, Tailwind CSS 4 - frontend masters, Figma.
- **Keep the depth to three levels.** If a change would nest a page four levels deep, flatten it instead.
- **Report what changed.** After any reorganization, tell him which pages moved, merged, were renamed or trashed.

## Known limitations

- The Notion connector can only see the **Architect** workspace. Other workspaces need the connection switched in Claude's settings.
- Bookmark and embed cards show up as unreadable placeholders, so Claude can't tell what they link to. Ask him, or leave them where they are.
- Claude can move pages to Trash but can't empty Trash; permanent deletion is done by him in Notion.
