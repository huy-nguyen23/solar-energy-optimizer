import plotly.express as px
import pandas as pd

def create_energy_distribution_pie_chart(self_used_kwh: float, unused_exported_kwh: float):
    """
    Creates a pie chart showing the distribution of self-consumed vs unused/exported energy.
    
    Args:
        self_used_kwh (float): The amount of solar energy consumed directly by the household.
        unused_exported_kwh (float): The excess solar energy not used or exported to the grid.
        
    Returns:
        plotly.graph_objects.Figure: The generated pie chart figure.
    """
    pie_data = pd.DataFrame({
        "Energy Category": ["Self-Consumed (Saved Money)", "Unused / Exported to Grid"],
        "kWh per Month": [self_used_kwh, unused_exported_kwh]
    })  
    fig_pie = px.pie(pie_data, values="kWh per Month", names="Energy Category", 
                     title="Monthly Solar Energy Distribution",
                     color="Energy Category",
                     color_discrete_map={
                         "Self-Consumed (Saved Money)": "#2ca02c", 
                         "Unused / Exported to Grid": "#ff7f0e"
                     })
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    return fig_pie

def create_monthly_generation_bar_chart(generation_df: pd.DataFrame):
    """
    Creates a bar chart comparing monthly generation across different system sizes.
    
    Args:
        generation_df (pd.DataFrame): DataFrame containing generation data per month and system size.
        
    Returns:
        plotly.graph_objects.Figure: The generated bar chart figure.
    """
    chart_data = generation_df.pivot(index='month', columns='system_kwp', values='generation_kwh').reset_index()
    fig_bar = px.bar(chart_data, x="month", y=[c for c in chart_data.columns if c != "month"],
                     title="Estimated Monthly Generation (kWh)",
                     barmode="group")
    return fig_bar

def create_cumulative_cash_flow_line_chart(investment_cost_vnd: float, annual_saving_vnd: float, max_years: int = 15):
    """
    Creates a line chart tracing the return on investment over the specified number of years.
    
    Args:
        investment_cost_vnd (float): The total upfront investment cost.
        annual_saving_vnd (float): The estimated annual savings from self-consumed energy.
        max_years (int): The number of years to trace the cash flow (default 15).
        
    Returns:
        plotly.graph_objects.Figure: The generated line chart figure showing cumulative ROI.
    """
    years = list(range(0, max_years + 1))
    cash_flows = [(-investment_cost_vnd + annual_saving_vnd * y) for y in years]
    cf_df = pd.DataFrame({"Year": years, "Cumulative Cash Flow (VND)": cash_flows})
    
    fig_line = px.line(cf_df, x="Year", y="Cumulative Cash Flow (VND)", 
                       title=f"Projected ROI over {max_years} Years", markers=True)
    fig_line.add_hline(y=0, line_dash="dash", line_color="green", annotation_text="Break-even Point")
    return fig_line