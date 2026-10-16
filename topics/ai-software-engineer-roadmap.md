---
title: "AI Software Engineer Roadmap"
notion_id: 3fbebef13b84817e9660fd39a5c1970c
notion_url: https://www.notion.so/3fbebef13b84817e9660fd39a5c1970c
last_edited: 2026-10-16T05:40:47.336Z
icon: "🧭"
---

[Architect](../README.md) / [Topics](README.md)

# 🧭 AI Software Engineer Roadmap

> 🎯 **Goal:** Graduate ready to land a job as an AI software engineer — someone who builds real products on top of AI models (LLM apps, agents, ML features), not just someone who studied AI theory.

**How to use this roadmap:** Each phase lines up roughly with a year of a 4-year degree. Move faster if you can. The most important rule: **build something at every stage.** Projects and shipped work matter more than certificates.

---

## Phase 1 — Programming Foundations (Year 1)

**Goal:** Become a confident programmer who can build and debug small programs alone.

### Learn

- [ ] **Python** — your main language. Data types, functions, OOP, modules, virtual environments, packages (pip / uv)
- [ ] **A second language** — JavaScript/TypeScript (for web) or Java/C++ (for fundamentals)
- [ ] **Git & GitHub** — commits, branches, pull requests, writing a good README
- [ ] **Command line & Linux basics** — navigating, files, permissions, running scripts
- [ ] **Data structures & algorithms** — arrays, hash maps, linked lists, trees, graphs, sorting, searching, Big O
- [ ] **Basic SQL** — SELECT, JOIN, GROUP BY, simple schema design

### Math to start

- [ ] Linear algebra basics — vectors, matrices, dot product
- [ ] Discrete math & logic

### Build

- [ ] 3–5 small Python projects (CLI tool, web scraper, simple game, automation script)
- [ ] Put every project on GitHub with a README

### Milestone ✅

You can solve easy/medium coding problems and build a small program from scratch without a tutorial.

---

## Phase 2 — Software Engineering Core (Year 2)

**Goal:** Learn to build real, full applications the way companies do.

### Learn

- [ ] **Backend development** — REST APIs with FastAPI (Python) or Node.js
- [ ] **Databases** — PostgreSQL, normalization, indexes, an ORM (SQLAlchemy / Prisma)
- [ ] **Frontend basics** — HTML, CSS, React or Next.js (enough to build a UI for your apps)
- [ ] **Testing** — unit tests with pytest, basic integration tests
- [ ] **Docker** — containerize your apps
- [ ] **Clean code & design patterns** — SOLID, separation of concerns, repository pattern
- [ ] **Networking basics** — HTTP, DNS, TCP, how the web works

### Math to continue

- [ ] Calculus — derivatives, chain rule, gradients
- [ ] Probability & statistics — distributions, mean/variance, Bayes' theorem

### Build

- [ ] A full-stack app with auth, database and a deployed URL (e.g. task manager, expense tracker)
- [ ] Deploy at least one app to the cloud (Azure, AWS, GCP, Vercel or Render)

### Milestone ✅

You can build, test, containerize and deploy a full-stack web app.

---

## Phase 3 — Machine Learning & AI Fundamentals (Year 3)

**Goal:** Understand how models work so you can use them wisely, debug them and explain them in interviews.

### Learn — Classical ML

- [ ] NumPy, Pandas, Matplotlib — data handling and visualization
- [ ] scikit-learn — regression, classification, clustering, train/test splits, cross-validation
- [ ] Model evaluation — accuracy, precision, recall, F1, overfitting vs underfitting
- [ ] Feature engineering and data cleaning

### Learn — Deep Learning

- [ ] Neural networks, backpropagation, gradient descent
- [ ] **PyTorch** — tensors, training loops, datasets
- [ ] CNNs (images) and the basics of sequence models
- [ ] **Transformers & attention** — how LLMs work: tokens, embeddings, context windows

### Recommended courses

