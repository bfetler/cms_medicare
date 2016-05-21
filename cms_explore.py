
# explore cms data (center for medicare services data)

import pandas as pd

def read_raw_data(fname):
    df = pd.read_csv(fname, sep=None, engine='python')
#   df = pd.read_csv(fname, delim_whitespace=True)
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

def calc_new_columns(df):
    dfc = df.copy()
#   new_cols = [ 'provider_type','nppes_provider_gender','nppes_provider_state','total_services','total_unique_benes','total_submitted_chrg_amt','total_medicare_payment_amt','beneficiary_average_age','Beneficiary_Average_Risk_Score' ]
    dfc['overcharge_ratio'] = dfc['total_submitted_chrg_amt'] / dfc['total_medicare_payment_amt']
    dfc['charge_per_service'] = dfc['total_submitted_chrg_amt'] / dfc['total_services']
    dfc['charge_per_person'] = dfc['total_submitted_chrg_amt'] / dfc['total_unique_benes']
    dfc['pay_per_service'] = dfc['total_medicare_payment_amt'] / dfc['total_services']
    dfc['pay_per_person'] = dfc['total_medicare_payment_amt'] / dfc['total_unique_benes']
    return dfc

def print_select_columns(df):
    "try to find interesting columns"
#   new_cols = [ 'provider_type','nppes_provider_gender','nppes_provider_state','total_services','total_unique_benes','total_med_services','total_med_unique_benes','total_submitted_chrg_amt','total_medicare_payment_amt','total_med_submitted_chrg_amt','total_med_medicare_payment_amt','beneficiary_average_age','Beneficiary_Average_Risk_Score' ]
#    as I suspected, the following columns appear to be near duplicates:
#       total_med_services, total_services
#       total_med_unique_benes, total_unique_benes
#       total_med_submitted_chrg_amt, total_submitted_chrg_amt
#	total_med_medicare_payment_amt, total_medicare_payment_amt

#   new_cols = [ 'provider_type','nppes_provider_gender','nppes_provider_state','total_services','total_unique_benes','total_submitted_chrg_amt','total_medicare_payment_amt','total_drug_services','total_drug_unique_benes','total_drug_submitted_chrg_amt','total_drug_medicare_payment_amt','beneficiary_average_age','Beneficiary_Average_Risk_Score','beneficiary_female_count','beneficiary_male_count','beneficiary_cc_cancer_percent' ]
    new_cols = [ 'provider_type','nppes_provider_gender','nppes_provider_state','total_services','total_unique_benes','total_submitted_chrg_amt','total_medicare_payment_amt','beneficiary_average_age','Beneficiary_Average_Risk_Score' ]
    print("new columns len=%d\n%s" % (len(new_cols), new_cols))
    df = calc_new_columns(df[new_cols])
#   print(df[new_cols])
    print(df)
    return new_cols

def print_all_columns(df):
    "divide columns into sensible groups and print"
    nppes_col = [ m for m in list(df.columns) if m.startswith('nppes') ]
#   nppes_col.insert(0, 'npi')   # just an index
    nppes_col.extend(['provider_type','medicare_participation_indicator'])
    # 14 columns
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
#   bene_count.extend(['beneficiary_average_age','Beneficiary_Average_Risk_Score'])
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

def getn(o1, n=3):
    i=0
    while i<len(o1):
        ar = []
        ar.append(o1[i])
        i += 1
        while i % n != 0:
            if i<len(o1):
                ar.append(o1[i])
                i += 1
            else:
                break
        yield ar

def read_select_data(new_cols, fname):
    iterf = pd.read_csv(fname, sep=None, engine='python', iterator=True, chunksize=50000)
#   df = pd.concat(chunk[new_cols] for chunk in iterf)
    df = pd.DataFrame()
    for chunk in iterf:
        print('.', end='', flush=True)   # print to show it does something
        df = df.append(chunk[new_cols])
#   df = iterf.get_chunk(size=50000)     # get one line, for testing
#   df = df[new_cols]

# calc new columns
    df['overcharge_ratio'] = df['total_submitted_chrg_amt'] / df['total_medicare_payment_amt']
    df['pay_per_service'] = df['total_medicare_payment_amt'] / df['total_services']
    df['pay_per_person'] = df['total_medicare_payment_amt'] / df['total_unique_benes']
    print("\ndf type", str(type(df)))
    print("%s shape %s" % (df.shape, fname))

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
# loop to print all provider types
#   for i in range(0, len(providers), 3):
#       px = providers[i:i+3]
#       print(dfdescribe.ix[px])
    print('provider types: len=%d %s' % (len(providers), providers))

    provider_mean = df.groupby('provider_type').mean()
    provider_mean = provider_mean.sort_values(by='pay_per_service', ascending=False)
#   provider_mean = provider_mean.sort_values(by='total_medicare_payment_amt', ascending=False)
#   print(provider_mean)
#   print(provider_mean['pay_per_service'])
    print('top mean pay per service')
    prx = list(provider_mean.index)
    gprx = getn(prx, 18)
    for g in gprx:
        print(provider_mean['pay_per_service'].ix[g])

def main():
    df = read_raw_data('data/head.txt')
#   print_all_columns(df)
    new_cols = print_select_columns(df)
#   read_first_data('data/head.txt')
    read_select_data(new_cols, 'data/Medicare_Physician_and_Other_Supplier_NPI_Aggregate_CY2014.txt')

if __name__ == '__main__':
    main()

