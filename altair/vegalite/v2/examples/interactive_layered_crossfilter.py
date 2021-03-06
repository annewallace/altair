"""
Crossfilter
===========
This example shows a multi-panel view of the same data, where you can interactively
select a portion of the data in any of the panels to highlight that portion in any
of the other panels.
"""
# category: interactive

import altair as alt
from vega_datasets import data

flights = alt.UrlData(data.flights_2k.url,
                      format={'parse': {'date': 'date'}})

brush = alt.selection(type='interval', encodings=['x'])

# Define the base chart, with the common parts of the
# background and highlights
base = alt.Chart().mark_bar().encode(
    x=alt.X(alt.repeat('column'), type='quantitative', bin=alt.Bin(maxbins=20)),
    y='count(*):Q'
).properties(
    width=180,
    height=130
)

# blue background with selection
background = base.properties(
    selection=brush
)

# yellow highlights on the transformed data
highlight = base.encode(
    alt.ColorValue('goldenrod')
).transform_filter(
    brush.ref()
)

# layer the two charts & repeat
chart = alt.layer(
    background, highlight,
    data=flights
).transform_calculate(
    "time", "hours(datum.date)"
).repeat(
    column=["distance", "delay", "time"]
)
