import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pypalettes import load_cmap
from highlight_text import ax_text, fig_text
from pyfonts import load_font
from drawarrow import ax_arrow
from pypalettes import load_cmap
import matplotlib.patches as patches
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import warnings
warnings.filterwarnings("ignore")

# file local drive paths
polio_est_reported = r"D:\Learning\Data Visualization\data\india\polio\data\polio_india_reported_estimated.csv"
polio_vaccines = r"D:\Learning\Data Visualization\data\india\polio\data\vac_india_all_sub.csv"
# data import
data_polio_cases = pd.read_csv(polio_est_reported)
data_polio_vaccines = pd.read_csv(polio_vaccines)

# avoid tampering original import
df_polio_cases = data_polio_cases.copy()
df_polio_vac = data_polio_vaccines.copy()

# truncated data of interest
df_polio_cases = df_polio_cases[["Year", "Total polio cases", "Estimated polio cases"]]
df_polio_vac = df_polio_vac[["year", "POLIO"]]

# data for plotting
years = list(range(1981, 2024))
polio_cases = df_polio_cases["Total polio cases"]
polio_vacs = df_polio_vac["POLIO"]

# specific values for highlighting events
polio_vac_1985 = float(df_polio_vac[df_polio_vac["year"]==1985]["POLIO"].values) 
polio_vac_1995 = float(df_polio_vac[df_polio_vac["year"]==1995]["POLIO"].values) 
polio_case_last_2011 = 1
polio_free_vac_given = float(df_polio_vac[df_polio_vac["year"]==2014]["POLIO"].values) 
polio_vac_ipv = float(df_polio_vac[df_polio_vac["year"]==2015]["POLIO"].values) 

# FONTS

# Gentium Book Plus
gbp_reg = load_font(r"https://github.com/google/fonts/blob/main/ofl/gentiumbookplus/GentiumBookPlus-Regular.ttf?raw=true")
gbp_i = load_font(r"https://github.com/google/fonts/blob/main/ofl/gentiumbookplus/GentiumBookPlus-Italic.ttf?raw=true")
gbp_b = load_font(r"https://github.com/google/fonts/blob/main/ofl/gentiumbookplus/GentiumBookPlus-Bold.ttf?raw=true")
gbp_bi = load_font(r"https://github.com/google/fonts/blob/main/ofl/gentiumbookplus/GentiumBookPlus-BoldItalic.ttf?raw=true")


# COLOR PALLETES

# red tones (dark to light)
cmap_red = load_cmap("X26").colors
# blue tones (dark to light)
cmap_blue = load_cmap("Ostracion_whitleyi").colors
# background color
bg_white = "#F8F8F8FF"


# TEXT SYLE
text_style = dict(
    size=7, ha="left"
)


#########################################################

fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(17, 15))

ax1, ax2 = axs

fig.set_facecolor(bg_white)
ax1.set_facecolor(bg_white)
ax2.set_facecolor(bg_white)

# restrict plot to certain % of canvas space
fig.subplots_adjust(top=0.85, bottom=0.08, hspace=0.35, left=0.1)

#########################################################

# plot title & sub-title
title = "<Do Boond> Zindagi Ke"
fig_text(s=title, x=0.084, y=.88, ha="left",
         size=24, font=gbp_reg,
         highlight_textprops=[
             dict(font=gbp_b, size=24.5, color=cmap_blue[-3])
         ])

sub_title = "How India became <Polio-free> in <2014>"
fig_text(s=sub_title, x=0.084, y=0.854, ha="left",
         size=13, font=gbp_reg,
         highlight_textprops=[
             dict(font=gbp_b, size=14, color=cmap_blue[-3]),
             dict(font=gbp_b, size=14, color=cmap_blue[-3])
         ])

#########################################################

# cleaning up canvas
ax1.tick_params(axis="both", which="both", length=0)
ax1.ticklabel_format(axis='y', style='plain')
ax2.tick_params(axis="both", which="both", length=0)
ax2.ticklabel_format(axis='y', style='plain')
ax1.spines[["top", "right", "left"]].set_visible(0)
ax2.spines[["top", "right", "left"]].set_visible(0)


