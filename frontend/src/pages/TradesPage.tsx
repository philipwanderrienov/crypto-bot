import { useEffect, useState } from "react";
import { api } from "../api";
import type { TradeResponse } from "../types";

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

export function TradesPage() {
  const [trades, setTrades] = useState<TradeResponse[]>([]);

  useEffect(() => {
    let active = true;

    api.trades().then((data) => {
      if (active) setTrades(data);
    });

    return () => {
      active = false;
    };
  }, []);

  return (
    <section className="simple-page">
      <h1>Trades</h1>
      {trades.length > 0 ? (
        <ul>
          {trades.map((trade) => (
            <li key={trade.trade_id}>
              {trade.symbol} {trade.side} {trade.quantity} @ {formatCurrency(trade.price)} — fee{" "}
              {formatCurrency(trade.fee)} — {formatDate(trade.executed_at)}
            </li>
          ))}
        </ul>
      ) : (
        <p>No trades returned by the backend.</p>
      )}
    </section>
  );
}