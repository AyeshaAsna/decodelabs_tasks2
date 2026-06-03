from pathlib import Path

import numpy as np
import pandas as pd

# --------------------------------------------------------
# PROJECT-2: Dataset Analysis (Single Script)
# Goal: Understand patterns, trends, and distributions
# --------------------------------------------------------

INPUT_FILE = Path(r"C:\Users\Ayesha Asna\Downloads\Dataset for Data Analytics (1).xlsx")
OUTPUT_DIR = Path(r"D:\DECODESLAB INTERNSHIP\PROJECT-2")
OUTPUT_REPORT = OUTPUT_DIR / "project2_analysis_report.txt"
OUTPUT_STATS_CSV = OUTPUT_DIR / "project2_numeric_statistics.csv"
OUTPUT_OUTLIERS_CSV = OUTPUT_DIR / "project2_outlier_summary.csv"


def print_section(title):
    print("\n" + "=" * 75)
    print(title)
    print("=" * 75)


def detect_date_columns(dataframe):
    date_cols = []
    for col in dataframe.columns:
        col_lower = col.lower()
        if "date" in col_lower or "time" in col_lower:
            parsed = pd.to_datetime(dataframe[col], errors="coerce")
            if parsed.notna().sum() > 0:
                dataframe[col] = parsed
                date_cols.append(col)
    return date_cols


