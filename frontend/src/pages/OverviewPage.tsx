import { useEffect, useMemo, useState } from "react";
import { getAnalysis, getNews } from "../api";
import type { AnalysisResponse, NewsItem, NewsResponse } from "../types";

function formatPercent(value: number) {
  return `${Math.round(value * 100)}%`;
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function signalTone(signal: AnalysisResponse["signal"]) {
  switch (signal) {
    case "bullish":
      return "pill pill--positive";
    case "bearish":
      return "pill pill--negative";
    case "cautious":
      return "pill pill--warning";
    default:
      return "pill pill--neutral";
  }
}

function importanceTone(importance: NewsItem["importance"]) {
  switch (importance) {
    case "high":
      return "pill pill--negative";
    case "medium":
      return "pill pill--warning";
    default:
      return "pill pill--neutral";
  }
}

const fallbackAnalysis: AnalysisResponse = {
  signal: "neutral",
  reason: "Analysis is loading.",
  confidence: 0,
  key_factors: [],
  updated_at: new Date().toISOString(),
};

const fallbackNews: NewsResponse = {
  items: [],
  updated_at: new Date().toISOString(),
};

export function OverviewPage() {
  const [analysis, setAnalysis] = useState<AnalysisResponse>(fallbackAnalysis);
  const [news, setNews] = useState<NewsResponse>(fallbackNews);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    Promise.all([getAnalysis(), getNews()])
      .then(([analysisData, newsData]) => {
        if (!active) return;
        setAnalysis(analysisData);
        setNews(newsData);
        setError(null);
      })
      .catch((err: unknown) => {
        if (!active) return;
        setError(err instanceof Error ? err.message : "Unable to load analysis and news.");
        setAnalysis(fallbackAnalysis);
        setNews(fallbackNews);
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, []);

  const sortedNews = useMemo(
    () => [...news.items].sort((a, b) => new Date(b.published_at).getTime() - new Date(a.published_at).getTime()),
    [news.items],
  );

  return (
    <div className="dashboard dashboard--analysis">
      <header className="topbar">
        <div className="topbar__inner">
          <div className="topbar__brand">
            <div className="topbar__avatar" aria-hidden="true">
              <span className="material-symbols-outlined">insights</span>
            </div>
            <div>
              <div className="topbar__eyebrow">Analysis-first dashboard</div>
              <div className="topbar__title">Signal + News</div>
            </div>
          </div>
        </div>
      </header>

      {error ? (
        <section className="content-panel content-panel--notice">
          <h2 className="section-title">Unable to refresh backend data</h2>
          <p>{error}</p>
        </section>
      ) : null}

      <section className="hero-grid">
        <article className="hero-card">
          <div className="hero-card__content">
            <div>
              <span className="section-kicker">Current signal</span>
              <h1 className="hero-card__value">{loading ? "Loading…" : analysis.signal}</h1>
              <div className="hero-card__meta">
                <span className={signalTone(analysis.signal)}>{analysis.signal}</span>
                <span className="hero-card__delta">Confidence {formatPercent(analysis.confidence)}</span>
              </div>
            </div>
          </div>
        </article>

        <div className="stats-grid">
          <article className="stat-card">
            <span className="stat-card__icon tone-primary">
              <span className="material-symbols-outlined">psychology</span>
            </span>
            <div className="stat-card__label">Reason</div>
            <div className="stat-card__value tone-primary">{loading ? "Loading…" : analysis.reason}</div>
          </article>

          <article className="stat-card">
            <span className="stat-card__icon tone-tertiary">
              <span className="material-symbols-outlined">award_star</span>
            </span>
            <div className="stat-card__label">Updated</div>
            <div className="stat-card__value tone-tertiary">{formatDate(analysis.updated_at)}</div>
          </article>
        </div>
      </section>

      <div className="dashboard-grid">
        <section className="content-panel">
          <div className="section-header">
            <h2 className="section-title">Key factors</h2>
            <span className="live-pill">Backend</span>
          </div>

          {analysis.key_factors.length > 0 ? (
            <ul className="factor-list">
              {analysis.key_factors.map((factor) => (
                <li key={factor} className="factor-list__item">
                  {factor}
                </li>
              ))}
            </ul>
          ) : loading ? (
            <p>Loading factors…</p>
          ) : (
            <p>No key factors returned by the backend.</p>
          )}
        </section>

        <aside className="sidebar-panel">
          <div className="section-header">
            <h2 className="section-title">News feed</h2>
            <span className="live-pill">{news.items.length} items</span>
          </div>

          {sortedNews.length > 0 ? (
            <div className="activity-list">
              {sortedNews.map((item) => (
                <article key={item.id} className="news-card">
                  <div className="news-card__header">
                    <strong>{item.headline}</strong>
                    <span className={importanceTone(item.importance)}>{item.importance}</span>
                  </div>
                  <p className="news-card__summary">{item.summary}</p>
                  <div className="news-card__meta">
                    <span>{item.source}</span>
                    <span>{formatDate(item.published_at)}</span>
                  </div>
                  {item.tags.length > 0 ? (
                    <div className="news-card__tags">
                      {item.tags.map((tag) => (
                        <span key={tag} className="pill pill--neutral">
                          {tag}
                        </span>
                      ))}
                    </div>
                  ) : null}
                </article>
              ))}
            </div>
          ) : loading ? (
            <p>Loading news…</p>
          ) : (
            <p>No relevant news returned by the backend.</p>
          )}
        </aside>
      </div>
    </div>
  );
}
