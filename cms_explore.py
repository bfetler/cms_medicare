# explore center for medicare services (CMS) data

import os, sys
from re import compile as re_compile

import numpy as np
import pandas as pd

# from calc_by_states import calc_by_states
from state_maps import make_state_map, get_basemap
from zip_calc import calc_zip_group

from plot_methods import make_plotdir, print_all_rows, make_hist_plots, plot_hists, \
        make_bar_plot, make_scatter_plot, make_group_bar_plots

# interesting questions:
#    group_by provider_type, find:
#	avg std total_submitted_chrg_amt / total_services
#	avg std total_medicare_payment_amt / total_services
#	avg beneficiary_average_age, Beneficiary_Average_Risk_Score
#	group beneficiaries by disease percent
#	group_by provider_state, provider_gender
#       sort by most to least expensive provider
#       find count, cost ratio by provider_gender
#       group by patient gender, patient age range
#    other columns: 
#      total_medicare_payment_amt vs. total_submitted_chrg_amt
#        vs. total_med_medicare_payment_amt (may not include drugs)

def get_select_columns():
    "try to select interesting columns, rather than all 70"
    ''' the following columns appear to be near duplicates,
        except more NA's in 2nd column:
          total_services              total_med_services
          total_unique_benes          total_med_unique_benes
          total_submitted_chrg_amt    total_med_submitted_chrg_amt
 	  total_medicare_payment_amt  total_med_medicare_payment_amt
    '''
    new_cols = [ 'provider_type','nppes_provider_gender','nppes_provider_state','nppes_provider_zip','total_services','total_unique_benes','total_submitted_chrg_amt','total_medicare_payment_amt','beneficiary_average_age','Beneficiary_Average_Risk_Score', 'total_med_medicare_payment_amt', 'total_med_services','total_drug_medicare_payment_amt','total_drug_services','beneficiary_female_count','beneficiary_male_count','beneficiary_age_less_65_count','beneficiary_age_65_74_count','beneficiary_age_75_84_count','beneficiary_age_greater_84_count' ]
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
#   shape (986677, 19)
    print("df %s shape, filename %s" % (df.shape, fname))

    print("df columns isnull sum\n%s" % df.isnull().sum())
#   nppes_provider_gender  61330, others 0
#   total_med_services, total_drug_services 5186 out of 50000
    print("df columns iszero sum\n%s" % (df==0).sum())
#   total_drug_services 32011 out of 50000

    pay_diff = (df['total_services'] != df['total_med_services']).sum()
    print('med services diff sum', pay_diff)  # 17989
    pay_diff = (df['total_medicare_payment_amt'] != df['total_med_medicare_payment_amt']).sum()
    print('med pay diff sum', pay_diff)  # 17989 out of 50000 ~ 36%
    pay_diff = (df['total_services'] != df['total_drug_services']).sum()
    print('drug services diff sum', pay_diff)  # 49995
    pay_diff = (df['total_medicare_payment_amt'] != df['total_drug_medicare_payment_amt']).sum()
    print('drug pay diff sum', pay_diff)  # 49994 out of 50000 ~ 100%

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
#   shape (986674, 21)

    return df

def get_col(df, col, log=False):
    "get a series from dataframe for a particular column, w/ option to take log of series"
    series = df[col].dropna()
    if log:
        series = np.log10(series)
    return series

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

def calc_par_group(df, agg_fns, pars, cols, print_out=True):
    "aggregate function grouped by provider_type or gender"
    par_group = df.groupby(pars)[cols].agg(agg_fns)
    if print_out:
        print('alphabetical group by %s, %s stats' % (pars, cols))
        print_all_rows(par_group, cols)
    return par_group

def average_age_par_group(df):
    "average age calc per provider type"
    df['total_age'] = df['beneficiary_average_age'] * df['total_unique_benes']
#   print(df['total_age'])
    plotdir = make_plotdir(plotdir='cms_pop_plots/')
    agg_fns = ['sum']
    p_group = calc_par_group(df, agg_fns, ['provider_type'], ['total_unique_benes','total_age'])
    p_group['avg_age'] = p_group['total_age']['sum'] / p_group['total_unique_benes']['sum']
    p_sort = p_group.sort_values(by='avg_age', ascending=False)
    print_all_rows(p_sort, ['avg_age'])
    make_bar_plot(get_col(p_sort,'avg_age'), plotdir, 'beneficiary_average_age', 'Beneficiary Average Age', xlim=(50,100))

def gender_par_groups(df):
    "calculate series of grouped gender parameters, printed by column"
    plotdir = make_plotdir(plotdir='cms_pop_gender_plots/')
    agg_fns = ['count','sum']
    pars = ['beneficiary_female_count','beneficiary_male_count']
    p_group = calc_par_group(df, agg_fns, ['provider_type'], pars)
    make_group_bar_plots(p_group, 'provider_type', pars, ['female','male'], 'sum', 'Patient Gender', plotdir)

