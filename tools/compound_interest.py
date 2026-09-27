import argparse
import math


def calculate_compound_interest(
    principal: float,
    annual_rate: float,
    compounds_per_year: int,
    total_years: float,
) -> tuple[float, float]:
    rate_per_period = annual_rate / 100 / compounds_per_year
    periods = compounds_per_year * total_years
    amount = principal * (1 + rate_per_period) ** periods
    return amount, amount - principal


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate compound interest. Enter the annual rate as a percentage, such as 7.34 for 7.34%."
    )
    parser.add_argument("principal", type=float, help="Initial principal amount")
    parser.add_argument("annual_rate", type=float, help="Nominal annual interest rate, as a percentage")
    parser.add_argument("compounds_per_year", type=int, help="Number of compounding periods per year")
    parser.add_argument("total_years", type=float, help="Investment duration in years")
    args = parser.parse_args()

    values = (args.principal, args.annual_rate, args.total_years)
    if not all(math.isfinite(value) for value in values):
        parser.error("principal, annual_rate, and total_years must be finite numbers")
    if args.principal < 0:
        parser.error("principal must be non-negative")
    if args.compounds_per_year <= 0:
        parser.error("compounds_per_year must be a positive integer")
    if args.total_years < 0:
        parser.error("total_years must be non-negative")
    if 1 + args.annual_rate / 100 / args.compounds_per_year < 0:
        parser.error("annual_rate must not produce a negative growth factor per period")

    amount, interest = calculate_compound_interest(
        args.principal,
        args.annual_rate,
        args.compounds_per_year,
        args.total_years,
    )
    print(f"Final amount: ${amount:,.2f}")
    print(f"Interest earned: ${interest:,.2f}")


if __name__ == "__main__":
    main()