---
name: Calculate Compound Interest
description: "Use the compound interest CLI to calculate a final balance and interest earned from user-provided inputs."
user-invocable: true
---
- Use this instruction when the user asks to calculate compound interest and provides or requests calculation inputs.
- Require principal, nominal annual interest rate, compounding periods per year, and duration in years; ask for any missing value instead of guessing.
- Treat the annual rate as a percentage, not a decimal: enter `7.34` for 7.34%.
- Convert durations with months to fractional years before invoking the tool; for example, 8 years and 7 months is `8.5833333333` years.
- Invoke the script from the project root with positional arguments in this order: principal, annual rate percentage, compounds per year, total years.
  + Example: `python tools/compound_interest.py 15847 7.34 12 8.5833333333`
- Run the command in the terminal and use its output; do not manually recompute or alter the reported values.
- Present both output fields clearly: `Final amount` and `Interest earned`, preserving the script's currency symbol and two-decimal rounding.
- If the command rejects an input or fails, explain the error and ask the user to correct the relevant value; do not present a guessed result.