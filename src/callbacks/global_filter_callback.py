import json
import pandas as pd
from dash.dependencies import Input, Output, State
from src.data_ingestion.data_loader import load_clean_data
from src.utils.filtering import filter_dataframe, get_date_ranges_from_years

def register_global_filter_callbacks(app):
    @app.callback(
        Output("store-filtered-data", "data"),
        [Input("year-filter", "value"),
         Input("portfolio-filter", "value"),
         Input("year-mode", "value")]
    )
    def global_filtering_callback(selected_years, selected_portfolios, year_mode):

        # 1) cargar data
        dfs = load_clean_data()
        payments_df = dfs.get("payments", pd.DataFrame())
        pledges_df = dfs.get("pledges", pd.DataFrame())

        # 2) Construir las máscaras/filtros
        #    a) date range segun selected_years y year_mode
        filtered_payments = payments_df
        if selected_years:
            date_ranges = get_date_ranges_from_years(selected_years, year_mode)
            mask = False
            for (start_dt, end_dt) in date_ranges:
                mask |= (filtered_payments["date"] >= start_dt) & (filtered_payments["date"] <= end_dt)
            filtered_payments = filtered_payments[mask]

        #    b) filtrar portfolio en payments
        if selected_portfolios:
            filtered_payments = filter_dataframe(filtered_payments, {"portfolio": selected_portfolios})

        # 3) (Opcional) filtrar pledges por la misma lógica de date-range:
        #    Este ya es más raro, porque para pledges tu "fecha de referencia" es pledge_starts_at?
        #    O a veces no quieres filtrar pledges por fecha. Depende de tu necesidad.
        #    Ejemplo de filtrar pledges en base al "pledge_created_at":
        if selected_years:
            # create a similar mask for pledges
            p_mask = False
            for (start_dt, end_dt) in date_ranges:
                p_mask |= (pledges_df["pledge_created_at"] >= start_dt) & (pledges_df["pledge_created_at"] <= end_dt)
            filtered_pledges = pledges_df[p_mask]
        else:
            filtered_pledges = pledges_df

        # c) Si quisieras filtrar pledges por portfolio, normalmente se hace join con payments.
        #    O si ya tienes un 'portfolio' en pledges. Es tu decisión.

        # 4) Convertir a JSON para almacenarlo en el dcc.Store
        #    Lo recomendable es reducir el DF a dict y luego a JSON:

        # Convertir datetime64 a string en payments
        for col in filtered_payments.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns:
            filtered_payments[col] = filtered_payments[col].dt.strftime("%Y-%m-%d %H:%M:%S")

        # Convertir datetime64 a string en pledges
        for col in filtered_pledges.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns:
            filtered_pledges[col] = filtered_pledges[col].dt.strftime("%Y-%m-%d %H:%M:%S")

        filtered_data = {
            "payments": filtered_payments.to_dict("records"),
            "pledges": filtered_pledges.to_dict("records"),
        }
        return json.dumps(filtered_data)
