import { useEffect, useState } from "react";
import { api } from "../api";
import type { SettingsResponse } from "../types";

export function SettingsPage() {
  const [settings, setSettings] = useState<SettingsResponse | null>(null);

  useEffect(() => {
    let active = true;

    api.settings().then((data) => {
      if (active) setSettings(data);
    });

    return () => {
      active = false;
    };
  }, []);

  return (
    <section className="simple-page">
      <h1>Settings</h1>
      {settings ? (
        <ul>
          <li>App: {settings.app_name}</li>
          <li>Environment: {settings.app_env}</li>
          <li>Log level: {settings.log_level}</li>
          <li>Default symbol: {settings.default_symbol}</li>
          <li>Default timeframe: {settings.default_timeframe}</li>
          <li>Bybit testnet: {settings.bybit_testnet ? "Yes" : "No"}</li>
          <li>Bybit base URL: {settings.bybit_base_url}</li>
          <li>API credentials: {settings.has_api_credentials ? "Configured" : "Missing"}</li>
        </ul>
      ) : (
        <p>Loading settings...</p>
      )}
    </section>
  );
}