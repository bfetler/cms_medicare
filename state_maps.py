# make state maps from input data
# use Basemap

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon

from plot_methods import make_plotdir

def get_full_states():
    "add full state names, needed by basemap shapefile"
    states = {
        'Alaska':         {'abbr':'AK'},
        'Alabama':        {'abbr':'AL'},
        'Arkansas':       {'abbr':'AR'},
        'Arizona':        {'abbr':'AZ'},
        'California':     {'abbr':'CA'},
        'Colorado':       {'abbr':'CO'},
        'Connecticut':    {'abbr':'CT'},
        'District of Columbia': {'abbr':'DC'},
        'Delaware':       {'abbr':'DE'},
        'Florida':        {'abbr':'FL'},
        'Georgia':        {'abbr':'GA'},
        'Hawaii':         {'abbr':'HI'},
        'Iowa':           {'abbr':'IA'},
        'Idaho':          {'abbr':'ID'},
        'Illinois':       {'abbr':'IL'},
        'Indiana':        {'abbr':'IN'},
        'Kansas':         {'abbr':'KS'},
        'Kentucky':       {'abbr':'KY'},
        'Louisiana':      {'abbr':'LA'},
        'Massachusetts':  {'abbr':'MA'},
        'Maryland':       {'abbr':'MD'},
        'Maine':          {'abbr':'ME'},
        'Michigan':       {'abbr':'MI'},
        'Minnesota':      {'abbr':'MN'},
        'Missouri':       {'abbr':'MO'},
        'Mississippi':    {'abbr':'MS'},
        'Montana':        {'abbr':'MT'},
        'North Carolina': {'abbr':'NC'},
        'North Dakota':   {'abbr':'ND'},
        'Nebraska':       {'abbr':'NE'},
        'New Hampshire':  {'abbr':'NH'},
        'New Jersey':     {'abbr':'NJ'},
        'New Mexico':     {'abbr':'NM'},
        'Nevada':         {'abbr':'NV'},
        'New York':       {'abbr':'NY'},
        'Ohio':           {'abbr':'OH'},
        'Oklahoma':       {'abbr':'OK'},
        'Oregon':         {'abbr':'OR'},
        'Pennsylvania':   {'abbr':'PA'},
        'Rhode Island':   {'abbr':'RI'},
        'South Carolina': {'abbr':'SC'},
        'South Dakota':   {'abbr':'SD'},
        'Tennessee':      {'abbr':'TN'},
        'Texas':          {'abbr':'TX'},
        'Utah':           {'abbr':'UT'},
        'Virginia':       {'abbr':'VA'},
        'Vermont':        {'abbr':'VT'},
        'Washington':     {'abbr':'WA'},
        'Wisconsin':      {'abbr':'WI'},
        'West Virginia':  {'abbr':'WV'},
        'Wyoming':        {'abbr':'WY'}
    }
    return states

# call this once from cms_explore, rather than for each plot, faster
def get_basemap():
# Lambert Conformal map of lower 48 states
    m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
            projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
    shp_info = m.readshapefile('maps/st99_d00','states',drawbounds=True)
#   print(shp_info)
    return m

def set_colors(df, states, mmin, mmax):
    "set colors for each state"
    cmap = plt.cm.plasma
#   cmap = plt.cm.hot
#   cmap = plt.cm.coolwarm
    for state,val in states.items():
        dval = df.ix[states[state]['abbr']]
        states[state]['color'] = rgb2hex(cmap(1.0 - np.sqrt((dval-mmin)/(mmax-mmin)))[:3])
    return states

def plot_map(m, states, plotdir, fname, label):
    "plot states map"
    plt.clf()
    f = plt.figure()
    ax = f.add_subplot(111)
    for shapedict, seg in zip(m.states_info, m.states):
        statename = shapedict['NAME']
        if statename not in ['Puerto Rico']:
            color = states[statename]['color']
            poly = Polygon(seg,facecolor=color,edgecolor=color)
            ax.add_patch(poly)
    m.drawparallels(range(25,65,20),labels=[1,0,0,0])
    m.drawmeridians(range(-120,-40,20),labels=[0,0,0,1])
    plt.title(label)
    pname = '%smap_%s.png' % (plotdir, fname)
    plt.savefig(pname)
    print('saved plot %s' % pname)

def make_state_map(df, mmin, mmax, plotdir, fname, label):
    "make state map from data frame"
    print('make state map: %s' % label)
    print('WY\n', df.ix['WY'], type(df))
    m = get_basemap()
    print(m.states_info[0].keys())
    states = get_full_states()
    states = set_colors(df, states, mmin, mmax)
    print('states', states)
    plot_map(m, states, plotdir, fname, label)


