import os, glob

import datetime, time
from datetime import datetime as dt

import warnings
warnings.simplefilter(action='ignore')

import numpy as np
# import matplotlib.pyplot as plt

import pandas as pd
from pandas import DataFrame
from pandas.tseries.offsets import MonthBegin

# from Scripts.dur_data_gen import generate_labels, populate_durations
HOME = os.path.expanduser("~")
WORK_DIR = os.getcwd()
DIR_PATH = os.path.join(WORK_DIR,"Data Prep\\")
SAVE = True
PREFIX = ''
SUFFIX = ''

### 

def read_gh_hist_files(path:str="./GH Alt Dataset",
                       columns:list=[],
                       ) -> DataFrame:
    if not os.path.exists(os.path.join(DIR_PATH,path)): 
        raise FileExistsError(f'Path {path} does not exist. Please check and try again')
    all_files = glob.glob(os.path.join(DIR_PATH,path,'./*.csv'))
    li = []
    for filename in all_files:
        df = pd.read_csv(filename, 
                         index_col=None, 
                         header=0, 
                         names=columns, 
                         low_memory=False,
                         )
        li.append(df)
    return pd.concat(li, axis=0, ignore_index=True)

def add_step_id(df:DataFrame,
                step_order_list:list=[],
                mapped_col:str='new_value',
                step_id_col:str='step_order',
                )-> DataFrame:
    step_order = []
    for x in df[mapped_col]:
        for count, value in enumerate(step_order_list):
            if x == value:
                step = count
                step_order.append(step)
    df[step_id_col] = step_order
    return df

def add_fsaldu(df:DataFrame,
               write_fsaldu:bool=True,
               fsaldu_path:str='applicants_by_',
               fsa_ldu:str='both',
               pc_col:str='postal_code',
               application_col:str='application_id',
               ) -> DataFrame:
    df[pc_col] = df[pc_col].str.replace(' ','')
    df['FSA'] = df[pc_col].str[:3]
    if write_fsaldu:
        write_apps_by_fsaldu(df, 
                             fsaldu_path=fsaldu_path, 
                             fsa_ldu=fsa_ldu,
                             pc_col=pc_col, 
                             application_col=application_col,
                             )
    return df

def add_date_ranks(df:DataFrame,
                   ascending:bool=True,
                   ) -> DataFrame:
    suffix = '_asc' if ascending else '_desc'
    df['rank'+suffix] = rank_dates(df,method='first',ascending=ascending)
    return df

def write_apps_by_fsaldu(df:DataFrame,
                         fsaldu_path:str='applicants_by_',
                         fsa_ldu:str='both',
                         fsa_col:str='FSA',
                         pc_col:str='postal_code',
                         application_col:str='application_id',
                         ):
    if (fsa_ldu=='fsa') or (fsa_ldu=='both'):
        fsa = df.groupby([fsa_col])[application_col].nunique()
        fsa = fsa.reset_index()
        save_csv(fsa,
                 fsaldu_path+'fsa.csv'
                 )
        # fsa.to_csv(fsaldu_path+'fsa.csv')
    if (fsa_ldu=='ldu') or (fsa_ldu=='both'):
        ldu = df.groupby([pc_col])[application_col].nunique()
        ldu = ldu.reset_index()
        save_csv(ldu,
                 fsaldu_path+'postal_code.csv'
                 )
        # ldu.to_csv(fsaldu_path+'postal_code.csv')

def create_date_df(begin_date:str,
                   units:int,
                   ) -> DataFrame:
    dim_date = pd.DataFrame({'dim_date':pd.date_range(begin_date, periods=units)})

    dim_date['dim_month'] = pd.to_datetime(dim_date['dim_date'], infer_datetime_format=True, format='mixed') - MonthBegin(1)
    
    dim_date['dim_week'] = dim_date['dim_date'].dt.to_period('W').apply(lambda r: r.start_time)
    dim_date['dim_week_number'] = dim_date['dim_week'].dt.isocalendar().week

    return dim_date

def rank_dates(df:DataFrame, 
               grpby_col:str='application_id',
               rank_col:str='edit_date',
               method:str='first',
               ascending:bool=True,
               ) -> DataFrame:
    return df.groupby(grpby_col)[rank_col].rank(method=method, ascending=ascending)

def set_first_date(df:DataFrame) -> DataFrame:
    # print(df.shape)
    df_1st_rec = df[df['rank_asc']==1]
    df_1st_rec['edit_date'] = df_1st_rec['app_created_date']
    df_1st_rec['old_value'] = 'Registration Started'
    df_1st_rec['new_value'] = 'Registration Completed'
    return df_1st_rec

