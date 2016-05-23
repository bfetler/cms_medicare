
# explore center for medicare services data (CMS)

import pandas as pd

# to do:
#    print top 20 pay_per_service, pay_per_person,
#       total_payment_amt, overcharge_ratio
#       groupby provider_type (and state?)
#    clean up

def read_raw_data(fname):
#   change to read only 1st ten rows of any file
    df = pd.read_csv(fname, sep=None, engine='python')
    print("%s shape %s" % (fname, df.shape))
    print("df columns\n%s" % df.columns)
    return df

# interesting questions:
#    group_by provider_type, find:
#	avg std total_submitted_chrg_amt / total_services
#	avg std total_medicare_payment_amt / total_services
#	drug vs. other benefits
#	avg beneficiary_average_age, Beneficiary_Average_Risk_Score
#	group beneficiaries by disease percent
#	group_by provider_state, provider_gender
#   how to deal with NA's?

# not used, since it requires copy of large dataframe
def calc_new_columns(df):
    dfc = df.copy()
#   new_cols = [ 'provider_type','nppes_provider_gender','nppes_provider_state','total_services','total_unique_benes','total_submitted_chrg_amt','total_medicare_payment_amt','beneficiary_average_age','Beneficiary_Average_Risk_Score' ]
    dfc['overcharge_ratio'] = dfc['total_submitted_chrg_amt'] / dfc['total_medicare_payment_amt']
    dfc['charge_per_service'] = dfc['total_submitted_chrg_amt'] / dfc['total_services']
    dfc['charge_per_person'] = dfc['total_submitted_chrg_amt'] / dfc['total_unique_benes']
    dfc['pay_per_service'] = dfc['total_medicare_payment_amt'] / dfc['total_services']
    dfc['pay_per_person'] = dfc['total_medicare_payment_amt'] / dfc['total_unique_benes']
    return dfc

def get_select_columns():
    "try to select interesting columns, rather than all 70"
#   new_cols = [ 'provider_type','nppes_provider_gender','nppes_provider_state','total_services','total_unique_benes','total_med_services','total_med_unique_benes','total_submitted_chrg_amt','total_medicare_payment_amt','total_med_submitted_chrg_amt','total_med_medicare_payment_amt','beneficiary_average_age','Beneficiary_Average_Risk_Score' ]
#   the following columns appear to be near duplicates,
#      except more NA's in 1st column:
#         total_med_services, total_services
#         total_med_unique_benes, total_unique_benes
#         total_med_submitted_chrg_amt, total_submitted_chrg_amt
#	  total_med_medicare_payment_amt, total_medicare_payment_amt

#   new_cols = [ 'provider_type','nppes_provider_gender','nppes_provider_state','total_services','total_unique_benes','total_submitted_chrg_amt','total_medicare_payment_amt','total_drug_services','total_drug_unique_benes','total_drug_submitted_chrg_amt','total_drug_medicare_payment_amt','beneficiary_average_age','Beneficiary_Average_Risk_Score','beneficiary_female_count','beneficiary_male_count','beneficiary_cc_cancer_percent' ]
    new_cols = [ 'provider_type','nppes_provider_gender','nppes_provider_state','total_services','total_unique_benes','total_submitted_chrg_amt','total_medicare_payment_amt','beneficiary_average_age','Beneficiary_Average_Risk_Score' ]
#   print("new columns len=%d\n%s" % (len(new_cols), new_cols))
    return new_cols

def print_select_columns(df, new_cols):
    "print subset of columns"
    df = calc_new_columns(df[new_cols])
#   print(df[new_cols])
    print("select columns \n%s" % df)

