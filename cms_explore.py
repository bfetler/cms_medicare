# explore center for medicare services (CMS) data

import os, sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# to do:
#    hist plots of each provider_type for key variables (normal dist?)

# interesting questions:
#    group_by provider_type, find:
#	avg std total_submitted_chrg_amt / total_services
#	avg std total_medicare_payment_amt / total_services
#	drug vs. other benefits
#	avg beneficiary_average_age, Beneficiary_Average_Risk_Score
#	group beneficiaries by disease percent
#	group_by provider_state, provider_gender

def make_plotdir(plotdir='cms_hist_plots/'):
    "make plot directory on file system"
    if not os.access(plotdir, os.F_OK):
        os.mkdir(plotdir)
    sns.set_style("darkgrid")
    return plotdir

def read_first_data(fname, size=10):
    "read first N=size rows from csv file fname"
    iterf = pd.read_csv(fname, sep=None, engine='python', iterator=True, chunksize=size)
    iterp = iter(iterf)
    df = next(iterp)
    print("%s shape %s" % (fname, df.shape))
    return df

def get_select_columns():
    "try to select interesting columns, rather than all 70"
    ''' the following columns appear to be near duplicates,
        except more NA's in 2nd column:
          total_services              total_med_services
          total_unique_benes          total_med_unique_benes
          total_submitted_chrg_amt    total_med_submitted_chrg_amt
 	  total_medicare_payment_amt  total_med_medicare_payment_amt
    '''
    new_cols = [ 'provider_type','nppes_provider_gender','nppes_provider_state','total_services','total_unique_benes','total_submitted_chrg_amt','total_medicare_payment_amt','beneficiary_average_age','Beneficiary_Average_Risk_Score' ]
    return new_cols

def print_select_columns(df, new_cols, size=10):
    "print subset of columns"
    print("select columns \n%s" % df[new_cols][:size])

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

def make_hist_plot(df, column_names):
    "make histogram plot of whole data frame"
# works but mostly illegible
    plotdir = make_plotdir()
    plt.clf()
    df.hist(column=column_names, by='provider_type', layout=(10,10), figsize=(40,40))
    plt.tick_params(labelbottom='off', labelleft='off')
    plt.savefig(plotdir + 'hist.png')

def make_hist_plots(df, column_name, group_var, plotdir=make_plotdir(), split_var=None):
    "make histogram plot of data frame subsets by group variable"
#   plotdir = make_plotdir()
    col_name = column_name     # for now
    providers = sorted(list(set(df[group_var])))
    print('plotting histograms')
    gx = getn(providers, 12)
    for k, v in enumerate(gx):
        print('.', end='', flush=True)
        plot_hists(df, v, 'group%s' % (k+1), col_name, group_var, plotdir, split_var=split_var)
    print(' done plotting histograms')
# e.g. make_hist_plots(df, 'pay_per_service', 'provider_type')

def plot_hists(df, vlist, label, col_name, group_var, plotdir, ncols=3, split_var=None):
    plt.clf()
    fig = plt.figure(figsize=(10,8))
    if split_var:    # e.g. nppes_provider_gender
        splits = sorted(list(set(df[split_var])))
        splits.reverse()
#       print('splits', splits)
        colors = ['green','blue','red']   # need alpha transparency
# reverse colors, plot F last, may show on top of M?  count(M) > count(F)
        aligns = ['left','right','mid']  # not always correct?  need more pixels?
    nrows = len(vlist) // ncols
    if len(vlist) % ncols > 0:
        nrows += 1
    for k, val in enumerate(vlist):
        ax = fig.add_subplot(nrows, ncols, k+1)
        if split_var:
#            for j,s in enumerate(splits):
##               ax.hist(df[(df[group_var]==val) & (df[split_var]==s)][col_name], bins=30, color=colors[j], alpha=0.4)
#                ax.hist(df[(df[group_var]==val) & (df[split_var]==s)][col_name], bins=20, rwidth=0.5, align=aligns[j])  # use seaborn colors
            hdata = []
            for s in splits:
                hpart = df[(df[group_var]==val) & (df[split_var]==s)][col_name]
#               print(s, hpart.size, sep=' ', end='')
#               if hpart.size > 0:
#                   hdata.append(np.array(hpart))
                hdata.append(df[(df[group_var]==val) & (df[split_var]==s)][col_name])
            ax.hist(hdata, bins=20)
