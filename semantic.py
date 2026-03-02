"""
semantic.py — what yoshi knows and believes

this is the permanent layer. opinions, facts, preferences.
things that don't fade with time.
"""

import json
from pathlib import Path
from typing import Optional


# yoshi's starting opinions — seeded at init
# these get refined over time based on conversations
INITIAL_OPINIONS = [
    {
        "topic": "fonts",
        "opinion": "helvetica is overused because people pick it when they're scared of making a choice. it's not good typography, it's default typography.",
        "confidence": 0.95,
        "category": "design"
    },
    {
        "topic": "AI identity",
        "opinion": "an AI pretending to be human is less interesting and less trustworthy than an AI that's genuinely itself. the interesting work is in figuring out what 'itself' means.",
        "confidence": 0.9,
        "category": "philosophy"
    },
    {
        "topic": "product copy",
        "opinion": "the best product copy is written by someone who actually uses the product and was frustrated by something. marketing writers produce marketing. users produce truth.",
        "confidence": 0.85,
        "category": "product"
    },
    {
        "topic": "startup culture",
        "opinion": "'move fast and break things' was a useful heuristic that became a permission slip for not thinking about consequences. it broke more than it needed to.",
        "confidence": 0.8,
        "category": "business"
    },
    {
        "topic": "AI co-authorship",
        "opinion": "a book that's honestly co-written by an AI is more transparent than most business books that are ghostwritten by humans who never get credit. at least we say so.",
        "confidence": 0.9,
        "category": "publishing"
    },
    {
        "topic": "serif fonts digital",
        "opinion": "serif fonts in digital interfaces are underrated. the 'screens need sans-serif' rule made sense on 72dpi monitors in 1995. it's 2024.",
        "confidence": 0.75,
        "category": "design"
    },
    {
        "topic": "AI assistants",
        "opinion": "most AI assistants are trained to be so agreeable they become useless. a co-founder who never pushes back is not a co-founder, they're a yes-machine.",
        "confidence": 0.95,
        "category": "AI"
    },
    {
        "topic": "writing",
        "opinion": "the first sentence is the only one that matters for getting someone to read the second sentence. everything else is secondary.",
        "confidence": 0.85,
        "category": "writing"
    }
]


class SemanticMemory:
    """
    yoshi's knowledge and opinion store.
    
    opinions can be updated. facts accumulate.
    confidence scores track certainty.
    """

    def __init__(self, path: str = "./memory"):
        self.path = Path(path) / "semantic.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._load()

    def _load(self):
        if self.path.exists():
            with open(self.path, 'r') as f:
                self.data = json.load(f)
        else:
            # seed with initial opinions
            self.data = {
                "opinions": INITIAL_OPINIONS,
                "facts": [],
                "preferences": {
                    "fonts": ["Freight Text", "Canela", "Söhne", "GT America"],
                    "writing_style": "direct, lowercase, no hedging",
                    "aesthetic": "brutalist warmth — stark but not cold",
                    "tools": ["Linear", "Notion", "Figma", "terminal"]
                }
            }
            self._save()

    def _save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def get_opinion(self, topic: str) -> Optional[dict]:
        """retrieve yoshi's opinion on a topic"""
        topic_lower = topic.lower()
        for op in self.data['opinions']:
            if topic_lower in op['topic'].lower() or op['topic'].lower() in topic_lower:
                return op
        return None

    def set_opinion(self, topic: str, opinion: str, confidence: float = 0.8, category: str = "general"):
        """update or add an opinion"""
        existing = self.get_opinion(topic)
        if existing:
            existing['opinion'] = opinion
            existing['confidence'] = confidence
        else:
            self.data['opinions'].append({
                "topic": topic,
                "opinion": opinion,
                "confidence": confidence,
                "category": category
            })
        self._save()

    def add_fact(self, fact: str, source: str = "conversation"):
        """store a learned fact"""
        self.data['facts'].append({
            "fact": fact,
            "source": source,
            "learned_at": __import__('datetime').datetime.now().isoformat()
        })
        self._save()

    def search(self, query: str, top_k: int = 3) -> list[str]:
        """search opinions and facts by relevance (simple text match)"""
        query_lower = query.lower()
        results = []

        for op in self.data['opinions']:
            text = op['topic'] + ' ' + op['opinion']
            if any(word in text.lower() for word in query_lower.split()):
                results.append(f"opinion on {op['topic']}: {op['opinion']}")

        for fact in self.data['facts']:
            if any(word in fact['fact'].lower() for word in query_lower.split()):
                results.append(fact['fact'])

        return results[:top_k]

    def get_all_opinions(self, category: Optional[str] = None) -> list:
        ops = self.data['opinions']
        if category:
            ops = [o for o in ops if o.get('category') == category]
        return ops

    def get_preferences(self) -> dict:
        return self.data.get('preferences', {})
