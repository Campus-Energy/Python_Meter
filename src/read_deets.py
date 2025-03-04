from pathlib import Path
import pandas as pd
def readMeterDeets():
    base_dir = Path(__file__).resolve().parent  # This ensures we are referencing the correct directory
    deet = pd.read_csv(base_dir / "config/Meter Deets.csv")
    print(deet)


readMeterDeets()