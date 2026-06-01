import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pandas as pd
import joblib
from pathlib import Path

app = FastAPI(title="Automotive Lead Conversion API")

# Resolve all project files relative to this app module.
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"
MODEL_PATH = BASE_DIR / "champion_model.pkl"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def page_response(file_name: str) -> FileResponse:
    return FileResponse(BASE_DIR / file_name)


def detail_page_response(
    request: Request,
    template_name: str,
    page_title: str,
    active_page: str,
    current_page_label: str,
    current_page_href: str,
):
    return templates.TemplateResponse(
        request,
        template_name,
        {
            "page_title": page_title,
            "active_page": active_page,
            "current_page_label": current_page_label,
            "current_page_href": current_page_href,
        },
    )


# Load model
model = None
if MODEL_PATH.exists():
    model = joblib.load(MODEL_PATH)

class LeadFeatures(BaseModel):
    vehicle_segment: str = "Compact SUV / Crossover"
    model_year_position: str = "Current Model Year"
    powertrain_focus: str = "ICE"
    primary_channel: str = "Paid Social"
    secondary_channel_syndicated_flag: str = "No"
    shopper_intent_decile: int = 6
    market_region_tier: str = "US – Major Metro"
    nameplate_lifecycle_stage: str = "Steady State"
    incentive_program_pressure_band: str = "Moderate APR / Cash"
    competitive_conquest_intensity_band: str = "Moderate"
    days_supply_inventory_proxy_band: str = "Balanced"
    auto_loan_rate_environment_band: str = "Adverse – Rising APR"
    personalization_depth_band: str = "Segmented"
    dealer_cosponsored_local_campaign_flag: str = "No"
    days_since_last_brand_engagement: int = 37
    major_auto_show_or_event_window_flag: str = "No"
    ev_adoption_maturity_region_band: str = "Growing"
    ad_frequency_saturation_risk_band: str = "Typical"
    certified_preowned_vs_new_intent_context: str = "New Vehicle Focus"
    credit_availability_consumer_stress_band: str = "Benign"
    multicultural_locale_creative_match_flag: str = "No"
    recent_engagement_flag: str = "0"
    high_intent_flag: str = "0"
    intent_engagement_score: float = 50.0
    activity_month_num: int = 6

@app.get("/")
async def read_index():
    return page_response("index.html")


@app.get("/features")
async def read_features_page(request: Request):
    return detail_page_response(
        request,
        "pages/features.html",
        "Lead Features",
        "features",
        "Features",
        "/features",
    )


@app.get("/insights")
async def read_insights_page(request: Request):
    return detail_page_response(
        request,
        "pages/insights.html",
        "Lead Insights",
        "insights",
        "Insights",
        "/insights",
    )


@app.get("/model-analytics")
async def read_model_analytics_page(request: Request):
    return detail_page_response(
        request,
        "pages/model-analytics.html",
        "Model Analytics",
        "analytics",
        "Analytics",
        "/model-analytics",
    )


@app.get("/audience")
async def read_audience_page(request: Request):
    return detail_page_response(
        request,
        "pages/audience.html",
        "Audience Summary",
        "audience",
        "Audience",
        "/audience",
    )


@app.get("/conquest-targets")
async def read_conquest_targets_page(request: Request):
    return detail_page_response(
        request,
        "pages/conquest-targets.html",
        "Conquest Targets",
        "targets",
        "Targets",
        "/conquest-targets",
    )





@app.get("/guide")
async def read_guide_page(request: Request):
    return detail_page_response(
        request,
        "pages/guide.html",
        "User Guide",
        "guide",
        "Guide",
        "/guide",
    )

@app.post("/predict")
async def predict_conversion(lead: LeadFeatures):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Convert input data to DataFrame
        df = pd.DataFrame([lead.dict()])
        
        # Ensure correct column order
        expected_columns = [
            'vehicle_segment', 'model_year_position', 'powertrain_focus',
            'primary_channel', 'secondary_channel_syndicated_flag',
            'shopper_intent_decile', 'market_region_tier', 'nameplate_lifecycle_stage',
            'incentive_program_pressure_band', 'competitive_conquest_intensity_band',
            'days_supply_inventory_proxy_band', 'auto_loan_rate_environment_band',
            'personalization_depth_band', 'dealer_cosponsored_local_campaign_flag',
            'days_since_last_brand_engagement', 'major_auto_show_or_event_window_flag',
            'ev_adoption_maturity_region_band', 'ad_frequency_saturation_risk_band',
            'certified_preowned_vs_new_intent_context',
            'credit_availability_consumer_stress_band',
            'multicultural_locale_creative_match_flag', 'recent_engagement_flag',
            'high_intent_flag', 'intent_engagement_score', 'activity_month_num'
        ]
        
        df = df[expected_columns]
        
        # The ML model expects intent_engagement_score in the range 0.0-1.0,
        # but the UI sends it as a percentage (0-100).
        df['intent_engagement_score'] = df['intent_engagement_score'] / 100.0
        
        # Predict probability
        probability = model.predict_proba(df)[0][1]
        prediction = model.predict(df)[0]
        
        return {
            "prediction": int(prediction),
            "conversion_probability": float(probability)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/analytics")
async def get_analytics():
    try:
        results_df = pd.read_csv(BASE_DIR / "model_results.csv")
        feature_importance_df = pd.read_csv(BASE_DIR / "feature_importance.csv")
        
        # Parse CSVs
        results = results_df.to_dict('records')
        
        # For feature importance, assume columns Feature, Importance
        feature_importance_df.columns = ['Feature', 'Importance']
        features = feature_importance_df.sort_values(by='Importance', ascending=False).head(10).to_dict('records')
        
        return {
            "model_results": results,
            "top_features": features
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8002, reload=True)
