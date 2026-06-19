import plotly.express as px 

def plot_monthly_solar_radiation(df):
    monthly_df=df[df['month_number']<13]
    fig=px.bar(
        monthly_df,
        x='month_number',
        y='solar_radiation',
        title='Monthly Solar Radiation',
        labels={
            'month_number':'Month',
            'solar_radiation':'Solar Radiation (kWh/m²/day)'
        },
        text_auto='.2f'
    )
    return fig
    