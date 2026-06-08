from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from ragas.llms import LangchainLLMWrapper
from langchain_google_genai import ChatGoogleGenerativeAI
from datasets import Dataset
from shared.config import settings

# Extracting the 4 chunk texts from your sources data
CHUNKS = [
    "capacities and utilization [7], with some zones sparsely\nused and others experiencing concentrated demand peaks.\nExternal factors, such as weekday/holiday patterns, weather,\nlocal events, and tariff changes, further modulate demand.\nThe spatial and temporal variability across zones renders\na uniform forecasting model inadequate. Effective manage-\nment requires models that account for inter-zone differences,\nexplicitly address peak periods, and adopt conservative",
    "nated as the training set, while the data from January 1, 2023,\nto January 31, 2023, serves as the out-of-sample test set.\nZones with near-zero training variance are omitted from\nevaluation but retained during anchor training to preserve\ncross-zone transfer. Inputs are min-max normalized per\nzone (train+test by default), with targets scaled similarly\nand converted back to physical units for guardrails and\nevaluation. Timestamp information is transformed into sine",
    "and charging duration are summed within each hour and\nsubsequently aggregated to the level, while occupied-pile\ncounts and price variables are averaged to the hourly cadence.\nA recent dataset revision standardized hourly occupancy to\noccupied-pile counts rather than ratios.\nA chronological, non-overlapping train-test split is used,\naligning all zone-level series across splits. Specifically, the\ndata from September 1, 2022, to December 31, 2022, is desig-",
    "and cosine HOD. Main results use only hourly targets and\ntime-based features, whereas the sensitivity tests may add\noptional prompt flags (e.g., prices, weather data, and calen-\ndar markers) for the LLM adjuster without modifying the\nnumeric backbone.\nThe primary task is single-step forecasting at H ∈ {3, 6, 9}\nhours, relying on input sequences of L = 24. To evaluate how\nstable the results are with respect to the temporal window\nand the forecast range, auxiliary horizons H ∈ {1, 6, 12} and"
]

def get_gemini_llm():
    return LangchainLLMWrapper(
        ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=settings.GEMINI_API_KEY
        )
    )


def test_rag_faithfulness():
    # Setup dataset specifically for faithfulness evaluation
    data = {
        "question": ["what is this document about?"],
        "answer": ["This document is about forecasting, specifically focusing on demand and utilization across different zones, likely related to charging stations"],
        "contexts": [CHUNKS],
        "ground_truth": ["This document is about demand forecasting for EV charging stations across different zones"]
    }
    dataset = Dataset.from_dict(data)
    
    # Run evaluation
    results = evaluate(dataset, metrics=[faithfulness],llm=get_gemini_llm())
    
    # Assert score meets threshold
    assert results['faithfulness'] >= 0.75, f"Faithfulness score {results['faithfulness']} is under 0.75"

def test_rag_answer_relevancy():
    # Setup dataset specifically for answer relevancy evaluation
    data = {
        "question": ["what is this document about?"],
        "answer": ["This document is about forecasting, specifically focusing on demand and utilization across different zones, likely related to charging stations"],
        "contexts": [CHUNKS],
        "ground_truth": ["This document is about demand forecasting for EV charging stations across different zones"]
    }
    dataset = Dataset.from_dict(data)
    
    # Run evaluation
    results = evaluate(dataset, metrics=[answer_relevancy],llm=get_gemini_llm())
    
    # Assert score meets threshold
    assert results['answer_relevancy'] >= 0.70, f"Answer Relevancy score {results['answer_relevancy']} is under 0.70"