# calc zip groups from input dataframe

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

def set_colors(df, states, minmax=None):
    "set colors for each state"
    cmap = plt.cm.plasma
# issue for rare providers: state may not be in df.ix
    if minmax:
        mmin = minmax[0]
        mmax = minmax[1]
    else:
        mmin, mmax = (0.95*df.min(), 1.05*df.max())
        mmed = df.median()
        mdiff = max(mmax-mmed, mmed-mmin)
        mmin, mmax = mmed - mdiff, mmed + mdiff
    print('min max med', mmin, mmax, mmed)

def state_nn(im_group):
    "state nearest neighbors"
    df = im_group['median']
    dfwt = im_group['count']   # use 'count' as weight
#   WY = avg(MT, ID, UT, CO, NE, SD)  nearest states
    dfc = im_group['medwt'] = im_group['median'] * im_group['count']
    print(im_group)
    wy = ( df['MT'] + df['ID'] + df['UT'] + df['CO'] + df['NE'] + df['SD'] ) / 6.0
    pop = ( dfwt['MT'] + dfwt['ID'] + dfwt['UT'] + dfwt['CO'] + dfwt['NE'] + dfwt['SD'] )
    wypop = ( df['MT'] * dfwt['MT'] + df['ID'] * dfwt['ID'] + df['UT'] * dfwt['UT'] + df['CO'] * dfwt['CO'] + df['NE'] * dfwt['NE'] + df['SD'] * dfwt['SD'] ) / pop
    wypop2 = ( dfc['MT'] + dfc['ID'] + dfc['UT'] + dfc['CO'] + dfc['NE'] + dfc['SD'] ) / pop
    print('WY', wy, wypop, wypop2)
# note 'count' is count of providers, not patients

# to do:
#    get zipcode w/ median cost, patient pop(?), create maps
#    truncate zip to 5 digits (it's really unordered categorical)
#    predict cost by zip as continuous var, see it fail

#    get zipcode w/ lat/long
#    predict cost by lat/long as continuous var, see if it may work

#    create kdtree w/ zip lat/long, cost, pop(?)
#    find kNN of new lat/long for prediction

#    calc cost category, high/medium/low
#    split train/test by zip, predict cost category

def calc_zip_group(im_group, label):
    "calc zip group from data frame"
    print('calc zip group: %s' % label)
#   states = get_full_states()
    state_nn(im_group)


