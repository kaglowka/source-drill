import plotly.graph_objects as go
import textwrap
import numpy as np

def plot_text_sim(similarities: list, texts: list):
    plt_texts = []
    shorten_width = 1000 # characters
    line_width = 60
    for text in texts:
        # first add "[...]" for very long texts
        text = textwrap.shorten(text, width=shorten_width)
        # wrap
        lines = textwrap.wrap(text, width=line_width)
        plt_texts.append('<br>'.join(lines))
        
    
    fig = go.Figure(
        data = [
            go.Bar(
                x=np.arange(0, len(similarities)), 
                y=similarities, 
                hovertext=plt_texts,
            )
        ]
    )
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white", 
            font_size=13, 
            font_family="Rockwell"
        ),)
    _ = fig.show()
    return fig
 