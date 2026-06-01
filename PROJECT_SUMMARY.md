# Project Summary

**Goal**: Convert a Jupyter Notebook ML analysis into a production-ready web application.

**Implementation**:
- **Backend**: Built with FastAPI. Provides high performance, auto-generating docs (Swagger), and robust data validation via Pydantic.
- **Frontend**: A single-page HTML interface utilizing Tailwind CSS for styling and Chart.js for data visualization. 
- **Model**: A Scikit-learn Gradient Boosting model saved via Joblib.

**Outcomes**:
- A functional REST API for predicting automotive sales lead conversions.
- An interactive dashboard for sales teams to manually input lead metrics and view conversion probability.
- Dynamic charts demonstrating model performance and feature importance based on batch CSV results.
