# explore center for medicare services (CMS) data

import os, sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.feature_extraction import DictVectorizer
from nlp_process import vectorize_group

# to do:
#    hist plots of each provider_type for key variables (normal dist?)

# interesting questions:
#    group_by provider_type, find:
#	avg std total_submitted_chrg_amt / total_services
#	avg std total_medicare_payment_amt / total_services
#	avg beneficiary_average_age, Beneficiary_Average_Risk_Score
#	group beneficiaries by disease percent
#	group_by provider_state, provider_gender
#       sort by most to least expensive provider
#       find count by gender, find cost ratio by gender
#   use NLP to find word associations w/ high or low cost, e.g. surgery
#   other columns: patient_gender, age_groups vs. cost

def make_plotdir(plotdir='cms_hist_plots/'):
    "make plot directory on file system"
    if not os.access(plotdir, os.F_OK):
        os.mkdir(plotdir)
    sns.set_style("darkgrid")
    return plotdir

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

def make_hist_plots(df, column_name, group_var, plotdir=make_plotdir(), split_var=None):
    "make histogram plot of data frame subsets by group variable, with optional split variable"
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
    "plot subset of histograms"
    plt.clf()
    fig = plt.figure(figsize=(10,8))
    if split_var:    # e.g. nppes_provider_gender
        splits = sorted(list(set(df[split_var])))
        splits.reverse()
#       print('splits', splits)
        colors = ['blue','green','red']   # need alpha transparency
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
#       print('df initial shape', df.shape)   # 50000 by 70
        df = df[new_cols]
    else:            # loop through all data
        for chunk in iterf:
            print('.', end='', flush=True)   # print during long read
            df = df.append(chunk[new_cols])

    print(" done")
#   shape (986677, 9)
    print("df %s shape, filename %s" % (df.shape, fname))

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
    print("df shape", df.shape)
#   shape (986674, 11)

    return df

def process_by_var(plotdir, dfgroup, col, var='nppes_provider_gender'):
    "process dataframe group by variable, usually gender"
# assumes agg_fns [count, median, mean, std] and gender [F, M, nan]
    dfg = dfgroup.unstack(level=var)[col]
    print('process group by %s' % var)
    dfg['count_fractionF'] = dfg['count']['F'] / (dfg['count']['F'] + dfg['count']['M'])
    dfg['median_FtoMdiff'] = dfg['median']['F'] / dfg['median']['M']
    dfg['median_FtoM'] = 10 ** (dfg['median']['F'] - dfg['median']['M'])
    dfg['mean_diff_ratio'] = (dfg['mean']['F'] - dfg['mean']['M']) * 2 / (dfg['std']['F'] + dfg['std']['M'])  # mean difference divided by avg std error
    print('\nprocess group by %s stat columns' % var)
    print_all_rows(dfg, ['count','median','mean','std'])
    print('\nprocess group by %s FtoM columns' % var)
    cols = ['count_fractionF','median_FtoM','mean_diff_ratio']
    print_all_rows(dfg, cols)
    print('\ntop count_fractionF')
    g_sort = filter_group_by_var(dfg, cols, stat='count_fractionF')
    make_bar_plot(get_col(g_sort,'count_fractionF'), plotdir, 'count_fraction', 'Count Fraction Female')
    g_sort = filter_group_by_var(dfg, cols, stat='median_FtoM')
    make_bar_plot(get_col(g_sort,'median_FtoM'), plotdir, 'salary_ratio', 'Salary Ratio Female / Male')
