from agents import function_tool
from datetime import date, timedelta

from database import (
    add_subscription as db_add_subscription,
    get_monthly_total as db_get_monthly_total,
    get_all_subscriptions as db_get_all_subscriptions,
    set_budget as db_set_budget,
    get_budget as db_get_budget,
)


@function_tool
def add_subscription(
    name: str,
    cost: float,
    renewal_date: str | None = None,
) -> str:
    """
    Add a new active subscription.

    Args:
        name: Name of the subscription.
        cost: Monthly cost in rupees.
        renewal_date: Renewal date in YYYY-MM-DD format, if known.

    Returns:
        Confirmation that the subscription was added.
    """

    db_add_subscription(name, cost, renewal_date)

    if renewal_date:
        return (
            f"Subscription '{name}' was added successfully. "
            f"Monthly cost: ₹{cost:.2f}. "
            f"Renewal date: {renewal_date}."
        )

    return (
        f"Subscription '{name}' was added successfully. "
        f"Monthly cost: ₹{cost:.2f}."
    )


@function_tool
def get_monthly_total(request: str) -> str:
    """
    Get the total monthly cost of all active subscriptions.

    Args:
        request: A short description of why the monthly total is needed.

    Returns:
        Current monthly subscription cost.
    """

    total = db_get_monthly_total()

    return f"Current monthly subscription cost: ₹{total:.2f}"


@function_tool
def get_subscriptions(request: str) -> str:
    """
    Get all active subscriptions.

    Args:
        request: A short description of why the subscription list is needed.

    Returns:
        A list of active subscriptions.
    """

    subscriptions = db_get_all_subscriptions()

    if not subscriptions:
        return "There are currently no active subscriptions."

    lines = []

    for subscription in subscriptions:
        line = (
            f"{subscription['name']}: "
            f"₹{subscription['cost']:.2f}/month"
        )

        if subscription["renewal_date"]:
            line += (
                f", renewal date: "
                f"{subscription['renewal_date']}"
            )

        lines.append(line)

    return "\n".join(lines)


@function_tool
def set_monthly_budget(budget: float) -> str:
    """
    Set the user's monthly subscription budget.

    Args:
        budget: Maximum amount the user wants to spend per month in rupees.

    Returns:
        Confirmation of the saved budget.
    """

    if budget <= 0:
        return "Budget must be greater than zero."

    db_set_budget(budget)

    return f"Monthly subscription budget set to ₹{budget:.2f}."


@function_tool
def get_monthly_budget(request: str) -> str:
    """
    Get the user's current monthly subscription budget.

    Args:
        request: A short description of why the budget is needed.

    Returns:
        The current monthly budget.
    """

    budget = db_get_budget()

    if budget is None:
        return "No monthly subscription budget has been set."

    return f"Current monthly subscription budget: ₹{budget:.2f}"



@function_tool
def get_yearly_cost(request: str) -> str:
    """
    Calculate the estimated yearly cost of all active subscriptions.

    Args:
        request: A short description of why the yearly cost is needed.

    Returns:
        Estimated yearly subscription cost.
    """

    monthly_total = db_get_monthly_total()
    yearly_total = monthly_total * 12

    return (
        f"Current monthly cost: ₹{monthly_total:.2f}. "
        f"Estimated yearly cost: ₹{yearly_total:.2f}."
    )


@function_tool
def get_upcoming_renewals(days_ahead: int = 30) -> str:
    """
    Find active subscriptions renewing within the specified number of days.

    Args:
        days_ahead: Number of days into the future to check.

    Returns:
        List of upcoming subscription renewals.
    """

    if days_ahead <= 0:
        return "days_ahead must be greater than zero."

    subscriptions = db_get_all_subscriptions()

    today = date.today()
    end_date = today + timedelta(days=days_ahead)

    upcoming = []

    for subscription in subscriptions:
        renewal_date = subscription["renewal_date"]

        if not renewal_date:
            continue

        try:
            renewal = date.fromisoformat(renewal_date)
        except ValueError:
            continue

        if today <= renewal <= end_date:
            upcoming.append(
                (
                    renewal,
                    subscription["name"],
                    subscription["cost"],
                )
            )

    if not upcoming:
        return (
            f"No subscriptions are renewing "
            f"within the next {days_ahead} days."
        )

    upcoming.sort()

    lines = []

    for renewal, name, cost in upcoming:
        lines.append(
            f"{name} - ₹{cost:.2f} - "
            f"renews on {renewal.isoformat()}"
        )

    return "\n".join(lines)