- [ ] Machine Learning Specialization — Andrew Ng (Coursera)
- [ ] Deep Learning Specialization — Andrew Ng, or [fast.ai](http://fast.ai) Practical Deep Learning
- [ ] Andrej Karpathy — Neural Networks: Zero to Hero (YouTube)

### Build

- [ ] An end-to-end ML project: collect data → train → evaluate → serve with a FastAPI endpoint
- [ ] One Kaggle competition or dataset project with a written-up notebook

### Get experience

- [ ] Apply for internships (software or ML) — start applying early in Year 3

### Milestone ✅

You can train, evaluate and serve a model, and explain how a transformer works.

---

## Phase 4 — AI Engineering & Specialization (Year 4)

**Goal:** Build production-quality AI applications — this is the core of the AI software engineer job.

### Learn — LLM application development

- [ ] **Using LLM APIs** — Claude, OpenAI, Gemini; open-source models via Hugging Face / Ollama
- [ ] **Prompt & context engineering** — system prompts, few-shot examples, structured outputs (JSON)
- [ ] **RAG (Retrieval-Augmented Generation)** — chunking, embeddings, vector databases (pgvector, Pinecone, Chroma), reranking
- [ ] **Tool use & agents** — function calling, agent loops, multi-step workflows
- [ ] **MCP (Model Context Protocol)** — connecting models to tools and data
- [ ] **Frameworks** — LangChain / LangGraph, LlamaIndex, Claude Agent SDK (learn what they do, but understand how to build without them too)
- [ ] **Streaming responses** in APIs and UIs

### Learn — Production concerns

- [ ] **Evaluation (evals)** — how to measure if your AI app actually works; test sets, LLM-as-judge
- [ ] **Observability** — logging, tracing (LangSmith, Langfuse)
- [ ] **Cost & latency** — caching, model selection, token budgets
- [ ] **Safety** — prompt injection, data privacy, guardrails
- [ ] **MLOps basics** — model versioning, CI/CD, monitoring
- [ ] **Cloud AI services** — Azure AI Foundry / AWS Bedrock / Google Vertex AI

### Learn — System design

- [ ] Scalability, caching (Redis), queues, microservices vs monolith
- [ ] Designing AI systems — e.g. "design a customer support chatbot"

### Build (your portfolio centerpiece)

- [ ] **A RAG app** — chat with your own documents, with citations and evals
- [ ] **An AI agent** — uses tools to complete real tasks (e.g. research agent, coding helper)
- [ ] **Final year project** — choose an AI product that solves a real problem; deploy it, get real users

### Milestone ✅

You have 2–3 deployed AI projects with clean code, tests and evals that you can demo and explain in depth.

---

## Ongoing — Throughout All 4 Years

### Use AI coding tools well

- [ ] Learn Claude Code, Cursor or GitHub Copilot — but always understand and review the code they write

### Build your profile

- [ ] Keep GitHub active with real projects
- [ ] LinkedIn profile with projects and skills
- [ ] Write blog posts or short write-ups about what you build
- [ ] Contribute to an open-source AI project (docs fixes and small issues count)

### Community

- [ ] Join hackathons — great for fast learning and networking
- [ ] Join AI/dev communities, meetups and university tech clubs

### Stay current

- [ ] Follow AI engineering blogs (Anthropic, OpenAI, Hugging Face, Simon Willison)
- [ ] Read one important paper per month — start with "Attention Is All You Need"

### Interview prep (start in Year 3)

- [ ] LeetCode — focus on medium problems
- [ ] System design practice
- [ ] ML/LLM concept questions — be ready to explain RAG, embeddings, transformers, evals
- [ ] Practice explaining your projects clearly: problem → approach → trade-offs → results

---

## Skills Checklist at Graduation

- [ ] Strong Python + one more language
- [ ] Data structures, algorithms and solid CS fundamentals
- [ ] Can build and deploy full-stack apps
- [ ] Understands ML fundamentals and how LLMs work
- [ ] Can build RAG systems and AI agents
- [ ] Knows how to evaluate, monitor and secure AI apps
- [ ] Comfortable with Docker, Git, cloud and CI/CD
- [ ] Portfolio of 2–3 deployed AI projects
- [ ] At least one internship or real-world project experience
