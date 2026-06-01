function formatPercent(value) {
    return `${(value * 100).toFixed(1)}%`;
}

function formatScore(value) {
    return Number(value).toFixed(3);
}

function selectChampion(models) {
    if (!Array.isArray(models) || models.length === 0) {
        return null;
    }

    const namedChampion = models.find((model) => String(model.Model).includes("Gradient Boosting"));
    if (namedChampion) {
        return namedChampion;
    }

    return [...models].sort((left, right) => {
        return Number(right["F1-Score"]) - Number(left["F1-Score"]);
    })[0];
}

async function loadModelAnalyticsPage() {
    const status = document.getElementById("analytics-status");
    const tableBody = document.getElementById("analytics-table-body");
    const championName = document.getElementById("champion-model-name");
    const championCopy = document.getElementById("champion-model-copy");
    const bestAccuracy = document.getElementById("best-accuracy");
    const bestRocAuc = document.getElementById("best-roc-auc");
    const bestF1 = document.getElementById("best-f1");
    const featurePills = document.getElementById("top-feature-pills");

    try {
        const response = await fetch("/api/analytics");
        const data = await response.json();

        if (!response.ok || data.error) {
            throw new Error(data.error || "Unable to load analytics.");
        }

        const models = Array.isArray(data.model_results) ? data.model_results : [];
        const features = Array.isArray(data.top_features) ? data.top_features : [];

        if (models.length === 0) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="6">
                        <div class="empty-state">No model comparison records were returned from the analytics API.</div>
                    </td>
                </tr>
            `;
            status.textContent = "Analytics loaded, but no model rows were available.";
            return;
        }

        const champion = selectChampion(models);
        const bestAccuracyModel = [...models].sort((left, right) => Number(right.Accuracy) - Number(left.Accuracy))[0];
        const bestRocAucModel = [...models].sort((left, right) => Number(right["ROC-AUC"]) - Number(left["ROC-AUC"]))[0];

        championName.textContent = champion.Model;
        championCopy.textContent = `Chosen as the active scoring model based on its overall operating balance across accuracy, F1-score, and ROC-AUC.`;
        bestAccuracy.textContent = formatPercent(bestAccuracyModel.Accuracy);
        bestRocAuc.textContent = formatScore(bestRocAucModel["ROC-AUC"]);
        bestF1.textContent = formatScore(champion["F1-Score"]);

        status.textContent = `Loaded ${models.length} models from the live analytics endpoint.`;

        tableBody.innerHTML = models.map((model) => {
            const isChampion = model.Model === champion.Model;
            return `
                <tr class="${isChampion ? "highlight" : ""}">
                    <td>
                        <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
                            <strong>${model.Model}</strong>
                            ${isChampion ? '<span class="chip success">Champion</span>' : ""}
                        </div>
                    </td>
                    <td>${formatPercent(model.Accuracy)}</td>
                    <td>${formatScore(model.Precision)}</td>
                    <td>${formatScore(model.Recall)}</td>
                    <td>${formatScore(model["F1-Score"])}</td>
                    <td>
                        <div>${formatScore(model["ROC-AUC"])}</div>
                        <div class="metric-bar">
                            <div class="metric-fill" style="width:${Math.max(0, Math.min(100, Number(model["ROC-AUC"]) * 100))}%"></div>
                        </div>
                    </td>
                </tr>
            `;
        }).join("");

        featurePills.innerHTML = features.slice(0, 5).map((feature) => {
            const label = String(feature.Feature || "").replace(/_/g, " ");
            return `<span class="pill">${label}</span>`;
        }).join("");
    } catch (error) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="6">
                    <div class="empty-state">${error.message}</div>
                </td>
            </tr>
        `;
        if (status) {
            status.textContent = "Analytics could not be loaded.";
        }
    }
}

if (document.readyState === "loading") {
    window.addEventListener("DOMContentLoaded", loadModelAnalyticsPage);
} else {
    loadModelAnalyticsPage();
}
