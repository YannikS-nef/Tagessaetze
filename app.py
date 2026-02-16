from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any

from flask import Flask, g, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "data" / "customers.db"

app = Flask(__name__)

from calc import calculate_rate_plan


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        DATABASE.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_: Any) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            daily_rate REAL NOT NULL,
            revenue REAL NOT NULL DEFAULT 0,
            customer_type TEXT NOT NULL CHECK(customer_type IN ('Hauptkunde', 'Nebenkunde'))
        )
        """
    )
    db.commit()


def classify_rate(rate: float, all_rates: list[float]) -> tuple[str, str]:
    if not all_rates:
        return "secondary", "Keine Vergleichsdaten"

    low = min(all_rates)
    high = max(all_rates)
    if high == low:
        return "success", "Stabil"

    lower_third = low + (high - low) / 3
    upper_third = low + 2 * (high - low) / 3

    if rate < lower_third:
        return "danger", "Anpassung prüfen"
    if rate < upper_third:
        return "warning", "Beobachten"
    return "success", "Gut positioniert"


@app.route("/", methods=["GET"])
def index() -> str:
    init_db()
    db = get_db()
    customers = db.execute("SELECT * FROM customers ORDER BY daily_rate DESC, name ASC").fetchall()
    rates = [row["daily_rate"] for row in customers]

    processed_customers = []
    for row in customers:
        color, label = classify_rate(row["daily_rate"], rates)
        processed_customers.append(
            {
                "id": row["id"],
                "name": row["name"],
                "daily_rate": row["daily_rate"],
                "revenue": row["revenue"],
                "customer_type": row["customer_type"],
                "ampel_color": color,
                "ampel_label": label,
            }
        )

    totals = {
        "customers": len(customers),
        "revenue": sum(row["revenue"] for row in customers),
        "avg_rate": (sum(rates) / len(rates)) if rates else 0,
    }

    optimizer_result = None
    if request.args.get("optimize"):
        optimizer_result = calculate_rate_plan(
            gross_target=float(request.args.get("gross_target", 0)),
            net_target=float(request.args.get("net_target", 0)),
            tax_and_cost_factor=float(request.args.get("tax_and_cost_factor", 35)),
            vacation_days=int(request.args.get("vacation_days", 30)),
            holidays=int(request.args.get("holidays", 10)),
            sick_days=int(request.args.get("sick_days", 5)),
            workdays_per_week=int(request.args.get("workdays_per_week", 5)),
            utilization_percent=float(request.args.get("utilization_percent", 75)),
            hours_per_day=float(request.args.get("hours_per_day", 8)),
        )

    return render_template(
        "index.html",
        customers=processed_customers,
        totals=totals,
        optimizer_result=optimizer_result,
    )


@app.route("/customers", methods=["POST"])
def create_customer() -> Any:
    init_db()
    name = request.form.get("name", "").strip()
    customer_type = request.form.get("customer_type", "Nebenkunde")

    if not name:
        return redirect(url_for("index"))

    daily_rate = float(request.form.get("daily_rate", 0) or 0)
    revenue = float(request.form.get("revenue", 0) or 0)

    db = get_db()
    db.execute(
        "INSERT INTO customers (name, daily_rate, revenue, customer_type) VALUES (?, ?, ?, ?)",
        (name, daily_rate, revenue, customer_type),
    )
    db.commit()
    return redirect(url_for("index"))


@app.route("/customers/<int:customer_id>/delete", methods=["POST"])
def delete_customer(customer_id: int) -> Any:
    init_db()
    db = get_db()
    db.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    db.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=False)