def print_all_columns(df):
    "divide columns into sensible groups and print"
    nppes_col = [ m for m in list(df.columns) if m.startswith('nppes') ]
    nppes_col.insert(0, 'npi')   # just an index
    nppes_col.extend(['provider_type','medicare_participation_indicator'])
    # 15 columns
    print("nppes columns len=%d\n%s" % (len(nppes_col), nppes_col))   # zip contains 9 digits sometimes
    df['nppes_provider_zip'] = df['nppes_provider_zip'].map(lambda s: int(str(s)[:5]))
    print(df[nppes_col])

    total_col = [ m for m in list(df.columns) if m.startswith('total') ]
    # 23 columns
    print("total columns len=%d\n%s" % (len(total_col), total_col))
    print(df[total_col])

    number_col = [ m for m in list(df.columns) if m.startswith('number') or m.endswith('suppress_indicator') ]
    # 18 columns
    print("number columns len=%d\n%s" % (len(number_col), number_col))
    print(df[number_col])

    bene_count = [ m for m in list(df.columns) if m.startswith('bene') and m.endswith('count') ]
    bene_count.insert(0, 'beneficiary_average_age')
    bene_count.insert(1, 'Beneficiary_Average_Risk_Score')
    # 5 columns
    print("bene_count columns len=%d\n%s" % (len(bene_count), bene_count))
    print(df[bene_count])

    bene_pct = [ m for m in list(df.columns) if m.startswith('bene') and m.endswith('percent') ]
    # 16 columns
    print("bene_pct columns len=%d\n%s" % (len(bene_pct), bene_pct))
    print(df[bene_pct])

def read_first_data(fname):
#   iterf = pd.read_csv(fname, sep=None, engine='python', iterator=True, chunksize=100000)
    iterf = pd.read_csv(fname, sep=None, engine='python', iterator=True, chunksize=5)
    print("iterf", str(type(iterf)))
#   df = pd.concat(chunk for chunk in iterf)
#   print("%s shape %s" % (fname, df.shape))
#   df = iterf.get_chunk(size=5)    # operates like next()
#   df = iterf.get_chunk(size=5)
    iterp = iter(iterf)    # has __iter__(), can use iter()
    df = next(iterp)
    df = next(iterp)
    print("df", str(type(df)), str(type(iterp)))
    print("%s shape %s" % (fname, df.shape))

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
    gx = getn(list(df.index), 20)
    for g in gx:
        print(df[column_names].ix[g])

def group_select_data(new_cols, fname, first=False):
    chunksize = 50000
    iterf = pd.read_csv(fname, sep=None, engine='python', iterator=True, chunksize=chunksize)
#   df = pd.concat(chunk[new_cols] for chunk in iterf)
    df = pd.DataFrame()
    print('reading data ', end='', flush=True)
    if (first):      # get one line for testing
        df = iterf.get_chunk(size=chunksize)
        df = df[new_cols]
    else:            # loop through all data
        for chunk in iterf:
            print('.', end='', flush=True)   # print during long read
            df = df.append(chunk[new_cols])

# calc new columns
    df['overcharge_ratio'] = df['total_submitted_chrg_amt'] / df['total_medicare_payment_amt']
    df['pay_per_service'] = df['total_medicare_payment_amt'] / df['total_services']
    df['pay_per_person'] = df['total_medicare_payment_amt'] / df['total_unique_benes']
    print("done\ndf %s shape %s" % (df.shape, fname))

    providers = list(set(df['provider_type']))
#   print('provider types: len=%d %s' % (len(providers), providers))
#   def provider_to_num(s):
#       return providers.index(s)
#   dfgroup = df.groupby('provider_type')

# describe statistics
#   dfdescribe = dfgroup.describe()
#   print('group describe type %s' % str(type(dfdescribe)))
#   print('group describe shape', dfdescribe.shape)
#   print(dfdescribe)
    print('provider types: len=%d %s' % (len(providers), providers))

    provider_mean = df.groupby('provider_type').mean()
    provider_mean = provider_mean.sort_values(by='pay_per_person', ascending=False)
    print('top mean pay per service')
#   print_all_rows(provider_mean, ['pay_per_service','pay_per_person','overcharge_ratio','total_medicare_payment_amt'])
    print_all_rows(provider_mean, ['pay_per_service','pay_per_person','overcharge_ratio'])

def main():
    df = read_raw_data('data/head.txt')
# in other words, replace read_raw_data with read_first_data()
    print_all_columns(df)
    new_cols = get_select_columns()
    print_select_columns(df, new_cols)
#   read_first_data('data/head.txt')
    group_select_data(new_cols, 'data/Medicare_Physician_and_Other_Supplier_NPI_Aggregate_CY2014.txt', first=True)

if __name__ == '__main__':
    main()

