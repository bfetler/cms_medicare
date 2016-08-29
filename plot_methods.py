# plot and print methods

import os
import matplotlib.pyplot as plt
import seaborn as sns

def make_plotdir(plotdir='cms_hist_plots/'):
    "make plot directory on file system"
    if not os.access(plotdir, os.F_OK):
        os.mkdir(plotdir)
    sns.set_style("darkgrid")
    return plotdir

def print_all_columns(df, size=10):
    "print columns in sensible groups"
    nppes_col = [ m for m in list(df.columns) if m.startswith('nppes') ]
    nppes_col.insert(0, 'npi')   # just an index
    nppes_col.extend(['provider_type','medicare_participation_indicator'])
    # 15 columns
    print("nppes columns len=%d\n%s" % (len(nppes_col), nppes_col))   # zip contains 9 digits sometimes
    df['nppes_provider_zip'] = df['nppes_provider_zip'].map(lambda s: int(str(s)[:5]))
    print(df[nppes_col][:size])

    total_col = [ m for m in list(df.columns) if m.startswith('total') ]
    # 23 columns
    print("total columns len=%d\n%s" % (len(total_col), total_col))
    print(df[total_col][:size])

    number_col = [ m for m in list(df.columns) if m.startswith('number') or m.endswith('suppress_indicator') ]
    # 18 columns
    print("number columns len=%d\n%s" % (len(number_col), number_col))
    print(df[number_col][:size])

    bene_count = [ m for m in list(df.columns) if m.startswith('bene') and m.endswith('count') ]
    bene_count.insert(0, 'beneficiary_average_age')
    bene_count.insert(1, 'Beneficiary_Average_Risk_Score')
    # 5 columns
    print("bene_count columns len=%d\n%s" % (len(bene_count), bene_count))
    print(df[bene_count][:size])

    bene_pct = [ m for m in list(df.columns) if m.startswith('bene') and m.endswith('percent') ]
    # 16 columns
    print("bene_pct columns len=%d\n%s" % (len(bene_pct), bene_pct))
    print(df[bene_pct][:size])

def getn(o1, n=10):
    "get n rows of array o1, for print output"
    i=0
    while i<len(o1):
        ar = [o1[i]]
        i += 1
        while i % n != 0:
            if i<len(o1):
                ar.append(o1[i])
                i += 1
            else:
                break
        yield ar

def print_all_rows(df, column_names):
    "print all rows in groups of 20"
    gx = getn(list(df.index), 20)
    for g in gx:
        print(df[column_names].ix[g])

def make_group_bar_plots(df, index, columns, xlabels, stat, tlabel, plotdir):
    "make bar plot of data frame subsets by group variable"
    print('plotting bar plots')
    providers = df.index
    gx = getn(providers, 12)
    for k, v in enumerate(gx):
        print('.', end='', flush=True)
        plot_bars(df, v, 'group%s' % (k+1), index, columns, xlabels, stat, tlabel, plotdir)
    print(' done plotting bar plots')

def plot_bars(df, vlist, glabel, index, columns, xlabels, stat, tlabel, plotdir, ncols=3):
    "plot subset of bar plots"
    colors = ['#bb0000','#0000bb','#bb00bb','#00bb00']
    plt.clf()
    fig = plt.figure(figsize=(10,8))
    nrows = len(vlist) // ncols
    if len(vlist) % ncols > 0:
        nrows += 1
    for k, val in enumerate(vlist):
        ax = fig.add_subplot(nrows, ncols, k+1)
        hdata = []
        for column in columns:
            hdata.append(df[column][stat].ix[[val]].values)
        ax.bar(range(len(columns)), hdata, align='center', color=colors)
        ax.set_xticks(range(len(columns)))
        ax.set_xticklabels(xlabels, size=6)
        ylim = ax.get_ylim()
        ax.set_ylim(ylim[0], 1.2*ylim[1])
        ax.set_title(val, fontsize=10)
        ax.tick_params(labelbottom='on', labelleft='on', labelsize=7)
    plt.tight_layout()
    plt.subplots_adjust(top=0.88)
    plt.suptitle('CMS %s bar plots by %s' % (index, tlabel), fontsize=12)
    plt.savefig('%sbar_%s_%s.png' % (plotdir, index, glabel))