ax1.set_xlim((1980,2024))
ax2.set_xlim((1980,2024))

# axis labels
ax1.set_xlabel("Years", **text_style)
ax1.set_xticks(
      [1981, 1991, 2001, 2011, 2021],
      labels=[1981, 1991, 2001, 2011, 2021])
ax1.set_yticks([1000000*5, 1000000*10, 1000000*15, 1000000*20])
ax1.set_yticklabels(["50L", "1Cr", "1.5Cr", "2Cr"],
                    fontdict=dict(size=8.5))
ax1.set_ylim((0, 25000000))

ax2.set_xlabel("Years", **text_style)
ax2.set_xticks(
      [1981, 1991, 2001, 2011, 2021],
      labels=[1981, 1991, 2001, 2011, 2021])
ax2.set_yticks([10000, 20000, 30000, 40000])
ax2.set_yticklabels(["10K", "20K", "30K", "40K"],
                    fontdict=dict(size=8.5))
ax2.set_ylim((-1000, 41000))

#########################################################

# PLOT 1: Total vaccines given per year

# vac plot
ax1.plot(years, polio_vacs, color=cmap_blue[2])
ax1.grid(linestyle=":", linewidth=0.65, alpha=0.55,
         axis="y", color=cmap_blue[1])

# vac plot legend
ax_text(
    s="<Polio vaccines>\nadministered\nper year",
    x=2023.35, y=23600000,
    font=gbp_b, color=cmap_blue[0], size=13,
    highlight_textprops=[
        dict(font=gbp_b, color=cmap_blue[2])
    ], ax=ax1
)

# vac plot hightlights

# Highlight 1: UIP expansion

dot_uip = patches.Ellipse(
  xy=(1985, polio_vac_1985),
  width=0.3, height=500000,
  alpha=1,
  facecolor=cmap_blue[2],
  edgecolor=cmap_blue[0],
  linewidth=0.5, zorder=5
)
ax1.add_patch(dot_uip)

# arrow for UIP expansion
ax_arrow(
    head_position=[1985, 7000000],
    tail_position=[1985, polio_vac_1985+150000],
    ax=ax1, radius=0, color=cmap_blue[1],
    fill_head=True, head_width=1.85, zorder=10
)

# text for UIP expansion
ax_text(
    s="<UIP><*> expanded\nto <rural> India\nin year <1985>",
    x=1985.2, y=9650000, font=gbp_reg, size=11, ha="center", ax=ax1,
    highlight_textprops=[
        dict(font=gbp_b, size=11, color=cmap_blue[1]),
        dict(font=gbp_reg, size=6, color=cmap_blue[0]),
        dict(font=gbp_b, size=11, color=cmap_blue[1]),
        dict(font=gbp_b, size=11, color=cmap_blue[1])
    ]
)


# Highlight 2: pulse polio campaign

dot_pulse_polio = patches.Ellipse(
  xy=(1995, polio_vac_1995*.995),
  width=0.3, height=500000,
  alpha=1,
  facecolor=cmap_blue[2],
  edgecolor=cmap_blue[0],
  linewidth=0.5, zorder=5
)
ax1.add_patch(dot_pulse_polio)

# arrow for pulse polio campaign
ax_arrow(
    head_position=[1995, 20900000],
    tail_position=[1995, polio_vac_1995+70000],
    ax=ax1, radius=0, color=cmap_blue[1],
    fill_head=True, head_width=1.85, zorder=10
)

# text for pulse polio campaign
ax_text(
    s="<Pulse Polio Campaign>\nlaunched in year <1995> with the\nslogan <'Do Boond Zindagi Ki'> (Two drops of life)",
    x=2002, y=25000000, font=gbp_reg, size=11, ha="center",
    highlight_textprops=[
        dict(font=gbp_b, size=11, color=cmap_blue[1]),
        dict(font=gbp_b, size=11, color=cmap_blue[1]),
        dict(font=gbp_i, size=11, color=cmap_blue[1])
    ], ax=ax1
)
ax_text(
    s="<8.8Cr> children <under 3 years> age immunized in that year.",
    x=1997.35, y=21950000, font=gbp_i, size=10, ha="left",
    highlight_textprops=[
        dict(font=gbp_i, size=10, color=cmap_blue[1]),
        dict(font=gbp_i, size=10, color=cmap_blue[1])
    ], ax=ax1
)

