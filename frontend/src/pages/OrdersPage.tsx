import { useEffect, useState } from "react";
import { api } from "../api";
import type { OrderResponse } from "../types";

function formatCurrency(value: number | null) {
  if (value == null) return "—";
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

export function OrdersPage() {
  const [orders, setOrders] = useState<OrderResponse[]>([]);

  useEffect(() => {
    let active = true;

    api.orders().then((data) => {
      if (active) setOrders(data);
    });

    return () => {
      active = false;
    };
  }, []);

  return (
    <section className="simple-page">
      <h1>Orders</h1>
      {orders.length > 0 ? (
        <ul>
          {orders.map((order) => (
            <li key={order.order_id}>
              {order.symbol} {order.side} {order.quantity} @ {formatCurrency(order.price)} ({order.status}) —{" "}
              {formatDate(order.created_at)}
            </li>
          ))}
        </ul>
      ) : (
        <p>No orders returned by the backend.</p>
      )}
    </section>
  );
}