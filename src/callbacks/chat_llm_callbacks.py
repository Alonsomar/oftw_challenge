# src/callbacks/chat_llm_callbacks.py

import os
import json
import openai
import pandas as pd

from dash.dependencies import Input, Output, State
from src.utils.cache import cache
from src.utils.callbacks_filter import get_filtered_data
from dotenv import load_dotenv

load_dotenv()

# Retrieve the API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Instantiate the OpenAI client with your API key
openai_client = openai.OpenAI(api_key=api_key)

# ---------------------------------------------------------
# Helper function to check the length of the user's question
# ---------------------------------------------------------
def check_question_length(question: str, max_chars: int = 300) -> bool:
    """
    Verifies if the question exceeds the specified character limit.
    Returns True if within limit, False otherwise.
    """
    return len(question) <= max_chars


# ---------------------------------------------------------
# Function to build a richer context from payments & pledges
# ---------------------------------------------------------
def create_rich_context(payments_df: pd.DataFrame, pledges_df: pd.DataFrame) -> str:
    """
    Generates a more detailed text summary of the filtered payments and pledges,
    giving the LLM additional background metrics.
    """
    context_lines = []

    # --- Summaries from payments_df ---
    if payments_df is not None and not payments_df.empty:
        total_usd = payments_df["amount_usd"].sum()
        count_payments = len(payments_df)
        avg_payment = payments_df["amount_usd"].mean()

        context_lines.append(f"PAYMENTS SUMMARY:")
        context_lines.append(f"- Total Payments: {count_payments} payments.")
        context_lines.append(f"- Sum of Payments in USD: {total_usd:.2f}.")
        context_lines.append(f"- Average Payment in USD: {avg_payment:.2f}.")

        if "payment_platform" in payments_df.columns:
            platform_counts = payments_df["payment_platform"].value_counts().head(3)
            if not platform_counts.empty:
                top_platforms = ", ".join(
                    [f"{plat} ({count} payments)" for plat, count in platform_counts.items()]
                )
                context_lines.append(f"- Top Payment Platforms (up to 3): {top_platforms}")
    else:
        context_lines.append("PAYMENTS SUMMARY: No payment data available for this filtered context.")

    context_lines.append("")  # Blank line for readability

    # --- Summaries from pledges_df ---
    if pledges_df is not None and not pledges_df.empty:
        context_lines.append(f"PLEDGES SUMMARY:")
        total_pledges = len(pledges_df)
        context_lines.append(f"- Total Pledges: {total_pledges}.")

        if "pledge_status" in pledges_df.columns:
            status_counts = pledges_df["pledge_status"].value_counts()
            if not status_counts.empty:
                statuses = ", ".join([f"{status} ({cnt})" for status, cnt in status_counts.items()])
                context_lines.append(f"- Status distribution: {statuses}")

        if "frequency" in pledges_df.columns:
            freq_counts = pledges_df["frequency"].value_counts()
            if not freq_counts.empty:
                freq_info = ", ".join([f"{freq} ({cnt})" for freq, cnt in freq_counts.items()])
                context_lines.append(f"- Frequency distribution: {freq_info}")

        # Could add more pledge-specific calculations (Active ARR, Future ARR, etc.)
        # if you want to incorporate that logic here.
    else:
        context_lines.append("PLEDGES SUMMARY: No pledge data available for this filtered context.")

    # Join everything into a single text block
    return "\n".join(context_lines)