# image for pulse polio campaign
image_pulse = mpimg.imread(r"D:\Learning\Data Visualization\data\india\polio\images\pulse_polio_ab_campaign.jpg")
img_pulse = OffsetImage(image_pulse, zoom=0.1)
# position (x, y) in data coordinates
position = (1995, 23500000)
ab_pulse = AnnotationBbox(img_pulse, position, xycoords='data', frameon=False)
# Add to the plot
ax1.add_artist(ab_pulse)

# Highlight 3: India introduced Inactivated Polio Vaccince (IPV)

dot_ipv = patches.Ellipse(
  xy=(2015, polio_vac_ipv),
  width=0.3, height=500000,
  alpha=1,
  facecolor=cmap_blue[2],
  edgecolor=cmap_blue[0],
  linewidth=0.5, zorder=5
)
ax1.add_patch(dot_ipv)

# arrow for IPV intro.
ax_arrow(
    head_position=[2015, 16000000],
    tail_position=[2015, polio_vac_ipv-70000],
    ax=ax1, radius=0, color=cmap_blue[1],
    fill_head=True, head_width=1.85, zorder=10
)

# text for IPV intro
ax_text(
    s="<IPV><*> introduced\nby India in year <2015>",
    x=2015.5, y=16000000, font=gbp_reg, size=11, ha="center",
    highlight_textprops=[
        dict(font=gbp_b, size=11, color=cmap_blue[1]),
        dict(font=gbp_reg, size=6, color=cmap_blue[0]),
        dict(font=gbp_b, size=11, color=cmap_blue[1])
    ], ax=ax1
)

# * Mark definitions
fig_text(
    x=0.084, y=0.47,
    s="*UIP: Universal Immunization Program",
    font=gbp_i, size=7, color=cmap_blue[0], ha="left"
)
fig_text(
    x=0.084, y=0.46,
    s="*IPV: Inactivated Polio-virus Vaccine (for additional protection, especially against type 2 poliovirus)",
    font=gbp_i, size=7, color=cmap_blue[0], ha="left"
)


#########################################################

# PLOT 2: Total reported cases of paralytic polio per year

# polio cases plot
ax2.plot(years, polio_cases, color=cmap_red[2])
ax2.grid(linestyle=":", linewidth=0.65, alpha=0.55,
         axis="y", color=cmap_red[1])

# polio plot legend
ax_text(
    s="No. of cases\nof <paralytic polio>",
    x=2023.35, y=2970, ha="left", size=13,
    font=gbp_b, color=cmap_red[0],
    highlight_textprops=[
        dict(font=gbp_b, color=cmap_red[2])
    ], ax=ax2
)


# polio plot hightlights

# Highlight 1: Zero reported cases

dot_zero_polio = patches.Ellipse(
  xy=(2012, 0),
  width=0.3, height=800,
  alpha=1,
  facecolor=cmap_red[2],
  edgecolor=cmap_red[0],
  linewidth=0.5, zorder=5
)
ax2.add_patch(dot_zero_polio)

# arrow for zero polio cases
ax_arrow(
    head_position=[2012, 8500],
    tail_position=[2012, 2],
    ax=ax2, radius=0, color=cmap_red[1],
    fill_head=True, head_width=1.85, zorder=10
)

# text for zero polio cases
ax_text(
    s="<Zero> cases reported\nfor first time\nin the year <2012>",
    x=2012.5, y=13500, font=gbp_reg, size=11, ha="center",
    highlight_textprops=[
        dict(font=gbp_b, size=11, color=cmap_red[1]),
        dict(font=gbp_b, size=11, color=cmap_red[1])
    ]
)

# Highlight 2: Last reported case of polio in 2011 Howrah, West Bengal

