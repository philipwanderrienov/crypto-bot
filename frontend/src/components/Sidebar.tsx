export type View = "overview";

type SidebarProps = {
  currentView: View;
  onSelectView: (view: View) => void;
};

const items: Array<{
  key: View;
  label: string;
  icon: string;
}> = [{ key: "overview", label: "Analysis", icon: "insights" }];

export function Sidebar({ currentView, onSelectView }: SidebarProps) {
  return (
    <aside className="sidebar" aria-label="Primary navigation">
      <div className="sidebar__brand">
        <div className="sidebar__avatar" aria-hidden="true">
          <span className="material-symbols-outlined">hub</span>
        </div>
        <div>
          <div className="sidebar__eyebrow">OB-01</div>
          <div className="sidebar__title">Kinetic Precision Terminal</div>
        </div>
      </div>

      <nav className="sidebar__nav">
        {items.map((item) => (
          <button
            key={item.key}
            type="button"
            className={`sidebar__item${currentView === item.key ? " sidebar__item--active" : ""}`}
            onClick={() => onSelectView(item.key)}
          >
            <span className="material-symbols-outlined sidebar__item-icon" aria-hidden="true">
              {item.icon}
            </span>
            <span>{item.label}</span>
          </button>
        ))}
      </nav>
    </aside>
  );
}