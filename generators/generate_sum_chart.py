import pandas as pd
import altair as alt
from altair_saver import save
alt.renderers.enable('default')

two_charts_template = """
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/vega@{vega_version}"></script>
  <script src="https://cdn.jsdelivr.net/npm/vega-lite@{vegalite_version}"></script>
  <script src="https://cdn.jsdelivr.net/npm/vega-embed@{vegaembed_version}"></script>
</head>
<body>

<div id="vis1"></div>
<div id="vis2"></div>

<script type="text/javascript">
  vegaEmbed('#vis1', {spec1}).catch(console.error);
  vegaEmbed('#vis2', {spec2}).catch(console.error);
</script>
</body>
</html>
"""

df = pd.read_csv('../106/data/summary.csv')
df['Datum'] = pd.to_datetime(df['version'].map(lambda x: '20220'+str(x)))

sumdata = pd.melt(df, id_vars=['Datum'], value_vars=['lakcSzavkorSzavaz','magyarLakc','levelben','partlistara','nemzreSzavaz']).rename(columns={'Datum':"Dátum",'value':'Fő','variable':'Szavazás módja'})
sumdata['Szavazás módja']=sumdata['Szavazás módja'].map(lambda x: {'nemzreSzavaz':'Nemzetiségi listára szavaz','partlistara':'Pártlistára szavaz','levelben':'Levélben szavaz','magyarLakc':'Magyarországi lakcímmel rendelkezik','lakcSzavkorSzavaz':'Lakcíme szerinti szavazókörben szavaz'}[x])

source = sumdata
nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['Dátum'], empty='none')

line = alt.Chart(source).mark_line().encode(
    x='Dátum:T',
    y=alt.Y("Fő:Q", scale = alt.Scale(type='pow', exponent=0.85)),
    color=alt.Color('Szavazás módja:N', legend=alt.Legend(columns=3))
)

# Transparent selectors across the chart. This is what tells us
# the x-value of the cursor
selectors = alt.Chart(source).mark_point().encode(
    x='Dátum:T',
    opacity=alt.value(0),
).add_selection(
    nearest
)

# Draw points on the line, and highlight based on selection
points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

# Draw text labels near the points, and highlight based on selection
text = line.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest, 'Fő:Q', alt.value(' '))
)

# Draw a rule at the location of the selection
rules = alt.Chart(source).mark_rule(color='gray').encode(
    x='Dátum:T',
).transform_filter(
    nearest
)

# Put the five layers into a chart and bind the data
chart = alt.layer(
    line, selectors, points, rules, text
).properties(title='Szavazók összesített száma',
    width=600, height=180
)

chart1 = chart.configure_legend(
labelLimit= 0,
    orient='bottom'
) 



sumdata = pd.melt(df, id_vars=['Datum'], value_vars=['bolgar',
 'gorog',
 'horvat',
 'lengyel',
 'nemet',
 'ormeny',
 'roma',
 'roman',
 'ruszin',
 'szerb',
 'szlovak',
 'szloven',
 'ukran']).rename(columns={'Datum':"Dátum",'value':'Fő','variable':'Nemzetiség'})

sumdata['Nemzetiség']=sumdata['Nemzetiség'].map(lambda x: {'bolgar':'Bolgár',
 'gorog':'Görög',
 'horvat':'Horvát',
 'lengyel':'Lengyel',
 'nemet':'Német',
 'ormeny':"Örmény",
 'roma':'Roma',
 'roman':'Román',
 'ruszin':'Ruszin',
 'szerb':'Szerb',
 'szlovak':'Szlovák',
 'szloven':'Szlovén',
 'ukran':'Ukrán'}[x])

source = sumdata
nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['Dátum'], empty='none')

line = alt.Chart(source).mark_line().encode(
    x='Dátum:T',
    y=alt.Y("Fő:Q", scale = alt.Scale(type='log')),
    color=alt.Color('Nemzetiség:N', legend=alt.Legend(columns=7))
)

# Transparent selectors across the chart. This is what tells us
# the x-value of the cursor
selectors = alt.Chart(source).mark_point().encode(
    x='Dátum:T',
    opacity=alt.value(0),
).add_selection(
    nearest
)

# Draw points on the line, and highlight based on selection
points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

# Draw text labels near the points, and highlight based on selection
text = line.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest, 'Fő:Q', alt.value(' '))
)

# Draw a rule at the location of the selection
rules = alt.Chart(source).mark_rule(color='gray').encode(
    x='Dátum:T',
).transform_filter(
    nearest
)

# Put the five layers into a chart and bind the data
chart = alt.layer(
    line, selectors, points, rules, text
).properties(title='Nemzetiségi listákra szavazók összesített száma',
    width=600, height=180
)

chart2 = chart.configure_legend(
labelLimit= 0,
    orient='bottom'
) 

with open('../_includes/osszesitett.html', 'w') as f:
    f.write(two_charts_template.format(
        vega_version=alt.VEGA_VERSION,
        vegalite_version=alt.VEGALITE_VERSION,
        vegaembed_version=alt.VEGAEMBED_VERSION,
        spec1=chart1.to_json(indent=None),
        spec2=chart2.to_json(indent=None),
    ))
