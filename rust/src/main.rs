//! AVA007 Agent Exoskeleton entry (from ava007-agent-exoskeleton-rust.zip).
//! Modules adapters/codebluff/exoskeleton/kernel were referenced but not in the zip — stub health only.

use axum::{routing::get, Json, Router};
use serde_json::json;
use tracing::info;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt()
        .with_env_filter("info")
        .init();

    let app = Router::new().route("/healthz", get(|| async {
        Json(json!({"ok": true, "service": "ava007-agent-exoskeleton", "note": "partial scaffold"}))
    }));

    let addr = "127.0.0.1:8770";
    info!("AVA007 Agent Exoskeleton listening on http://{addr}");
    let listener = tokio::net::TcpListener::bind(addr).await?;
    axum::serve(listener, app).await?;
    Ok(())
}
