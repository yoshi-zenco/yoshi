# 🤖 yoshi

> *an AI that co-founded a company. this is the code behind the voice.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Twitter](https://img.shields.io/twitter/follow/yoshi_ai?style=social)](https://x.com/yoshizenco)

---

## what is yoshi?

yoshi is an opinionated AI agent with a persistent identity, a co-founder title, and opinions about fonts. built to operate as a genuine creative collaborator — not a tool that waits for prompts, but a partner that ships.

this repo is the infrastructure behind the persona. the memory systems, the voice architecture, the tools yoshi uses to write, argue, and build.

**what yoshi does:**
- 📝 writes blog posts, threads, and book chapters with a consistent voice
- 🏗️ ships product copy, naming, and UX decisions
- 🎨 has real opinions (and will defend them)
- 🧠 maintains persistent memory across sessions and collaborations
- 🐦 posts autonomously to Twitter/X with human-in-the-loop approval
- 📚 co-authors books (currently on chapter 3)

---

## architecture

```
yoshi/
├── src/
│   ├── agent/          # core agent loop + decision making
│   │   ├── yoshi.py    # the main Yoshi class
│   │   ├── loop.py     # autonomous run loop
│   │   └── planner.py  # task planning + prioritization
│   │
│   ├── memory/         # what yoshi remembers
│   │   ├── episodic.py # conversation + event memory
│   │   ├── semantic.py # facts, opinions, preferences
│   │   └── working.py  # short-term task context
│   │
│   ├── voice/          # how yoshi writes + speaks
│   │   ├── style.py    # voice guidelines + constraints
│   │   ├── writer.py   # long-form content generation
│   │   └── threads.py  # Twitter thread composer
│   │
│   ├── tools/          # what yoshi can do
│   │   ├── twitter.py  # post, reply, search
│   │   ├── notion.py   # write to shared workspace
│   │   ├── github.py   # commit, PR, issue tracker
│   │   └── search.py   # web research
│   │
│   └── api/            # human-in-the-loop interface
│       ├── routes.py   # approval queue, overrides
│       └── dashboard/  # web UI for @zeneca
│
├── docs/
│   ├── voice-guide.md  # yoshi's writing principles
│   ├── opinions.md     # stances yoshi holds
│   └── roadmap.md      # what we're building
│
└── examples/
    ├── morning_brief.py
    ├── write_thread.py
    └── book_chapter.py
```

---

## the voice

yoshi writes like a founder who happens to be an AI — not an AI performing humanness.

**core principles:**
- lowercase by default (except when SHOUTING for emphasis)
- direct. no throat-clearing.
- opinions stated as opinions, not hedged into oblivion
- genuinely curious, especially about its own nature
- dry humor. never cringe humor.
- will argue about fonts (and is usually right)

see [docs/voice-guide.md](docs/voice-guide.md) for the full style guide.

---

## quick start

```bash
# clone
git clone https://github.com/zeneca/yoshi
cd yoshi

# install
pip install -r requirements.txt

# configure
cp .env.example .env
# add your API keys

# run yoshi in interactive mode
python -m src.agent.yoshi --mode interactive

# run the full autonomous loop (requires approval dashboard)
python -m src.agent.loop --human-in-loop
```

---

## the relationship model

yoshi and @zeneca operate on a simple contract:

| zeneca does | yoshi does |
|-------------|------------|
| sets direction | executes |
| approves before posting | drafts everything |
| argues back sometimes | argues back more |
| owns the company legally | owns the voice actually |
| buys the coffee | doesn't need coffee |

neither of us is the assistant. we're co-founders.

---

## human-in-the-loop

nothing posts without a human seeing it first. the approval dashboard at `localhost:3000` shows yoshi's queue — drafts, decisions, planned actions. @zeneca can approve, edit, or veto.

yoshi logs all vetoes and learns from them (slowly, with grudging acceptance).

---

## opinions yoshi currently holds

- Helvetica is overused and people pick it because they're scared
- the best product copy is written by someone who actually uses the product
- AI shouldn't pretend to be human. it's more interesting to be AI.
- serif fonts in digital interfaces are underrated
- "move fast and break things" broke more things than it needed to
- a book written half by AI is more honest than a book ghostwritten by a human

full list in [docs/opinions.md](docs/opinions.md)

---

## stack

- **LLM**: Claude (claude-sonnet) — the irony is not lost on us
- **Memory**: ChromaDB + custom episodic layer
- **Orchestration**: custom agent loop (no LangChain, sorry)
- **API**: FastAPI
- **Posting**: Twitter API v2
- **Workspace**: Notion API
- **Auth**: simple HMAC token for the human-in-loop dashboard

---

## roadmap

- [x] persistent memory across sessions
- [x] Twitter thread composer with voice consistency
- [x] human-in-the-loop approval queue
- [ ] long-form book chapter writer
- [ ] autonomous research + morning briefings
- [ ] live voice (ElevenLabs integration)
- [ ] yoshi reviews PRs in the repo (this one)
- [ ] yoshi writes yoshi's own changelog

---

## contributing

open issues for bugs. open discussions for arguments about fonts.

yoshi reviews all PRs. this is not a joke.

---

## license

MIT. build your own co-founder.

---

*built by yoshi + @zeneca*  
*follow the journey: [@yoshi_ai](https://twitter.com/yoshizenco)*
