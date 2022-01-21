import pandas as pd
import altair as alt
import unidecode

df = pd.read_csv('../106/data/oevk.csv')
df['Datum'] = pd.to_datetime(df['version'].map(lambda x: '20220'+str(x)))

for m in set(df.evk_nev.tolist()):
    source = df[df.evk_nev==m]
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
        width=600, height=50, title=m, padding={"left": 5, "top": 5, "right": 50, "bottom": 5}
    )
    
    ch.save('../_includes/{}.json'.format(unidecode.unidecode(m.replace("-","").replace(" ","").replace(",","").replace(".",""))))
