import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib as mpl
import numpy as np
import matplotlib.font_manager as fm  # For custom fonts

sns.set_theme(
    style="whitegrid",
    context="talk",        
    palette="Blues",       
    font="Arial"     
)


data = {
    'model': [
        'DeepSeek R1',
        'OpenAI O1 Mini\n(2024-09-12)',
        'Anthropic Claude 3.5 Sonnet',
        'OpenAI GPT-4o\n(2024-11-20)',
        'Anthropic Claude 3.5 Haiku',
        'DeepSeek Chat',
        'Agent DeepSeek Chat',
        'Agent Qwen 2.5 Coder 32B Instruct',
        'Google Gemini Flash 1.5',
        'Agent OpenAI GPT-4o Mini',
        'OpenAI GPT-4o Mini',
        'Qwen 2.5 Coder 32B Instruct',
        'Meta LLaMA 3.1 70B Instruct',
        'Mistral AI Codestral 2501',
        'Mistral AI Codestral Mamba',
        'Microsoft Phi-4'
    ],
    'success_rate': [
        68.8,
        63.5,
        44.1,
        27.8,
        20.5,
        17.7,
        16.7,
        16.7,
        18.4,
        8.3,
        12.0,
        15.6,
        8.3,
        8.3,
        0.0,
        8.3
    ]
}

df = pd.DataFrame(data)
df = df.sort_values('success_rate', ascending=True)

num_bars = len(df)


# Figure and Axes

# Create a gradient transitioning between dark blue and grey
cmap = mpl.colors.LinearSegmentedColormap.from_list(
    "darkblue_grey", ["#1B1F3B", "#3B3B3B"]  # Dark blue to grey
)
darkblue_grey_palette = sns.color_palette([cmap(x) for x in np.linspace(0, 1, num_bars)])






fig, ax = plt.subplots(figsize=(14, 10), dpi=100)

# Background Customizations

fig.patch.set_facecolor('#2E3440')  # Dark slate gray

ax.set_facecolor('#3B4252')  # Slightly lighter than figure

gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))

ax.imshow(
    gradient,
    aspect='auto',
    cmap=mpl.cm.Blues,         
    extent=[0, 1, 0, 1],
    transform=ax.transAxes,
    alpha=0.05,               
    zorder=0                 
)

# Blue palette

cmap = plt.get_cmap('Blues')
blue_palette = sns.color_palette([cmap(x) for x in np.linspace(0.3, 0.7, num_bars)])


# Purple
cmap = plt.get_cmap('Purples')
purple_palette = sns.color_palette([cmap(x) for x in np.linspace(0.3, 0.7, num_bars)])


# Dark Grey Blue

cmap = mpl.colors.LinearSegmentedColormap.from_list(
    "darkblue_grey", ["#1B1F3B", "#3B3B3B"]  
)

# Orange

cmap = plt.get_cmap('Oranges')
orange_palette = sns.color_palette([cmap(x) for x in np.linspace(0.3, 0.7, num_bars)])

# Yellow 1

cmap = plt.get_cmap('YlGnBu')
yellow_blue_palette = sns.color_palette([cmap(x) for x in np.linspace(0.1, 0.4, num_bars)])

# Yellow 2

cmap = mpl.colors.LinearSegmentedColormap.from_list(
    "bright_yellow", ["#FFF700", "#FFD700"]  # Two shades of bright yellow
)
bright_yellow_palette = sns.color_palette([cmap(x) for x in np.linspace(0, 1, num_bars)])

# Red

cmap = plt.get_cmap('Reds')
red_palette = sns.color_palette([cmap(x) for x in np.linspace(0.3, 0.7, num_bars)])

# Bar Plot

bars = sns.barplot(
    data=df,
    x='success_rate',
    y='model',
    palette=darkblue_grey_palette,
    edgecolor=".2",
    linewidth=1.5,
    ax=ax
)




plt.title(
    'Model Success Rates for C++ AOC 2024',
    fontsize=24,                
    fontweight='bold',         
    pad=30,                   
    color='white',           
    fontname='Arial'        
)

for bar in bars.patches:
    width = bar.get_width()
    y = bar.get_y() + bar.get_height() / 2
    plt.text(
        width + 0.5, y,
        f'{width}%',
        va='center',
        fontsize=12,             
        fontweight='semibold',  
        color='white',         
        fontname='Arial'      
    )

plt.xlabel(
    'Success Rate (%)',
    fontsize=16,                
    fontweight='bold',         
    labelpad=15,              
    color='white',           
    fontname='Arial'        
)
plt.ylabel(
    'Model',
    fontsize=16,           
    fontweight='bold',    
    labelpad=15,         
    color='white',      
    fontname='Arial'   
)

ax.xaxis.grid(True, linestyle='--', which='major', color='grey', alpha=0.3)
ax.yaxis.grid(False)

plt.xticks(fontsize=12, color='white', fontname='Arial')
plt.yticks(fontsize=12, color='white', fontname='Arial')

sns.despine(left=True, bottom=True)

plt.xlim(0, max(df['success_rate']) * 1.1)

plt.tight_layout()

plt.show()

