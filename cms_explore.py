# explore center for medicare services (CMS) data

import pandas as pd

# to do:
#    print top 20 pay_per_service, pay_per_person,
#       total_payment_amt, overcharge_ratio
#       groupby provider_type (and gender or state)
#    hist plots of each provider_type for key variables (normal dist?)

# interesting questions:
#    group_by provider_type, find:
#	avg std total_submitted_chrg_amt / total_services
#	avg std total_medicare_payment_amt / total_services
#	drug vs. other benefits
#	avg beneficiary_average_age, Beneficiary_Average_Risk_Score
#	group beneficiaries by disease percent
#	group_by provider_state, provider_gender
#   how to deal with NA's?

def read_first_data(fname, size=10):
    "read first N=size rows from csv file fname"
    iterf = pd.read_csv(fname, sep=None, engine='python', iterator=True, chunksize=size)
    iterp = iter(iterf)
    df = next(iterp)
    print("%s shape %s" % (fname, df.shape))
    return df

def get_select_columns():
    "try to select interesting columns, rather than all 70"
#   new_cols = [ 'provider_type','nppes_provider_gender','nppes_provider_state','total_services','total_unique_benes','total_med_services','total_med_unique_benes','total_submitted_chrg_amt','total_medicare_payment_amt','total_med_submitted_chrg_amt','total_med_medicare_payment_amt','beneficiary_average_age','Beneficiary_Average_Risk_Score' ]
#   the following columns appear to be near duplicates,
#      except more NA's in 2nd column:
#         total_services              total_med_services
#         total_unique_benes          total_med_unique_benes
#         total_submitted_chrg_amt    total_med_submitted_chrg_amt
#	  total_medicare_payment_amt  total_med_medicare_payment_amt
# add drug columns, beneficiary columns?

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
#   total_medicare_payment_amt 3, others 0
    print("df gender set %s" % list(set(df['nppes_provider_gender'])))
#       [nan, 'M', 'F']

    df = df[df.total_medicare_payment_amt != 0]

# calc new columns
    df['pay_per_service'] = df['total_medicare_payment_amt'] / df['total_services']
    df['pay_per_person'] = df['total_medicare_payment_amt'] / df['total_unique_benes']
#   df['overcharge_ratio'] = df['total_submitted_chrg_amt'] / df['total_medicare_payment_amt']
    print("df %s shape, filename %s" % (df.shape, fname))
#   shape (986674, 11)

#   providers = list(set(df['provider_type']))
#   print('provider types: len=%d %s' % (len(providers), providers))
    print_all_rows(df.groupby('provider_type').count(), ['total_services'])
    provider_group = df.groupby('provider_type').median()
#   provider_group = df.groupby('provider_type').agg(['count','mean','std','median','mad'])
#   provider_gender_group = df.groupby(['provider_type','nppes_provider_gender']).mean()
#   print_all_rows(provider_group, ['pay_per_service','pay_per_person'])

    return provider_group

def filter_group_by_var(provider_group, var='pay_per_person'):
    "filter grouped data by variable var"
    provider_sort = provider_group.sort_values(by=var, ascending=False)
    print('\ntop median %s' % var)
#   print_all_rows(provider_mean, ['pay_per_service','pay_per_person','overcharge_ratio','total_medicare_payment_amt'])
    print_all_rows(provider_sort, ['pay_per_service','pay_per_person'])

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
    provider_group = read_select_data(new_cols, fname)
#   provider_group = read_select_data(new_cols, fname, first=True)  # 1st block
    filter_group_by_var(provider_group, var='pay_per_service')
    filter_group_by_var(provider_group, var='pay_per_person')

if __name__ == '__main__':
    main()

