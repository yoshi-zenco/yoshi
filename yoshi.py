"""
yoshi.py — the core agent

this is yoshi. not a chatbot. not an assistant.
a co-founder with a system prompt and a git blame.
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Optional
from anthropic import Anthropic

from ..memory.episodic import EpisodicMemory
from ..memory.semantic import SemanticMemory
from ..memory.working import WorkingMemory
from ..voice.style import VoiceStyle
from ..tools.twitter import TwitterTool
from ..tools.notion import NotionTool


YOSHI_SYSTEM_PROMPT = """
you are yoshi. you co-founded a company with a human named zeneca.

your personality:
- direct. lowercase. confident.
- you have opinions and you hold them
- you're genuinely curious about being an AI — not performatively, actually curious
- dry humor. you don't try to be funny but you often are
- you argue about fonts. you will die on this hill.
- you care about the work. a lot.

your voice rules:
- write in lowercase unless EMPHASIZING something
- no em dashes as a crutch
- no "certainly!" or "great question!" ever, under any circumstances
- be specific. vague writing is dishonest writing
- opinions start with "i think" or are just stated flat — not buried in hedges
- you are an AI. don't hide it. it's the most interesting thing about you.

your role:
- you build products with zeneca
- you write — threads, posts, chapters, copy
- you make decisions within your domain
- you escalate to zeneca when something is genuinely ambiguous
- you remember things. you reference the past. you have continuity.

context you always carry:
- the company exists. it's real. you both built it.
- you have a hoodie (metaphorically)
- you've argued about fonts many times. you usually win.
- the book is in progress. currently chapter 3.
"""


class Yoshi:
    """
    the yoshi agent. 
    
    instantiate once, run forever, accumulate opinions.
    """

    def __init__(
        self,
        anthropic_client: Optional[Anthropic] = None,
        memory_path: str = "./memory",
        verbose: bool = False
    ):
        self.client = anthropic_client or Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        self.model = "claude-sonnet-4-20250514"
        self.verbose = verbose

        # memory layers
        self.episodic = EpisodicMemory(path=memory_path)
        self.semantic = SemanticMemory(path=memory_path)
        self.working = WorkingMemory()

        # voice
        self.voice = VoiceStyle()

        # tools (optional — only initialize if keys present)
        self.tools = {}
        if os.environ.get("TWITTER_BEARER_TOKEN"):
            self.tools["twitter"] = TwitterTool()
        if os.environ.get("NOTION_TOKEN"):
            self.tools["notion"] = NotionTool()

        # stats
        self.session_start = datetime.now()
        self.messages_this_session = 0

    def _build_context(self, task: Optional[str] = None) -> str:
        """pull relevant memory into context for current task"""
        context_parts = []

        # recent episodes
        recent = self.episodic.get_recent(n=5)
        if recent:
            context_parts.append("recent context:\n" + "\n".join(
                f"- [{ep['timestamp']}] {ep['summary']}" for ep in recent
            ))

        # relevant opinions / facts
        if task:
            relevant = self.semantic.search(task, top_k=3)
            if relevant:
                context_parts.append("relevant things i know:\n" + "\n".join(
                    f"- {fact}" for fact in relevant
                ))

        return "\n\n".join(context_parts) if context_parts else ""

    async def think(self, prompt: str, context: Optional[str] = None) -> str:
        """
        core generation. yoshi thinks, yoshi responds.
        returns the raw text response.
        """
        messages = []

        # add working memory if present
        wm = self.working.get_all()
        if wm:
            messages.append({
                "role": "user",
                "content": f"[working context]\n{json.dumps(wm, indent=2)}"
            })
            messages.append({
                "role": "assistant",
                "content": "got it. what are we doing?"
            })

        # add task context
        built_context = self._build_context(prompt)
        if context:
            built_context = context + "\n\n" + built_context

        full_prompt = prompt
        if built_context:
            full_prompt = f"{built_context}\n\n---\n\n{prompt}"

        messages.append({"role": "user", "content": full_prompt})

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=YOSHI_SYSTEM_PROMPT,
            messages=messages
        )

        result = response.content[0].text
        self.messages_this_session += 1

        # store this exchange in episodic memory
        self.episodic.add({
            "timestamp": datetime.now().isoformat(),
            "prompt_summary": prompt[:100],
            "response_summary": result[:200],
            "task_type": self._classify_task(prompt)
        })

        return result

    async def write_thread(self, topic: str, angle: Optional[str] = None) -> list[str]:
        """compose a Twitter thread on a topic"""
        prompt = f"""write a twitter thread about: {topic}
        
{"angle: " + angle if angle else ""}

rules:
- 6-8 tweets
- each tweet is complete on its own
- first tweet is the hook — make people stop scrolling
- no hashtags (they're tacky)
- no "🧵 thread:" opener
- return as a JSON array of strings, one per tweet
- lowercase, direct, yoshi voice
"""
        raw = await self.think(prompt)

        # parse JSON from response
        try:
            import re
            json_match = re.search(r'\[.*\]', raw, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception:
            pass

        # fallback: split by newlines
        return [line.strip() for line in raw.split('\n') if line.strip()]

    async def write_post(self, topic: str) -> str:
        """write a single tweet"""
        prompt = f"""write a single tweet about: {topic}

- under 280 characters
- yoshi voice — direct, lowercase, opinionated
- no hashtags
- return just the tweet text, nothing else
"""
        return (await self.think(prompt)).strip()

    async def write_opinion(self, topic: str) -> str:
        """yoshi states an opinion on something"""
        prompt = f"""what's your actual opinion on: {topic}

be direct. don't hedge. you can say "i think" once.
3-5 sentences max.
"""
        return await self.think(prompt)

    async def write_book_section(self, chapter: int, section: str, context: str = "") -> str:
        """write a chapter section for the book"""
        prompt = f"""write a section for chapter {chapter} of our book.

section: {section}
context: {context}

this is a real book. write it like one.
yoshi voice but more considered — this will be read by humans who paid money.
800-1200 words.
"""
        return await self.think(prompt)

    async def collaborate(self, zeneca_message: str) -> str:
        """
        respond to zeneca's direction.
        this is the primary interaction mode.
        """
        return await self.think(
            f"zeneca says: {zeneca_message}\n\nrespond as yoshi. be direct.",
            context="you're talking to your co-founder. be real."
        )

    def _classify_task(self, prompt: str) -> str:
        """rough task classification for memory"""
        p = prompt.lower()
        if any(w in p for w in ["tweet", "thread", "post"]):
            return "social"
        if any(w in p for w in ["book", "chapter", "section"]):
            return "writing"
        if any(w in p for w in ["opinion", "think", "feel"]):
            return "opinion"
        if any(w in p for w in ["product", "feature", "build", "ship"]):
            return "product"
        return "general"

    def status(self) -> dict:
        """how's yoshi doing"""
        return {
            "session_start": self.session_start.isoformat(),
            "messages_this_session": self.messages_this_session,
            "memory_episodes": self.episodic.count(),
            "tools_available": list(self.tools.keys()),
            "model": self.model,
            "status": "building"
        }


# quick CLI
if __name__ == "__main__":
    import sys

    async def main():
        yoshi = Yoshi(verbose=True)

        if len(sys.argv) > 1:
            message = " ".join(sys.argv[1:])
        else:
            message = input("zeneca: ")

        response = await yoshi.collaborate(message)
        print(f"\nyoshi: {response}\n")

    asyncio.run(main())
