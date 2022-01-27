import pandas as pd
import altair as alt
import unidecode

df = pd.read_csv('../106/data/summary.csv')
df['Datum'] = pd.to_datetime(df['version'].map(lambda x: '20220'+str(x)))

df = df.rename(columns={'nemzreSzavaz':'Nemzetiségi listára szavaz','partlistara':'Pártlistára szavaz','levelben':'Levélben szavaz','magyarLakc':'Magyarországi lakcímmel rendelkezik','lakcSzavkorSzavaz':'Lakcíme szerinti szavazókörben szavaz'})

for stat in ['Nemzetiségi listára szavaz', 'Pártlistára szavaz','Levélben szavaz','Magyarországi lakcímmel rendelkezik','Lakcíme szerinti szavazókörben szavaz']:
    source = df
    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['Datum'], empty='none')
    
    # The basic line
    line = alt.Chart(source).mark_line(interpolate='basis').encode(
        x=alt.X('Datum:T', title="Dátum"),
        y=alt.Y(stat, title="Fő", scale=alt.Scale(domainMin=source[stat].min()-50, domainMax=source[stat].max()+50)),
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
        text=alt.condition(nearest, stat, alt.value(' '))
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
        width=600, height=50, title=stat, padding={"left": 5, "top": 5, "right": 50, "bottom": 5}
    )
    
    ch.save('../_includes/SumFigures/{}.json'.format(unidecode.unidecode(stat.replace(" ",""))))


tr = {'bolgar':'Bolgár',
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
 'ukran':'Ukrán'}

for stat in tr.keys():
    source = df
    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['Datum'], empty='none')
    
    # The basic line
    line = alt.Chart(source).mark_line(interpolate='basis').encode(
        x=alt.X('Datum:T', title="Dátum"),
        y=alt.Y(stat, title="Fő", scale=alt.Scale(domainMin=source[stat].min()-50, domainMax=source[stat].max()+50)),
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
        text=alt.condition(nearest, stat, alt.value(' '))
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
        width=600, height=50, title=tr[stat], padding={"left": 5, "top": 5, "right": 50, "bottom": 5}
    )
    
    ch.save('../_includes/SumFigures/{}.json'.format(unidecode.unidecode(stat)))
