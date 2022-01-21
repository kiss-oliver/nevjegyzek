import pandas as pd
import altair as alt
import unidecode
from tqdm import tqdm

tnev = pd.read_csv('../106/data/telepules.csv')

tr = {'á':'aa',
      'Á':'AA',
      'é':'ee',
      'É':'EE',
      'í':'ii',
      'Í':'II',
      'ó':'oo',
      'Ó':'OO',
      'ö':'oox',
      'Ö':'OOX',
      'ő':'ooxx',
      'Ő':'ooXX',
      'ú':'uu',
      'Ú':'UU',
      'ü':'uux',
      'Ü':'UUX',
      'ű':'uuxx',
      'Ű':'UUXX',
     }
tnev['filename'] = tnev.megnev.map(lambda x: ''.join([i if ord(i) < 128 else tr[i] for i in x.replace(" ","").replace(".","")]))

df = pd.read_csv('../106/data/szavazokor.csv').merge(tnev[['maz','taz','megnev','filename']].drop_duplicates(), on=['maz','taz'], how='left')
df['Datum'] = pd.to_datetime(df['version'].map(lambda x: '20220'+str(x)))

for szk in tqdm(list(set(df.szk_nev.tolist()))):
    source = df[df.szk_nev==szk]
    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['Datum'], empty='none')
    
    # The basic line
    line = alt.Chart(source).mark_line(interpolate='basis').encode(
        x=alt.X('Datum:T', title="Dátum"),
        y=alt.Y('honos:Q', title="Fő", scale=alt.Scale(domainMin=source.honos.min()-50, domainMax=source.honos.max()+50)),
        color=alt.value('#1F955C')
    )
    
    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = alt.Chart(source).mark_point().encode(
        x='Datum:T',
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
        text=alt.condition(nearest, 'honos:Q', alt.value(' '))
    )
    
    # Draw a rule at the location of the selection
    rules = alt.Chart(source).mark_rule(color='gray').encode(
        x=alt.X('Datum:T', title="Dátum"),
    ).transform_filter(
        nearest
    )
    
    # Put the five layers into a chart and bind the data
    ch = alt.layer(
        line, selectors, points, rules, text
    ).properties(
        width=600, height=50, title=[szk, source.cim.unique()[0], source.evk_nev.unique()[0]], padding={"left": 5, "top": 5, "right": 50, "bottom": 5}
    )
    
    ch.save('../_includes/{}X{}X{}.json'.format(source.maz.unique()[0],source.taz.unique()[0],source.sorszam.unique()[0]))