#           print('', flush=True)
        else:
            ax.hist(df[df[group_var]==val][col_name], bins=30)
        ax.set_title(val, fontsize=10)
        ax.tick_params(labelbottom='on', labelleft='on', labelsize=7)
    plt.tight_layout()
    plt.subplots_adjust(top=0.88)
    if split_var:
        plt.suptitle('CMS %s histograms by %s and %s' % (col_name, group_var, split_var[-6:]), fontsize=12)
        plt.savefig('%shist_%s_%s_%s.png' % (plotdir, split_var[-6:], col_name, label))
    else:
        plt.suptitle('CMS %s histograms by %s' % (col_name, group_var), fontsize=12)
        plt.savefig('%shist_%s_%s.png' % (plotdir, col_name, label))

def read_select_data(new_cols, fname, first=False):
    "read new_cols from csv file fname and groupby provider_type"
    chunksize = 50000
    iterf = pd.read_csv(fname, sep=None, engine='python', iterator=True, chunksize=chunksize)
    df = pd.DataFrame()
    print('reading data ', end='', flush=True)
    if (first):      # get one line for testing
        df = iterf.get_chunk(size=chunksize)
        df = df[new_cols]
    else:            # loop through all data
        for chunk in iterf:
            print('.', end='', flush=True)   # print during long read
            df = df.append(chunk[new_cols])

    print(" done")
#   shape (986677, 9)
    print("df columns isnull sum\n%s" % df.isnull().sum())
#   nppes_provider_gender  61330, others 0
    print("df columns iszero sum\n%s" % (df==0).sum())
#   total_medicare_payment_amt 3, others 0,remove zeroes
    df = df[df.total_medicare_payment_amt != 0]

#   convert gender nan to 'nan'
    df['nppes_provider_gender'] = df['nppes_provider_gender'].apply(lambda s: str(s))
    genders = sorted(list(set(df['nppes_provider_gender'])))
    print("df gender set %s" % genders)
#   print("df gender count %s" % df.groupby('nppes_provider_gender').count())
#       ['F', 'M' 'nan'] count (18721, 28116, 3162) in 1st 50000

# calc new columns, log of quotient = log($) - log(population)
    df['pay_per_service'] = np.log10(df['total_medicare_payment_amt'] / df['total_services'])
    df['pay_per_person'] = np.log10(df['total_medicare_payment_amt'] / df['total_unique_benes'])
#   df['overcharge_ratio'] = df['total_submitted_chrg_amt'] / df['total_medicare_payment_amt']
    print("df %s shape, filename %s" % (df.shape, fname))
#   shape (986674, 11)

    provider_group = df.groupby('provider_type').median()
#   provider_group = df.groupby('provider_type').agg(['count','mean','std','median','mad'])
    provider_gender_group = df.groupby(['provider_type','nppes_provider_gender']).count()
    print_all_rows(provider_gender_group, ['pay_per_person'])
# a count of provider_type, gender - very few F in many specialties

# hist plots very varied, log scale may not help
#   make_hist_plots(df, 'pay_per_service', 'provider_type')
#   make_hist_plots(df, 'pay_per_person', 'provider_type')
    make_hist_plots(df, 'pay_per_person', 'provider_type', plotdir=make_plotdir('cms_hist_gender_plots/'), split_var='nppes_provider_gender')
# one obvious thing from plot it seems many provider_types have only one gender

    return provider_group

def filter_group_by_var(provider_group, var='pay_per_person'):
    "filter grouped data by variable var"
    provider_sort = provider_group.sort_values(by=var, ascending=False)
    print('\ntop median %s' % var)
    print_all_rows(provider_sort, ['pay_per_service','pay_per_person'])
        # add ['overcharge_ratio','total_medicare_payment_amt']

def explore_initial_data(fname, new_cols):
    "explore initial data columns"
    df = read_first_data(fname)  # first 10 rows
    print_all_columns(df)
    print_select_columns(df, new_cols)

def main():
    fname = 'data/Medicare_Physician_and_Other_Supplier_NPI_Aggregate_CY2014.txt'
    new_cols = get_select_columns()
#   explore_initial_data(fname, new_cols)

# group and filter data by provider_type mean
    if len(sys.argv) > 1 and (sys.argv[1][0]=='t' or sys.argv[1][0]=='1'):
        provider_group = read_select_data(new_cols, fname, first=True)  # 1st block
    else:
        provider_group = read_select_data(new_cols, fname)
#   filter_group_by_var(provider_group, var='pay_per_service')
#   filter_group_by_var(provider_group, var='pay_per_person')

if __name__ == '__main__':
    main()


