import { useState } from "react";
import { Sidebar, type View } from "./components/Sidebar";
import { OverviewPage } from "./pages/OverviewPage";

const views: View[] = ["overview"];

export default function App() {
  const [view, setView] = useState<View>("overview");

  return (
    <div className="app-shell">
      <Sidebar currentView={view} onSelectView={setView} />
      <main className="app-content">
        <OverviewPage />
      </main>

      <nav className="mobile-nav" aria-label="Primary mobile navigation">
        {views.map((item) => (
          <button
            key={item}
            type="button"
            className={`mobile-nav__item${view === item ? " mobile-nav__item--active" : ""}`}
            onClick={() => setView(item)}
          >
            <span className="mobile-nav__icon" aria-hidden="true">
              {item === "overview" && "insights"}
            </span>
            <span className="mobile-nav__label">
              {item.charAt(0).toUpperCase() + item.slice(1)}
            </span>
          </button>
        ))}
      </nav>
    </div>
  );
}