dot_last_polio = patches.Ellipse(
  xy=(2011, 0),
  width=0.3, height=800,
  alpha=1,
  facecolor=cmap_red[2],
  edgecolor=cmap_red[0],
  linewidth=0.5, zorder=5
)
ax2.add_patch(dot_last_polio)

# arrow for Last reported case of polio in 2011 Howrah, West Bengal
ax_arrow(
    head_position=[2011, 1],
    tail_position=[2007, 7500],
    ax=ax2, radius=-0.3, color=cmap_red[1],
    fill_head=True, head_width=1.85, zorder=10
)

# text for Last reported case of polio in 2011 Howrah, West Bengal
ax_text(
    s="<Last> reported case\nof <wild Polio> in\n<Howrah>, <West Bengal>\nin year <2011>",
    x=2008, y=9500, font=gbp_reg, size=11, ha="right",
    highlight_textprops=[
        dict(font=gbp_b, size=11, color=cmap_red[1]),
        dict(font=gbp_b, size=11, color=cmap_red[1]),
        dict(font=gbp_b, size=11, color=cmap_red[1]),
        dict(font=gbp_b, size=11, color=cmap_red[1]),
        dict(font=gbp_b, size=11, color=cmap_red[1])
    ], ax=ax2)

# image for west bengal
image_wb = mpimg.imread(r"D:\Learning\Data Visualization\data\india\polio\images\india_wb.jpg")
img_wb = OffsetImage(image_wb, zoom=0.09)
# position (x, y) in data coordinates
position_wb = (2005.16, 15500)
ab_wb = AnnotationBbox(img_wb, position_wb, xycoords='data', frameon=False)
# Add to the plot
ax2.add_artist(ab_wb)

# Highlight 3: India declared polio-free by WHO in 2014

dot_polio_free = patches.Ellipse(
  xy=(2014, 0),
  width=0.3, height=800,
  alpha=1,
  facecolor=cmap_red[2],
  edgecolor=cmap_red[0],
  linewidth=0.5, zorder=5
)
ax2.add_patch(dot_polio_free)

# arrow for India declared polio-free by WHO in 2014
ax_arrow(
    head_position=[2014, 0],
    tail_position=[2016.5, 7000],
    ax=ax2, radius=0.3, color=cmap_red[1],
    fill_head=True, head_width=1.85, zorder=10
)

# text for India declared polio-free by WHO in 2014
ax_text(
    s="India declared\n<Polio-free><*> by <WHO><*>\non <27 March 2014>",
    x=2016.7, y=9500, font=gbp_reg, size=11, ha="left",
    highlight_textprops=[
        dict(font=gbp_b, size=11, color=cmap_red[1]),
        dict(font=gbp_reg, size=6, color=cmap_red[0]),
        dict(font=gbp_b, size=11, color=cmap_red[1]),
        dict(font=gbp_reg, size=6, color=cmap_red[0]),
        dict(font=gbp_b, size=11, color=cmap_red[1])
    ], ax=ax2)

# image for WHO logo
image_who = mpimg.imread(r"D:\Learning\Data Visualization\data\india\polio\images\who_logo.jpg")
img_who = OffsetImage(image_who, zoom=0.073)
# position (x, y) in data coordinates
position_who = (2018.25, 13900)
ab_who = AnnotationBbox(img_who, position_who, xycoords='data', frameon=False)
# Add to the plot
ax2.add_artist(ab_who)

# * Mark definitions
fig_text(
    x=0.084, y=0.035,
    s="*WHO: World Health Organisation (a inter-governmental specialized agency of the United Nations)",
    font=gbp_i, size=7, color=cmap_blue[0], ha="left"
)
fig_text(
    x=0.084, y=0.025,
    s="*Polio-free: Zero reported cases for three consecutive years",
    font=gbp_i, size=7, color=cmap_blue[0], ha="left"
)

#########################################################

# display & save
plt.savefig(r"D:\Learning\Data Visualization\data\india\polio\viz\polio.jpeg", dpi=250, bbox_inches="tight")
# plt.show()