def set_last_date(df:DataFrame,
                  max_edit_date:datetime.datetime=dt.today().date(),
                  ) -> DataFrame:
    df_last_rec = df[df['rank_desc']==1]
    df_last_rec['edit_date'] = max_edit_date
    df_last_rec['old_value'] = df_last_rec['new_value']
    return df_last_rec

def convert_to_datetimes(df:DataFrame,
                         columns:list=[],
                         ) -> DataFrame:
    for col in columns:
        df[col] = pd.to_datetime(df[col],infer_datetime_format=True, format='mixed')
    return df

def convert_to_datetime64(df:DataFrame,
                          cols:list=[],
                          ) -> DataFrame:
    for col in cols:
        df[col] = df[col].astype('datetime64[D]')
    return df

def convert_month_week(df:DataFrame) -> DataFrame:
    df['edit_day']      = pd.to_datetime(df['edit_date'].apply(lambda x: x.date()), infer_datetime_format=True, format='mixed')
    df['next_edit_day'] = pd.to_datetime(df['next_edit_date'].apply(lambda x: x.date()), infer_datetime_format=True, format='mixed')
    df['edit_date_month']      = df['edit_day'].dt.to_period('m').apply(lambda r: r.start_time)
    df['edit_date_week']       = df['edit_day'].dt.to_period('W').apply(lambda r: r.start_time)
    df['next_edit_date_month'] = df['next_edit_day'].dt.to_period('m').apply(lambda r: r.start_time)
    df['next_edit_date_week']  = df['next_edit_day'].dt.to_period('W').apply(lambda r: r.start_time)
    return df

def strip_date_df(df:DataFrame,
                  date_cols:list,
                  ) -> DataFrame:
    date_df = df[date_cols].copy()
    date_df = date_df.drop_duplicates()
    return date_df

def save_csv(df:DataFrame,
             path:str,
             mode:str='w',
             index:bool=True,
             header:bool=True,
             ):
    if SAVE:
        df.to_csv(os.path.join(DIR_PATH,PREFIX+path+SUFFIX), mode=mode, index=index, header=header)

def time_func(func, *args):
    start_time = time.time()
    ret = func(*args)
    total_time = time.time()-start_time
    # strptime
    # print
    return ret

#

def create_gh_hist_df(columns:list,
                      step_order_list:list,
                      begin_date:str,
                      units:int,
                      ) -> DataFrame:
    # print(f"Loading all files")
    raw_gh_df = read_gh_hist_files(columns=columns)

    if not raw_gh_df.shape[-1]==len(columns):
        raise ValueError(f'Not all columns exist in files.')
    # print(f"Converting columns to datetime")
    raw_gh_df = convert_to_datetimes(raw_gh_df, columns=['date_process_complete','app_created_date','edit_date'])
    raw_gh_df['edit_day'] = raw_gh_df['edit_date'].dt.floor('d')

    # Overwrite value of 'Created.' records
    raw_gh_df.loc[raw_gh_df['field_event']=='Created.','old_value'] = 'Registration Started' 
    raw_gh_df.loc[raw_gh_df['field_event']=='Created.','new_value'] = 'Registration Completed'
    # print(f"Adding step numbers")
    raw_gh_df = add_step_id(raw_gh_df, step_order_list)
    # print(f"Adding FSA/LDU")
    raw_gh_df = add_fsaldu(raw_gh_df, fsa_ldu='ldu')

    clean_gh_df = raw_gh_df.copy(deep=True)
    # print(f"Adding rank(s)")
    clean_gh_df = add_date_ranks(clean_gh_df)
    # print(f"Get first date per application")
    df_1st_rec = set_first_date(clean_gh_df)
    if raw_gh_df['application_id'].nunique() != df_1st_rec['application_id'].nunique():
        raise ValueError("Error in number of applicants identified, check 'set_first_date()' function.")
    clean_gh_df = pd.concat([clean_gh_df, df_1st_rec])
    clean_gh_df = add_date_ranks(clean_gh_df, ascending=False)
    # print(f"Get last date per application")
    df_last_rec = set_last_date(clean_gh_df,max_edit_date=raw_gh_df['edit_date'].max())
    if raw_gh_df['application_id'].nunique() != df_last_rec['application_id'].nunique():
        raise ValueError("Error in number of applicants identified, check 'set_last_date()' function.")
    gh_df = pd.concat([clean_gh_df, df_last_rec])

    gh_df = gh_df.sort_values(by=['application_id','edit_date'], ascending=True)
    gh_df['next_edit_date'] = gh_df.groupby(['application_id'])['edit_date'].shift(-1)
    # print(f"Convert months to weeks")
    gh_df = convert_month_week(gh_df)

    if not dt.strptime(begin_date,'%Y-%m-%d') <= dt.strptime(raw_gh_df['date_created'].min(),'%Y-%m-%d'):
        raise ValueError("Dates too small, 'begin_date' is after the minimum creation date of the dataset.")
    date_df = create_date_df(begin_date=begin_date, units=units)

    date_week_df  = strip_date_df(date_df, ['dim_week','dim_week_number'])
    date_month_df = strip_date_df(date_df, ['dim_month'])
    # print(f"Saving datasets...")
    save_csv(gh_df,        'final_dataset.csv')
    save_csv(date_week_df, 'dim_week.csv')
    save_csv(date_month_df,'dim_month.csv')

    return gh_df

