# make state maps from input data
# use Basemap

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
#       'District of Columbia': {'abbr':'DC'},
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

def set_colors(df, states, minmax=None):
    "set colors for each state"
    cmap = plt.cm.plasma
#   cmap = plt.cm.hot
#   cmap = plt.cm.gist_heat
# issue for rare providers: state may not be in df.ix
    if minmax:
        mmin = minmax[0]
        mmax = minmax[1]
    else:
#       mmin, mmax = (df.min(), df.max())
#       mmin, mmax = (0.9*df.min(), 1.1*df.max())
        mmin, mmax = (0.95*df.min(), 1.05*df.max())
        mmed = df.median()
        mdiff = max(mmax-mmed, mmed-mmin)
        mmin, mmax = mmed - mdiff, mmed + mdiff
    print('min max med', mmin, mmax, mmed)
    for state,val in states.items():
        if states[state]['abbr'] in df.index:
            dval = df.ix[states[state]['abbr']]
            states[state]['color'] = rgb2hex(cmap(1.0 - pow((dval-mmin)/(mmax-mmin), 1.0))[:3])
        else:
            states[state]['color'] = '#FFFFFF'
    return states

def plot_map(m, states, plotdir, fname, label):
    "plot states map"
    plt.clf()
    f = plt.figure()
    ax = f.add_subplot(111)
    for shapedict, seg in zip(m.states_info, m.states):
        statename = shapedict['NAME']
        if statename not in ['District of Columbia','Puerto Rico']:
            color = states[statename]['color']
            poly = Polygon(seg,facecolor=color,edgecolor=color)
            ax.add_patch(poly)
    m.drawparallels(range(25,65,20),labels=[1,0,0,0])
    m.drawmeridians(range(-120,-40,20),labels=[0,0,0,1])
    plt.title(label)
    pname = '%smap_%s.png' % (plotdir, fname)
    plt.savefig(pname)
    print('saved plot %s' % pname)

def make_state_map(m, df, plotdir, fname, label, minmax=None):
    "make state map from data frame"
    print('make state map: %s' % label)
    states = get_full_states()
    states = set_colors(df, states, minmax)
#   print('states', states)
    plot_map(m, states, plotdir, fname, label)


