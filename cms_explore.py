# explore center for medicare services (CMS) data

import os, sys

import numpy as np
import pandas as pd

from sklearn.feature_extraction import DictVectorizer
from nlp_process import vectorize_group

from plot_methods import make_plotdir, print_all_rows, make_hist_plots, plot_hists, \
        make_bar_plot, make_scatter_plot

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
#    use NLP to find word associations w/ high or low cost, e.g. surgery
#    other columns: patient_gender, age_groups vs. cost
#      total_medicare_payment_amt vs. total_submitted_chrg_amt
#        vs. total_med_medicare_payment_amt (may not include drugs)
#      beneficiary_average_age beneficiary_age_less_65_count beneficiary_age_65_74_count
#      beneficiary_female_count beneficiary_male_count 
# beneficiary_cc_afib_percent beneficiary_cc_cancer_percent beneficiary_cc_hypert_percent
# beneficiary_cc_strk_percent Beneficiary_Average_Risk_Score (what do abbreviations mean?)

def get_select_columns():
    "try to select interesting columns, rather than all 70"
    ''' the following columns appear to be near duplicates,
        except more NA's in 2nd column:
          total_services              total_med_services
          total_unique_benes          total_med_unique_benes
          total_submitted_chrg_amt    total_med_submitted_chrg_amt
 	  total_medicare_payment_amt  total_med_medicare_payment_amt
    '''
    new_cols = [ 'provider_type','nppes_provider_gender','nppes_provider_state','total_services','total_unique_benes','total_submitted_chrg_amt','total_medicare_payment_amt','beneficiary_average_age','Beneficiary_Average_Risk_Score', 'total_med_medicare_payment_amt', 'total_med_services','total_med_unique_benes' ]
    return new_cols

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
#	  total_medicare_payment_amt  total_med_medicare_payment_amt
    pay_diff = (df['total_medicare_payment_amt'] != df['total_med_medicare_payment_amt']).sum()
    print('pay_diff sum', pay_diff)  # it's not zero

#   total_medicare_payment_amt 3, others 0,remove zeroes
    df = df[df.total_medicare_payment_amt != 0]

#   convert gender nan to 'nan'
    df['nppes_provider_gender'] = df['nppes_provider_gender'].apply(lambda s: 'none' if type(s)==float else str(s))
    genders = sorted(list(set(df['nppes_provider_gender'])))
    print("df gender set %s" % genders)
#   print("df gender count %s" % df.groupby('nppes_provider_gender').count())
#       ['F', 'M' 'none'] count (18721, 28116, 3162) in 1st 50000

# calc new columns, log of quotient = log($) - log(population)
    df['pay_per_service'] = np.log10(df['total_medicare_payment_amt'] / df['total_services'])
    df['pay_per_person'] = np.log10(df['total_medicare_payment_amt'] / df['total_unique_benes'])
#   df['med_pay_per_service'] = np.log10(df['total_med_medicare_payment_amt'] / df['total_med_services'])
#   df['med_pay_per_person'] = np.log10(df['total_med_medicare_payment_amt'] / df['total_med_unique_benes'])
#   df['overcharge_ratio'] = df['total_submitted_chrg_amt'] / df['total_medicare_payment_amt']
    print("df shape", df.shape)
#   shape (986674, 11)

    return df

def get_col(df, col):
    "get a series from dataframe for a particular column"
    return df[col].dropna()

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
    make_bar_plot(get_col(g_sort,'median_FtoM'), plotdir, 'cost_ratio', 'Cost Ratio Female / Male')
#   g_sort = filter_group_by_var(dfg, cols, stat='mean_diff_ratio')
    make_bar_plot(get_col(g_sort,'mean_diff_ratio'), plotdir, 'mean_diff', 'Mean Female - Male Cost Difference')
    make_scatter_plot(dfg['count_fractionF'], dfg['median_FtoM'], plotdir, 'cost_ratio_by_fraction', 'Female Count Fraction', 'Cost Ratio Female / Male', xlim=(0,1))
    make_scatter_plot(dfg['count']['F'], dfg['median']['F'], plotdir, 'cost_by_count', 'Female Provider Count', 'Log10 Cost', xlim=(-1000,70000))
    make_scatter_plot(dfg['count_fractionF'], dfg['median']['F'], plotdir, 'cost_by_fraction_count', 'Female Count Fraction', 'Log10 Cost', xlim=(0,1))
    make_scatter_plot(dfg['count']['F'], dfg['median_FtoM'], plotdir, 'cost_ratio_by_count', 'Female Provider Count', 'Cost Ratio Female / Male', xlim=(-1000,70000))
#   make_scatter_plot(dfg['median_FtoM'], dfg['median']['F'], plotdir, 'cost_ratio_by_cost', 'Salary Ratio Female / Male', 'Log Salary')
#   print('\ntop median_FtoM')
#   g_sort = filter_group_by_var(dfg, cols, stat='median_FtoM')
# to do: plot gender columns
    return dfg[cols].dropna()

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
    plotdir = make_plotdir(plotdir='cms_cost_plots/')
    agg_fns = ['count','median','mean','std']
    p_group = calc_par_group(df, agg_fns, ['provider_type'], ['pay_per_person','pay_per_service'])
#   vectorize_group(p_group['pay_per_service'])

    print('\ntop pay_per_service')
    p_sort = filter_group_by_var(p_group['pay_per_service'], agg_fns, stat='median')
    make_bar_plot(get_col(p_sort,'median'), plotdir, 'pay_per_service', 'Median Log10 Pay Per Service')
    print('\ntop pay_per_person')
    p_sort = filter_group_by_var(p_group['pay_per_person'], agg_fns, stat='median')
    make_bar_plot(get_col(p_sort,'median'), plotdir, 'pay_per_person', 'Median Log10 Pay Per Person')
#   p_sort = filter_group_by_var(p_group['pay_per_person'], agg_fns, stat='count')
    make_bar_plot(get_col(p_sort,'count'), plotdir, 'pay_per_person_count', 'Count Per Specialist')
    make_scatter_plot(get_col(p_sort,'count'), get_col(p_sort,'median'), plotdir, 'pay_per_person_by_count', 'Count', 'Log10 Cost Per Person', xlim=(-1000,100000))

    plotdir = make_plotdir(plotdir='cms_gender_plots/')
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
    make_hist_plots(df, 'pay_per_person', 'provider_type', plotdir=make_plotdir('cms_hist_gender_plots/'), split_var='nppes_provider_gender')
# many provider_types have only one gender, nan

#   calc_par_groups(df)

if __name__ == '__main__':
    main()

