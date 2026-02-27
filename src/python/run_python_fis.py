import os
import sys

# Allow importing from repo root
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

from src.python.fis_model import simulate_observations


def main():
    out_dir = os.path.join(REPO_ROOT, "results")
    os.makedirs(out_dir, exist_ok=True)

    # ✅ Paste your FULL observation lists here (I put a short example)
    nitrogen_observation = [6, 11.8, 10.9]
    pH_observation = [7.6, 6.8, 7.7]
    NDRE_observation = [0.639306, 0.535043, 0.541024]
    yield_observation = [8.762764, 4.946119, 6.485314]  # optional

    df = simulate_observations(
        nitrogen_observation,
        pH_observation,
        NDRE_observation,
        yield_obs=yield_observation
    )

    out_file = os.path.join(out_dir, "productivity_clusters.xlsx")
    df.to_excel(out_file, index=False)
    print(f"Saved: {out_file}")


if __name__ == "__main__":
    main()
