from src.data_ingestion.data_loader import load_clean_data
from src.utils.filtering import get_date_ranges_from_years, filter_dataframe
from src.utils.cache import cache

@cache.memoize(timeout=300)
def get_filtered_data(selected_years, selected_portfolios, year_mode):
    """
    Retorna payments_df y pledges_df ya filtrados según los filtros recibidos.
    Está memoizado, de modo que si se llama repetidamente con los mismos
    parámetros, no vuelve a recalcular.
    """
    dfs = load_clean_data()  # Este también está cacheado, así que es doble capa de caching
    payments_df = dfs.get("payments", None)
    pledges_df = dfs.get("pledges", None)

    if payments_df is None or pledges_df is None:
        return (None, None)

    # 1) Filtrar payments por fechas:
    if selected_years:
        date_ranges = get_date_ranges_from_years(selected_years, year_mode)
        mask = False
        for (start_dt, end_dt) in date_ranges:
            mask |= (payments_df["date"] >= start_dt) & (payments_df["date"] <= end_dt)
        payments_df = payments_df[mask]

    # 2) Filtrar payments por portfolio
    if selected_portfolios:
        payments_df = filter_dataframe(payments_df, {"portfolio": selected_portfolios})

    # 3) Filtrar pledges por fecha (si corresponde)
    if selected_years:
        p_mask = False
        for (start_dt, end_dt) in date_ranges:
            p_mask |= (
                (pledges_df["pledge_created_at"] >= start_dt)
                & (pledges_df["pledge_created_at"] <= end_dt)
            )
        pledges_df = pledges_df[p_mask]

    # 4) (Opcional) filtrar pledges por portfolio si tu lógica lo requiere
    #    p.ej. si el 'portfolio' no está en pledges, puedes hacer un merge
    #    o simplemente ignorarlo.

    return payments_df, pledges_df