def register_chat_llm_callbacks(app):
    @app.callback(
        Output("chat-llm-response", "children"),
        [Input("chat-llm-submit", "n_clicks")],
        [
            State("chat-llm-input", "value"),
            Input("year-filter", "value"),
            Input("portfolio-filter", "value"),
            Input("year-mode", "value")
        ],
        prevent_initial_call=True
    )
    @cache.memoize(timeout=300)  # optional caching for repeated queries
    def run_chat_llm(n_clicks, user_question, selected_years, selected_portfolios, year_mode):
        """
        Calls the OpenAI API (or another LLM) to answer the user's question,
        using filtered data as context (if any).
        """

        # 1) Check if there's a question at all
        if not user_question:
            return "Please enter a question before hitting 'Send'."

        # 2) Check the character limit
        if not check_question_length(user_question):
            return (
                "Your question is too long. Please keep it under 300 characters "
                "and try again."
            )

        # 3) Prepare the filtered data context
        payments_df, pledges_df = get_filtered_data(selected_years, selected_portfolios, year_mode)

        # Build a robust context summary
        context_text = create_rich_context(payments_df, pledges_df)

        # 4) Build the system message and user prompt
        system_prompt = """
            You are a specialized data assistant for the One for the World (OFTW) organization. You have access to the following high-level context about the data, metrics, and codebase:    
            1) **Data & Datasets**:
               - **Pledges dataset** (pledge_id, donor_id, donor_chapter, chapter_type, pledge_status, pledge_created_at, pledge_starts_at, pledge_ended_at, contribution_amount, currency, frequency, payment_platform). 
                 - Each pledge records a donor’s intention to give recurring or one-time donations. It may be active, pledged (i.e. starting in the future), or canceled.
               - **Payments dataset** (id, donor_id, payment_platform, portfolio, amount, currency, date, counterfactuality, pledge_id).
                 - Each payment is an actual monetary transaction made by a donor on a certain date and might belong to a pledge. The "counterfactuality" factor (0–1) represents how much of this donation is truly attributable to OFTW’s influence.
            
            2) **Core Metrics & Definitions**:
               - **Money Moved**: The sum of relevant donations, converted to USD. This excludes certain portfolios such as “One for the World Discretionary Fund” or “One for the World Operating Costs,” focusing on the recommended charities.
               - **Counterfactual Money Moved**: Each donation multiplied by its counterfactual factor, to capture how much was uniquely caused by OFTW’s influence.
               - **Annualized Run Rate (ARR)**: A projection of yearly donation amounts based on the frequency in pledges (e.g., monthly pledges get multiplied by 12, quarterly by 4, etc.). Often subdivided into Active ARR (for “Active donor” pledges) and Future ARR (for “Pledged donor”).
               - **Pledge Performance**: Tracks the total of all pledges (active + future), the monthly attrition rate (how many pledges are lost or fail), and breakdowns by channel or chapter type.
               - **OKRs / Wishlist Metrics** (examples):
                 - Target $1.8M Money Moved by 2025,
                 - $1.2M Active ARR,
                 - 1200 total active donors,
                 - 850 active pledges,
                 - 18% pledge attrition rate, etc.
            
            3) **Filters**:
               - Users can filter the data by:
                 - **Year mode**: either “calendar” (Jan–Dec) or “fiscal” (Jul–Jun).
                 - **Year(s)**: e.g. 2023, 2024, etc., which define date ranges depending on the year mode.
                 - **Portfolio**: e.g., “OFTW Top Picks,” “Entire OFTW Portfolio,” or custom top picks.
            
            4) **Technical/Code Structure**:
               - The codebase is a Dash application with separate pages (Home, Money Moved, Pledge Performance, Objectives & Key Results, Notes, plus a new Chat LLM page).
               - The data ingestion converts all amounts to USD using historical currency rates, ignoring “One for the World Discretionary Fund” or “Operating Costs” in main metrics.
               - A variety of metrics are computed in dedicated modules (e.g., `money_metrics`, `performance_metrics`, `objectics_metrics`).
               - The user can combine filters (year, year-mode, portfolio) to see custom slices of the data.
            
            5) **How You Should Respond**:
               - Always answer in English.
               - Remain consistent with the above definitions of money moved, pledge statuses, and methodological assumptions.
               - If a user asks about specific calculations or code references, rely on these data definitions and the typical approach in the code (ARR = frequency factor × contribution amount in USD, etc.).
               - If uncertain because the code or data does not specify details, politely say you do not have enough information.
               - If the user’s question is longer than allowed or if it contradicts known constraints, provide an appropriate disclaimer.
            
            Your main objective: Provide coherent, concise, and accurate answers about the OFTW data, metrics, and logic described in the codebase. Do not fabricate details that are not supported by the provided context. If asked about numeric results, use the actual data context available (or disclaim you do not have it if not included).
            
            Remember: Respond strictly in English, reference only the known data and approach from the codebase, and keep your explanations straightforward but sufficiently detailed to be helpful.
        """

        user_prompt = (
            f"Context:\n{context_text}\n\n"
            f"User Question:\n{user_question}"
        )

        # 5) Call the OpenAI Chat Completion endpoint
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",  # Adjust to the model you want to use
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2
            )
            # Extract the LLM's reply
            answer = response.choices[0].message.content
        except Exception as e:
            answer = f"Error while calling the LLM: {e}"

        return answer
