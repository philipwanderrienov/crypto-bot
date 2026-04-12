import { useEffect, useState } from "react";
import { api } from "../api";
import type { PositionResponse } from "../types";

function formatCurrency(value: number) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: value >= 100 ? 0 : 2,
  }).format(value);
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

export function PositionsPage() {
  const [positions, setPositions] = useState<PositionResponse[]>([]);

  useEffect(() => {
    let active = true;

    api.positions().then((data) => {
      if (active) setPositions(data);
    });

    return () => {
      active = false;
    };
  }, []);

  return (
    <section className="simple-page">
      <h1>Positions</h1>
      {positions.length > 0 ? (
        <ul>
          {positions.map((position) => (
            <li key={`${position.symbol}-${position.side}`}>
              {position.symbol} {position.side} {position.size} @ {formatCurrency(position.entry_price)} — PnL{" "}
              {formatCurrency(position.unrealized_pnl)} (mark {formatCurrency(position.mark_price)}) — updated{" "}
              {formatDate(position.updated_at)}
            </li>
          ))}
        </ul>
      ) : (
        <p>No open positions returned by the backend.</p>
      )}
    </section>
  );
}