#   g_sort = filter_group_by_var(dfg, cols, stat='mean_diff_ratio')
    make_bar_plot(get_col(g_sort,'mean_diff_ratio'), plotdir, 'mean_diff', 'Mean Female - Male Salary Difference')
    make_scatter_plot(dfg['count_fractionF'], dfg['median_FtoM'], plotdir, 'salary_ratio_by_fraction', 'Female Count Fraction', 'Salary Ratio Female / Male', xlim=(0,1))
    make_scatter_plot(dfg['count']['F'], dfg['median']['F'], plotdir, 'salary_by_count', 'Female Count', 'Log Salary', xlim=(-50,3500))
    make_scatter_plot(dfg['count_fractionF'], dfg['median']['F'], plotdir, 'salary_by_fraction_count', 'Female Count Fraction', 'Log Salary', xlim=(0,1))
    make_scatter_plot(dfg['count']['F'], dfg['median_FtoM'], plotdir, 'salary_ratio_by_count', 'Female Count', 'Salary Ratio Female / Male', xlim=(-50,3500))
#   make_scatter_plot(dfg['median_FtoM'], dfg['median']['F'], plotdir, 'salary_ratio_by_salary', 'Salary Ratio Female / Male', 'Log Salary')
#   print('\ntop median_FtoM')
#   g_sort = filter_group_by_var(dfg, cols, stat='median_FtoM')
# to do: plot gender columns
    return dfg[cols].dropna()

def get_col(df, col):
    "get a series from dataframe for a particular column"
    return df[col].dropna()

def make_bar_plot(ser, plotdir, fname, label):
    "make bar plot"
    plt.clf()
    f = plt.figure(figsize=(10,8))
    ax = f.add_subplot(111)
#   ax.bar(range(ser.shape[0]), ser.values)
#   ax.set_xticklabels(ser.index, rotation=90, size=6)
    ax.barh(range(ser.shape[0]), ser.values)
    ax.set_yticks(range(ser.shape[0]))
    ax.set_yticklabels(ser.index, size=6)
    ax.set_ylim([0, ser.shape[0]])
    plt.title(label)
    plt.tight_layout()
#   plt.subplots_adjust(top=0.88)
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

def filter_group_by_var(p_group, agg_fns, stat='median'):
    "filter grouped data by variable var, sort by stat"
    print('filter_group_by_vars', stat)
    p_sort = p_group.sort_values(by=stat, ascending=False)
    print_all_rows(p_sort, agg_fns)
    return p_sort

def calc_par_group(df, agg_fns, pars, cols):
    "aggregate function grouped by provider_type or gender"
    par_group = df.groupby(pars)[cols].agg(agg_fns)
    print('alphabetical group by %s, %s stats' % (pars, cols))
    print_all_rows(par_group, cols)
    return par_group

def calc_par_groups(df):
    "calculate series of grouped parameters, printed by column"
    plotdir = make_plotdir(plotdir='cms_gender_plots/')
    agg_fns = ['count','median','mean','std']
    p_group = calc_par_group(df, agg_fns, ['provider_type'], ['pay_per_person','pay_per_service'])
#   vectorize_group(p_group['pay_per_service'])

    print('\ntop pay_per_service')
    filter_group_by_var(p_group['pay_per_service'], agg_fns, stat='median')
    print('\ntop pay_per_person')
    filter_group_by_var(p_group['pay_per_person'], agg_fns, stat='median')
    g_group = calc_par_group(df, agg_fns, ['provider_type','nppes_provider_gender'], ['pay_per_person'])
    g_group = process_by_var(plotdir, g_group, col='pay_per_person', var='nppes_provider_gender')

def main():
    fname = 'data/Medicare_Physician_and_Other_Supplier_NPI_Aggregate_CY2014.txt'
    new_cols = get_select_columns()

# group and filter data by provider_type mean
    if len(sys.argv) > 1 and sys.argv[1].startswith('test'):
        df = read_select_data(new_cols, fname, first=True)  # 1st block
    else:
        df = read_select_data(new_cols, fname)

# hist plots very varied, log scale doesn't always help
#   make_hist_plots(df, 'pay_per_service', 'provider_type')
#   make_hist_plots(df, 'pay_per_person', 'provider_type')
#   make_hist_plots(df, 'pay_per_person', 'provider_type', plotdir=make_plotdir('cms_hist_gender_plots/'), split_var='nppes_provider_gender')
# many provider_types have only one gender, nan

    calc_par_groups(df)

if __name__ == '__main__':
    main()

