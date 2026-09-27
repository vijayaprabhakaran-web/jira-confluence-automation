import argparse
import math


def format_points(value: float | None, missing_reason: str) -> str:
    if value is None:
        return f"Unavailable ({missing_reason})"
    return f"{value:g} points"


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Summarize sprint committed, completed, remaining, and unestimated work. "
            "Pass only values available from sprint data; omitted metrics are reported as unavailable."
        )
    )
    parser.add_argument("--committed-points", type=float, help="Story points committed at sprint start")
    parser.add_argument("--completed-points", type=float, help="Story points completed in the sprint")
    parser.add_argument(
        "--unestimated-issues",
        type=int,
        help="Number of in-scope issues with a missing estimate; explicitly pass 0 when there are none",
    )
    args = parser.parse_args()

    for name in ("committed_points", "completed_points"):
        value = getattr(args, name)
        if value is not None and (not math.isfinite(value) or value < 0):
            parser.error(f"{name.replace('_', '-')} must be a finite non-negative number")
    if args.unestimated_issues is not None and args.unestimated_issues < 0:
        parser.error("unestimated-issues must be a non-negative integer")

    if all(value is None for value in (args.committed_points, args.completed_points, args.unestimated_issues)):
        print("Sprint work data unavailable: provide at least one sprint metric.")
        return

    if args.committed_points is not None and args.completed_points is not None:
        remaining_points = max(args.committed_points - args.completed_points, 0)
        remaining_reason = ""
    else:
        remaining_points = None
        remaining_reason = "committed-points and completed-points are both required"

    print(f"Committed work: {format_points(args.committed_points, 'committed-points not provided')}")
    print(f"Completed work: {format_points(args.completed_points, 'completed-points not provided')}")
    print(f"Remaining committed work: {format_points(remaining_points, remaining_reason)}")
    if args.unestimated_issues is None:
        print("Unestimated work: Unavailable (unestimated-issues not provided)")
    else:
        label = "issue" if args.unestimated_issues == 1 else "issues"
        print(f"Unestimated work: {args.unestimated_issues} {label}")


if __name__ == "__main__":
    main()