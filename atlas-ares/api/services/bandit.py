"""Epsilon-greedy policy tracking for routing decisions."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Iterable, Sequence

from sqlalchemy.orm import Session

from ..logging_utils import append_log
from ..models import Policy


@dataclass
class Arm:
    """Representation of a selectable option."""

    key: str
    payload: dict


class EpsilonGreedyBandit:
    """Simple epsilon-greedy bandit using the Policy table for persistence."""

    def __init__(self, db: Session, epsilon: float = 0.1) -> None:
        self.db = db
        self.epsilon = epsilon

    def select(self, arms: Sequence[Arm]) -> Arm:
        """Select an arm using epsilon-greedy."""

        if not arms:
            raise ValueError("No arms provided")
        if random.random() < self.epsilon:
            choice = random.choice(list(arms))
            append_log("bandit_explore", path="bandit", detail=choice.key)
            return choice
        best_arm = None
        best_score = -math.inf
        for arm in arms:
            policy = self._get_policy(arm.key)
            score = (policy.successes + 1) / (policy.trials + 2)
            if score > best_score:
                best_score = score
                best_arm = arm
        append_log("bandit_exploit", path="bandit", detail=best_arm.key if best_arm else "")
        return best_arm or arms[0]

    def record(self, key: str, success: bool) -> None:
        """Update policy stats for the given arm."""

        policy = self._get_policy(key)
        policy.trials += 1
        if success:
            policy.successes += 1
        self.db.add(policy)
        self.db.commit()

    def _get_policy(self, key: str) -> Policy:
        policy = self.db.query(Policy).filter(Policy.key == key).first()
        if not policy:
            policy = Policy(key=key, successes=0, trials=0)
        return policy


def select_model(db: Session, options: Iterable[str]) -> str:
    """Public helper to select a model name with epsilon-greedy."""

    arms = [Arm(key=f"model::{name}", payload={"model": name}) for name in options]
    bandit = EpsilonGreedyBandit(db)
    arm = bandit.select(arms)
    return arm.payload["model"]
