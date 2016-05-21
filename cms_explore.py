
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
#	avg beneficiary_average_age, Beneficiary_Average_Risk_Score
#	group beneficiaries by disease percent

def print_select_columns(df):
    "try to find interesting columns"
#   new_cols = [ 'provider_type','nppes_provider_gender','nppes_provider_state','total_services','total_unique_benes','total_med_services','total_med_unique_benes','total_submitted_chrg_amt','total_medicare_payment_amt','total_med_submitted_chrg_amt','total_med_medicare_payment_amt','beneficiary_average_age','Beneficiary_Average_Risk_Score' ]
#    as I suspected, the following columns appear to be near duplicates:
#       total_med_services, total_services
#       total_med_unique_benes, total_unique_benes
#       total_med_submitted_chrg_amt, total_submitted_chrg_amt
#	total_med_medicare_payment_amt, total_medicare_payment_amt

    new_cols = [ 'provider_type','nppes_provider_gender','nppes_provider_state','total_services','total_unique_benes','total_submitted_chrg_amt','total_medicare_payment_amt','total_drug_services','total_drug_unique_benes','total_drug_submitted_chrg_amt','total_drug_medicare_payment_amt','beneficiary_average_age','Beneficiary_Average_Risk_Score','beneficiary_female_count','beneficiary_male_count','beneficiary_cc_cancer_percent' ]
    print("new columns len=%d\n%s" % (len(new_cols), new_cols))
    print(df[new_cols])

def print_all_columns(df):
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
    iterf = pd.read_csv(fname, sep=None, engine='python', iterator=True, chunksize=100000)
    print("iterf", str(type(iterf)))
    df = pd.concat(chunk for chunk in iterf)
    print("%s shape %s" % (fname, df.shape))
#   d1 = next(iterf)
#   print("d1", str(type(d1)))

def main():
    df = read_raw_data('data/head.txt')
#   read_first_data('data/head.txt')
#   print_all_columns(df)
    print_select_columns(df)

if __name__ == '__main__':
    main()

