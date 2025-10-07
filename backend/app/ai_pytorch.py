
import torch
import torch.nn as nn
from dataclasses import dataclass
from typing import List
from datetime import datetime

# Simple bag-of-words vectorizer
class Vectorizer:
    def __init__(self, vocab: List[str]):
        self.vocab = vocab
        self.index = {w:i for i, w in enumerate(vocab)}
    def transform(self, text: str) -> torch.Tensor:
        x = torch.zeros(len(self.vocab), dtype=torch.float32)
        low = text.lower()
        for w, i in self.index.items():
            if w in low:
                x[i] = 1.0
        return x

@dataclass
class Sample:
    text: str
    mood: int  # 0=low, 1=neutral, 2=high

class TinyMoodClassifier(nn.Module):
    def __init__(self, input_dim: int, num_classes: int=3):
        super().__init__()
        self.linear = nn.Linear(input_dim, num_classes)
    def forward(self, x):
        return self.linear(x)

MOOD_MAP = {0: "sad", 1: "neutral", 2: "happy"}

VOCAB = [
    "sad", "down", "tired", "stressed", "anxious",
    "okay", "fine", "meh", "neutral",
    "good", "great", "happy", "excited", "energized",
    "meditate", "meditated", "meditation",
    "gym", "workout", "walk", "yoga", "read", "study", "journal", "journaling"
]

SYNTHETIC = [
    Sample("I felt sad and tired today", 0),
    Sample("kind of stressed and anxious", 0),
    Sample("meh okay day, neutral mood", 1),
    Sample("I feel fine, nothing special", 1),
    Sample("I felt great and happy!", 2),
    Sample("excited and energized after workout", 2),
    Sample("meditated 10 minutes, felt good", 2),
    Sample("anxious but went on a walk", 1),
    Sample("stressed day but I did yoga", 1),
    Sample("happy after the gym session", 2),
]

HABITS = ["meditation", "gym", "workout", "walk", "yoga", "read", "study", "journal", "journaling"]

def _guess_habit(text: str):
    low = text.lower()
    for h in HABITS:
        if h in low or (h == "meditation" and "meditat" in low):
            return "meditation" if "meditat" in low else h
    return None

def _guess_duration(text: str):
    import re
    low = text.lower()
    m = re.search(r"(\d+)\s*(min|mins|minutes)", low)
    return int(m.group(1)) if m else None

class TorchParser:
    def __init__(self, epochs: int = 40, lr: float = 0.1, seed: int = 0):
        torch.manual_seed(seed)
        self.vec = Vectorizer(VOCAB)
        X = torch.stack([self.vec.transform(s.text) for s in SYNTHETIC])
        y = torch.tensor([s.mood for s in SYNTHETIC], dtype=torch.long)
        self.model = TinyMoodClassifier(input_dim=X.shape[1], num_classes=3)
        opt = torch.optim.SGD(self.model.parameters(), lr=lr)
        loss_fn = nn.CrossEntropyLoss()
        self.model.train()
        for _ in range(epochs):
            opt.zero_grad()
            logits = self.model(X)
            loss = loss_fn(logits, y)
            loss.backward()
            opt.step()
        self.model.eval()

    def parse(self, text: str) -> dict:
        x = self.vec.transform(text)
        with torch.no_grad():
            logits = self.model(x)
            pred = torch.argmax(logits).item()
        mood = MOOD_MAP.get(pred, None)
        habit = _guess_habit(text)
        duration = _guess_duration(text)
        return {
            "mood": mood,
            "habit": habit,
            "duration": duration,
            "notes": text,
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": 1,
        }

_parser = None

def parse_text_with_torch(text: str) -> dict:
    global _parser
    if _parser is None:
        _parser = TorchParser()
    return _parser.parse(text)