# def make_hist_plots(df, column_name, group_var, plotdir=make_plotdir(), split_var=None):
def make_hist_plots(df, column_name, group_var, plotdir, split_var=None):
    "make histogram plot of data frame subsets by group variable, with optional split variable"
    col_name = column_name     # for now
    providers = sorted(list(set(df[group_var])))
    print('plotting histograms')
    gx = getn(providers, 12)
    for k, v in enumerate(gx):
        print('.', end='', flush=True)
        plot_hists(df, v, 'group%s' % (k+1), col_name, group_var, plotdir, split_var=split_var)
    print(' done plotting histograms')

def plot_hists(df, vlist, label, col_name, group_var, plotdir, ncols=3, split_var=None):
    "plot subset of histograms"
    plt.clf()
    fig = plt.figure(figsize=(10,8))
    if split_var:    # e.g. nppes_provider_gender
        splits = sorted(list(set(df[split_var])))
        splits.reverse()
    nrows = len(vlist) // ncols
    if len(vlist) % ncols > 0:
        nrows += 1
    for k, val in enumerate(vlist):
        ax = fig.add_subplot(nrows, ncols, k+1)
        if split_var:
            hdata = []
            for s in splits:
                hdata.append(df[(df[group_var]==val) & (df[split_var]==s)][col_name])
            ax.hist(hdata, bins=20)
        else:
            ax.hist(df[df[group_var]==val][col_name], bins=30)
        ax.set_title(val, fontsize=10)
        ax.tick_params(labelbottom='on', labelleft='on', labelsize=7)
    plt.tight_layout()
    plt.subplots_adjust(top=0.88)
    if split_var:
        ax.legend(splits, bbox_to_anchor=(1.0,5.8))  # misses last plot
        plt.suptitle('CMS %s histograms by %s and %s' % (col_name, group_var, split_var[-6:]), fontsize=12)
        plt.savefig('%shist_%s_%s_%s.png' % (plotdir, split_var[-6:], col_name, label))
    else:
        plt.suptitle('CMS %s histograms by %s' % (col_name, group_var), fontsize=12)
        plt.savefig('%shist_%s_%s.png' % (plotdir, col_name, label))

def make_bar_plot(ser, plotdir, fname, label, xlim=None):
    "make bar plot from series"
    plt.clf()
    f = plt.figure(figsize=(10,8))
    ax = f.add_subplot(111)
#   ax.bar(range(ser.shape[0]), ser.values)
#   ax.set_xticklabels(ser.index, rotation=90, size=6)
    ax.barh(range(ser.shape[0]), ser.values)
    ax.set_yticks(range(ser.shape[0]))
    ax.set_yticklabels(ser.index, size=6)
    ax.set_ylim([0, ser.shape[0]])
    if xlim:
        ax.set_xlim(xlim[0], xlim[1])
    plt.title(label)
    plt.tight_layout()
    pname = '%sbar_%s.png' % (plotdir, fname)
    plt.savefig(pname)
    print('saved plot %s' % pname)

def make_scatter_plot(xvar, yvar, plotdir, fname, xlabel, ylabel, xlim=None):
    "make scatter plot"
    plt.clf()
    f = plt.figure()
    ax = f.add_subplot(111)
    ax.scatter(xvar, yvar, linewidths=0, c='blue', alpha=0.5)
    if xlim:
        ax.set_xlim(xlim[0], xlim[1])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    pname = '%sscatter_%s.png' % (plotdir, fname)
    plt.savefig(pname)
    print('saved plot %s' % pname)


