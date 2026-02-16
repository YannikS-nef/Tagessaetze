from calc import calculate_rate_plan


def test_calculate_rate_plan_has_positive_rates():
    result = calculate_rate_plan(
        gross_target=120000,
        net_target=0,
        tax_and_cost_factor=35,
        vacation_days=30,
        holidays=10,
        sick_days=5,
        workdays_per_week=5,
        utilization_percent=75,
        hours_per_day=8,
    )

    assert result.required_annual_revenue == 120000
    assert result.billable_days > 0
    assert result.required_daily_rate > 0
    assert result.required_hourly_rate > 0
