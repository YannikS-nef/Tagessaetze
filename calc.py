from dataclasses import dataclass


@dataclass
class RatePlanResult:
    required_annual_revenue: float
    billable_days: float
    required_daily_rate: float
    required_hourly_rate: float


def calculate_rate_plan(
    gross_target: float,
    net_target: float,
    tax_and_cost_factor: float,
    vacation_days: int,
    holidays: int,
    sick_days: int,
    workdays_per_week: int,
    utilization_percent: float,
    hours_per_day: float,
) -> RatePlanResult:
    target = max(gross_target, 0.0)
    if net_target > 0:
        target = max(target, net_target / max(0.01, 1 - tax_and_cost_factor / 100))

    yearly_workdays = workdays_per_week * 52
    available_days = max(0, yearly_workdays - vacation_days - holidays - sick_days)
    billable_days = available_days * max(0.01, utilization_percent / 100)
    required_daily_rate = target / billable_days if billable_days else 0.0
    required_hourly_rate = required_daily_rate / max(1, hours_per_day)

    return RatePlanResult(
        required_annual_revenue=target,
        billable_days=billable_days,
        required_daily_rate=required_daily_rate,
        required_hourly_rate=required_hourly_rate,
    )
