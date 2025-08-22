# evaluation/evaluate.py
import json, os, datetime, time
from pathlib import Path
from typing import Dict, List
import pandas as pd
from tqdm import tqdm
from strategies import ALL_STRATEGIES
from judge_prompt import judge

DATA_PATH = Path(__file__).parent / "dataset.json"
OUT_DIR = Path(__file__).parent / "results"

def load_dataset() -> List[Dict]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def run():
    ds = load_dataset()
    strategies = list(ALL_STRATEGIES.keys())  # run all
    rows = []

    for item in tqdm(ds, desc="Evaluating samples"):
        meta = {k: item.get(k) for k in ["id","game","category","question","expected","level","mode","inventory"]}
        for strat in strategies:
            fn = ALL_STRATEGIES[strat]
            ai_answer = fn(**item)

            j = judge(item["expected"], ai_answer, item["game"], item["category"], item["question"])

            rows.append({
                "id": meta["id"],
                "strategy": strat,
                "game": meta["game"],
                "category": meta["category"],
                "question": meta["question"],
                "ai_answer": ai_answer,
                "expected": item["expected"],
                **{k: j.get(k) for k in ["relevance","accuracy","completeness","clarity","total_score","feedback"]}
            })
            
            time.sleep(5) 

    df = pd.DataFrame(rows)

    summary = (
        df.groupby("strategy")["total_score"]
          .agg(["count","mean","std"])
          .sort_values("mean", ascending=False)
          .reset_index()
    )

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_json(OUT_DIR / f"run_{ts}.json", orient="records", force_ascii=False, indent=2)
    df.to_csv(OUT_DIR / f"run_{ts}.csv", index=False)
    summary.to_csv(OUT_DIR / f"summary_{ts}.csv", index=False)

    print("\n=== Per-strategy summary (out of 20) ===")
    print(summary.to_string(index=False))

if __name__ == "__main__":
    run()