def gh_prediction(path:str,
                  begin_date:str,
                  units:int,
                #   columns:list=[],
                  final_cols:list=[],
                  encoding:str='latin-1',
                  ):
    retrofit_df = pd.read_csv(os.path.join(DIR_PATH,path), encoding=encoding) 
    retrofit_df = add_fsaldu(retrofit_df, fsaldu_path='recipients_by_', fsa_ldu='ldu', pc_col='Postal Code', application_col='Application: Application#')

    retrofit_df['Retro Number'] = retrofit_df['Retrofit: Retrofit#'].str.slice(3,100)

    retrofit_df_max = retrofit_df.groupby(['Application: Application#'])['Retro Number'].max()
    retrofit_df_max = retrofit_df_max.reset_index()

    retrofit_df = retrofit_df.merge(retrofit_df_max, on='Application: Application#', how='left')
    retrofit_df = retrofit_df[retrofit_df['Retro Number_x']==retrofit_df['Retro Number_y']]

    retrofit_df['province_group'] = np.where((retrofit_df['Province']=='QC') | (retrofit_df['Province']=='NS'), 
                                             'QC/NS',
                                             'Others')
    
    retrofit_df = retrofit_df[final_cols]

    retrofit_sum_df = retrofit_df.groupby(['Date Process Complete']).sum()
    retrofit_sum_df['running_sum'] = retrofit_sum_df['Total Grant Approved'].cumsum()

    save_csv(retrofit_sum_df,'retrofit_running_sum_all_provinces.csv')

    date_df = create_date_df(begin_date, units)
    date_week_df = strip_date_df(date_df, ['dim_week', 'dim_week_number'])
    save_csv(date_week_df, 'dim_week_projection.csv')

###

if __name__=='__main__':
    update_date = input('Please input the latest date of the dataset (in the form "YYYY-MM-DD): ')
    try:
        datetime.date.fromisoformat(update_date)
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    retrofit_path = f'./GH Retrofit Dataset/Gh All Retrofits {update_date}.csv'
    try:
        assert os.path.exists(os.path.join(DIR_PATH,retrofit_path))
    except AssertionError:
        raise AssertionError(f"File does not exist, check that the path is correct and the file exists.\n{retrofit_path}")
    
    
    columns = ['date_created',
               'current_application_status',
               'is_for_pilot_project',
               'already_evaluated',
               'service_org_account_change_request',
               'inactive_reason',                    # Reason for Application Inactive',
               'incomplete_ineligible_reason',       # Reason for App Incomplete / Ineligible',
               'date_process_complete',
               'postal_code',
               'stage',
               'app_created_date',
               'application_id',
               'field_event',
               'old_value',
               'new_value',
               'edit_date',
               'application_inactive',
               'created_offline',
               'is_active_QC_NS',
               'province'
               ]
    step_order_list = ['Registration Started',
                       'Registration Completed',
                       'Eligibility Confirmed',
                       'Pre-retrofit evaluation requested',
                       'Pre-retrofit evaluation completed',
                       'Homeowner Review',
                       'Post-retrofit evaluation requested',
                       'Post-retrofit evaluation completed', 
                       'Final Homeowner Review',
                       'Receipts submitted and grant requested', 
                       'Grant to be Confirmed',
                       'Request Payment', 
                       'Process Completed',
                       ]
    begin_date = '2021-01-01'
    units = 1500 #~ 4 years
    st = time.perf_counter()
    print(f"Compiling Greener Homes data history ...")
    df = create_gh_hist_df(columns=columns,
                           step_order_list=step_order_list,
                           begin_date=begin_date,
                           units=units,
                           )
    print(f"... Complete! In {time.perf_counter() - st:0.4f} seconds")

    #

    # update_date = '2023-07-18' # make this an argument
    # retrofit_path = f'./GH Retrofit Dataset/Gh All Retrofits {update_date}.csv'
    final_cols = ['Date Process Complete','province_group','Total Grant Approved']
    units = 5000 # >10 years
    st = time.perf_counter()
    print(f"Computing Greener Homes predictions ...")
    gh_prediction(retrofit_path,
                  begin_date=begin_date,
                  units=units,
                  final_cols=final_cols,
                  )
    print(f"... Complete! In {time.perf_counter() - st:0.4f} seconds")