def age_segment_par_groups(df):
    "calculate series of grouped age parameters, printed by column"
    plotdir = make_plotdir(plotdir='cms_pop_age_plots/')
    agg_fns = ['count','sum']
    pars = ['beneficiary_age_less_65_count','beneficiary_age_65_74_count','beneficiary_age_75_84_count','beneficiary_age_greater_84_count']
    p_group = calc_par_group(df, agg_fns, ['provider_type'], pars)
    labels = ['< 65','65-74','75-84','> 84']

    age_sums = [ p_group[p]['sum'].sum() for p in pars ]
    age_total = 0
    for age in age_sums:
        age_total += age
    print('\nage_range  number of patients:')
    for label,age in zip(labels, age_sums):
        print('  %5s    %d   (%.2f%%)' % (label, age, 100*age/age_total))

    make_group_bar_plots(p_group, 'provider_type', pars, labels, 'sum', 'Patient Age Group', plotdir)

def pop_calc_par_groups(df):
    "calculate series of grouped population parameters, printed by column"
    plotdir = make_plotdir(plotdir='cms_pop_plots/')
    agg_fns = ['count','sum','median']
    p_group = calc_par_group(df, agg_fns, ['provider_type'], ['total_unique_benes','total_services','beneficiary_average_age','total_medicare_payment_amt'])

    print('\ntop total_services count')  # count of number of providers, not patients
    p_sort = filter_group_by_var(p_group['total_services'], agg_fns, stat='count')
    make_bar_plot(get_col(p_sort,'count',log=True), plotdir, 'total_services_count', 'Log10 Count Total Services', xlim=(0.1,5))
    print('\ntop total_services sum')
    p_sort = filter_group_by_var(p_group['total_services'], agg_fns, stat='sum')
    make_bar_plot(get_col(p_sort,'sum',log=True), plotdir, 'total_services_sum', 'Log10 Sum Total Services', xlim=(1,9))

    print('\ntop total_unique_benes sum')
    p_sort = filter_group_by_var(p_group['total_unique_benes'], agg_fns, stat='sum')
    make_bar_plot(get_col(p_sort,'sum',log=True), plotdir, 'total_unique_benes_sum', 'Log10 Sum Total Beneficiaries', xlim=(1,8))

    print('\ntop beneficiary_average_age median')
    p_sort = filter_group_by_var(p_group['beneficiary_average_age'], agg_fns, stat='median')
    make_bar_plot(get_col(p_sort,'median'), plotdir, 'beneficiary_average_age_median', 'Median Beneficiary Age Per Provider', xlim=(50,100))

    print('\ntop total_medicare_payment_amt median')
    p_sort = filter_group_by_var(p_group['total_medicare_payment_amt'], agg_fns, stat='median')
    make_bar_plot(get_col(p_sort,'median',log=True), plotdir, 'median_medicare_payment_amt', 'Log10 Median Medicare Payment Amount Per Provider', xlim=(1,6))

    print('\ntop total_medicare_payment_amt')
    p_sort = filter_group_by_var(p_group['total_medicare_payment_amt'], agg_fns, stat='sum')
    make_bar_plot(get_col(p_sort,'sum',log=True), plotdir, 'total_medicare_payment_amt', 'Log10 Total Medicare Payment Amount', xlim=(1,10))

def pay_calc_par_groups(df):
    "calculate series of grouped pay parameters, printed by column"
    plotdir = make_plotdir(plotdir='cms_cost_plots/')
    agg_fns = ['count','median','mean','std']
    p_group = calc_par_group(df, agg_fns, ['provider_type'], ['pay_per_person','pay_per_service'])

    print('\ntop pay_per_service')
    p_sort = filter_group_by_var(p_group['pay_per_service'], agg_fns, stat='median')
    make_bar_plot(get_col(p_sort,'median'), plotdir, 'pay_per_service', 'Median Log10 Pay Per Service')
    print('\ntop pay_per_person')
    p_sort = filter_group_by_var(p_group['pay_per_person'], agg_fns, stat='median')
    make_bar_plot(get_col(p_sort,'median'), plotdir, 'pay_per_person', 'Median Log10 Pay Per Person')
#   p_sort = filter_group_by_var(p_group['pay_per_person'], agg_fns, stat='count')
    make_bar_plot(get_col(p_sort,'count'), plotdir, 'pay_per_person_count', 'Count Per Person')
    make_scatter_plot(get_col(p_sort,'count'), get_col(p_sort,'median'), plotdir, 'pay_per_person_by_count', 'Count', 'Log10 Cost Per Person', xlim=(-1000,100000))

    plotdir = make_plotdir(plotdir='cms_gender_plots/')
    g_group = calc_par_group(df, agg_fns, ['provider_type','nppes_provider_gender'], ['pay_per_person'])
    g_group = process_by_var(plotdir, g_group, col='pay_per_person', var='nppes_provider_gender')