def main():
    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        print_section("PROJECT-2 DATA ANALYSIS STARTED")
        print(f"Input file: {INPUT_FILE}")

        # Load dataset
        df = pd.read_excel(INPUT_FILE)
        df.columns = [str(c).strip() for c in df.columns]
        print(f"\nDataset loaded successfully: {df.shape[0]} rows x {df.shape[1]} columns")

        # Missing values overview
        print_section("MISSING VALUES CHECK")
        missing_counts = df.isna().sum()
        total_missing = int(missing_counts.sum())
        print(f"Total missing values: {total_missing}")
        if total_missing > 0:
            print("Missing values by column:")
            print(missing_counts[missing_counts > 0].to_string())
        else:
            print("No missing values found.")

        # Identify date columns first
        date_cols = detect_date_columns(df)

        # Identify numeric columns and ensure conversion where possible
        print_section("NUMERIC COLUMN PREPARATION")
        numeric_cols = []
        for col in df.columns:
            if col in date_cols or pd.api.types.is_datetime64_any_dtype(df[col]):
                continue
            if pd.api.types.is_numeric_dtype(df[col]):
                numeric_cols.append(col)
            else:
                candidate = pd.to_numeric(df[col], errors="coerce")
                if candidate.notna().mean() >= 0.90:
                    df[col] = candidate
                    numeric_cols.append(col)

        print(f"Numeric columns detected: {numeric_cols if numeric_cols else 'None'}")

        # Basic statistics: mean, median, count (+ helpful distribution stats)
        print_section("BASIC STATISTICS (MEAN, MEDIAN, COUNT)")
        stats_rows = []
        if numeric_cols:
            for col in numeric_cols:
                series = pd.to_numeric(df[col], errors="coerce")
                stat = {
                    "column": col,
                    "count": int(series.count()),
                    "mean": float(series.mean()) if series.count() > 0 else np.nan,
                    "median": float(series.median()) if series.count() > 0 else np.nan,
                    "std": float(series.std()) if series.count() > 1 else np.nan,
                    "min": float(series.min()) if series.count() > 0 else np.nan,
                    "max": float(series.max()) if series.count() > 0 else np.nan,
                }
                stats_rows.append(stat)

            stats_df = pd.DataFrame(stats_rows)
            print(stats_df.to_string(index=False))
            stats_df.to_csv(OUTPUT_STATS_CSV, index=False, encoding="utf-8")
            print(f"\nSaved numeric statistics to: {OUTPUT_STATS_CSV}")
        else:
            stats_df = pd.DataFrame(columns=["column", "count", "mean", "median", "std", "min", "max"])
            print("No numeric columns found for statistics.")

        # Outlier analysis using IQR rule
        print_section("OUTLIER ANALYSIS (IQR METHOD)")
        outlier_rows = []
        for col in numeric_cols:
            series = pd.to_numeric(df[col], errors="coerce").dropna()
            if len(series) < 4:
                outlier_rows.append({"column": col, "outlier_count": 0, "outlier_percent": 0.0})
                continue
            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outlier_mask = (series < lower_bound) | (series > upper_bound)
            outlier_count = int(outlier_mask.sum())
            outlier_percent = round((outlier_count / len(series)) * 100, 2)
            outlier_rows.append(
                {
                    "column": col,
                    "outlier_count": outlier_count,
                    "outlier_percent": outlier_percent,
                }
            )

        outlier_df = pd.DataFrame(outlier_rows)
        if not outlier_df.empty:
            print(outlier_df.to_string(index=False))
            outlier_df.to_csv(OUTPUT_OUTLIERS_CSV, index=False, encoding="utf-8")
            print(f"\nSaved outlier summary to: {OUTPUT_OUTLIERS_CSV}")
        else:
            print("No numeric columns available for outlier analysis.")

        # Trend analysis
        print_section("TREND ANALYSIS")
        trend_lines = []
        if date_cols and numeric_cols:
            date_col = date_cols[0]
            metric_col = numeric_cols[0]
            trend_df = df[[date_col, metric_col]].dropna().copy()
            if not trend_df.empty:
                trend_df["YearMonth"] = trend_df[date_col].dt.to_period("M").astype(str)
                monthly_trend = trend_df.groupby("YearMonth")[metric_col].mean().round(2)
                print(f"Monthly trend using Date: {date_col} and Metric: {metric_col}")
                print(monthly_trend.to_string())

                if len(monthly_trend) >= 2:
                    first_val = monthly_trend.iloc[0]
                    last_val = monthly_trend.iloc[-1]
                    if last_val > first_val:
                        trend_lines.append(f"{metric_col} shows an overall increasing monthly trend.")
                    elif last_val < first_val:
                        trend_lines.append(f"{metric_col} shows an overall decreasing monthly trend.")
                    else:
                        trend_lines.append(f"{metric_col} remains mostly stable over months.")
            else:
                print("Not enough valid date and numeric values for monthly trend.")
        else:
            print("No suitable date + numeric columns found for time trend.")

        # Category distribution patterns
        cat_cols = [c for c in df.columns if df[c].dtype == "object"]
        if cat_cols:
            print("\nTop category distributions:")
            for col in cat_cols[:3]:
                print(f"\nColumn: {col}")
                print(df[col].value_counts(dropna=False).head(5).to_string())

        # Key observations summary
        print_section("KEY OBSERVATIONS SUMMARY")
        observations = []
        observations.append(f"Dataset size: {df.shape[0]} rows and {df.shape[1]} columns.")
        observations.append(f"Total missing values found: {total_missing}.")
        observations.append(f"Numeric columns analyzed: {len(numeric_cols)}.")

        if not outlier_df.empty:
            max_outlier_row = outlier_df.sort_values("outlier_percent", ascending=False).iloc[0]
            observations.append(
                f"Highest outlier concentration: {max_outlier_row['column']} ({max_outlier_row['outlier_percent']}%)."
            )

        observations.extend(trend_lines)

        if stats_df.shape[0] > 0:
            highest_mean_row = stats_df.sort_values("mean", ascending=False).iloc[0]
            observations.append(
                f"Highest average value appears in {highest_mean_row['column']} (mean={round(highest_mean_row['mean'], 2)})."
            )

        for idx, obs in enumerate(observations, start=1):
            print(f"{idx}. {obs}")

        # Save final report
        report_lines = []
        report_lines.append("PROJECT-2 DATA ANALYSIS REPORT")
        report_lines.append("-" * 50)
        report_lines.append(f"Input file: {INPUT_FILE}")
        report_lines.append(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
        report_lines.append(f"Total missing values: {total_missing}")
        report_lines.append(f"Numeric columns: {numeric_cols}")
        report_lines.append("")
        report_lines.append("KEY OBSERVATIONS:")
        for obs in observations:
            report_lines.append(f"- {obs}")
        report_lines.append("")
        report_lines.append(f"Saved stats CSV: {OUTPUT_STATS_CSV}")
        report_lines.append(f"Saved outlier CSV: {OUTPUT_OUTLIERS_CSV}")

        OUTPUT_REPORT.write_text("\n".join(report_lines), encoding="utf-8")

        print_section("FILES SAVED")
        print(f"Report file: {OUTPUT_REPORT}")
        print(f"Statistics file: {OUTPUT_STATS_CSV}")
        print(f"Outlier file: {OUTPUT_OUTLIERS_CSV}")

        print_section("PROJECT-2 DATA ANALYSIS COMPLETED")

    except FileNotFoundError:
        print(f"ERROR: File not found -> {INPUT_FILE}")
    except PermissionError:
        print("ERROR: Permission denied while reading/saving files.")
    except Exception as e:
        print(f"ERROR: Unexpected issue occurred -> {e}")


if __name__ == "__main__":
    main()