def calc_by_states(df):
    "calc parameters by state"
    plotdir = make_plotdir(plotdir='cms_state_service_plots/')
    agg_fns = ['count','median']
    p_group = calc_par_group(df, agg_fns, ['provider_type','nppes_provider_state'], ['pay_per_person','pay_per_service'], print_out=False)
#   print('index level provider_types\n', p_group.index.levels[0])

    bmap = get_basemap()  # read file once for all maps
#   minmax = (1.0, 2.7)
#   im = p_group.ix['Internal Medicine']['pay_per_service']['median']
#   print('%s\n' % provider, im)
#   make_state_map(bmap, im, plotdir, 'cost_per_service_internal_medicine', 'Internal Medicine, Median Cost Per Service')

#   im = p_group.ix['General Surgery']['pay_per_service']['median']
#   print('%s\n' % provider, im)
#   make_state_map(bmap, im, plotdir, 'cost_per_service_general_surgery', 'General Surgery, Median Cost Per Service')

#   im = p_group.ix['Physical Therapist']['pay_per_service']['median']
#   print('%s\n' % provider, im)
#   make_state_map(bmap, im, plotdir, 'cost_per_service_physical_therapist', 'Physical Therapist, Median Cost Per Service')

    patr = re_compile('[ (/)]+')
#   for provider in p_group.index.levels[0]:
#       im = p_group.ix[provider]['pay_per_service']['median']
#       make_state_map(bmap, im, plotdir, 'cost_per_service_%s' % '_'.join(patr.split(provider.lower())), '%s, Median Cost Per Service' % provider)

    plotdir = make_plotdir(plotdir='cms_state_person_plots/')
    for provider in p_group.index.levels[0]:
        im = p_group.ix[provider]['pay_per_person']['median']
        make_state_map(bmap, im, plotdir, 'cost_per_person_%s' % '_'.join(patr.split(provider.lower())), '%s, Median Cost Per Person' % provider)

def calc_by_zip(df):
    "calc parameters by zip code"
    plotdir = make_plotdir(plotdir='cms_zip_person_plots/')

# first validate by state, as a mock of zip
    agg_fns = ['count','median']
    p_group = calc_par_group(df, agg_fns, ['provider_type','nppes_provider_state'], ['pay_per_person','pay_per_service'], print_out=False)
#   print('index level provider_types\n', p_group.index.levels[0])

#   bmap = get_basemap()  # read file once for all maps
#   im = p_group.ix['Cardiology']['pay_per_person']['median']
#   make_state_map(bmap, im, plotdir, 'zip_cardiology_per_person', '%s, Median Cost Per Person' % 'Cardiology')
#   im = p_group.ix['Cardiology']['pay_per_person']['count']
#   make_state_map(bmap, im, plotdir, 'zip_cardiology_per_person_count', '%s, Median Count Per Person' % 'Cardiology')
    im_group = p_group.ix['Cardiology']['pay_per_person']
    calc_zip_group(im_group, 'Cardiology')


def main():
    fname = 'data/Medicare_Physician_and_Other_Supplier_NPI_Aggregate_CY2014.txt'
    new_cols = get_select_columns()

# group and filter data by provider_type mean
    if len(sys.argv) > 1 and sys.argv[1].startswith('test'):
        df = read_select_data(new_cols, fname, first=True)  # 1st block
    else:
        df = read_select_data(new_cols, fname)

# hist plots very varied, log scale usually helps $ and population data
#   make_hist_plots(df, 'pay_per_service', 'provider_type', plotdir=make_plotdir())
#   make_hist_plots(df, 'pay_per_person', 'provider_type', plotdir=make_plotdir())
#   make_hist_plots(df, 'beneficiary_average_age', 'provider_type', plotdir=make_plotdir('bene_average_age_plots/'))
#   make_hist_plots(df, 'Beneficiary_Average_Risk_Score', 'provider_type', plotdir=make_plotdir('bene_risk_plots/'))
#   make_hist_plots(df, 'pay_per_person', 'provider_type', plotdir=make_plotdir('cms_hist_gender_plots/'), split_var='nppes_provider_gender')
# many facility provider_types have only one gender, none

#   pay_calc_par_groups(df)
    pop_calc_par_groups(df)
#   average_age_par_group(df)
#   gender_par_groups(df)
#   age_segment_par_groups(df)

#   calc_by_states(df)
#   calc_by_zip(df)

if __name__ == '__main__':
    main()

