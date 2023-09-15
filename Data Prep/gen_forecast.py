import os

import warnings
warnings.simplefilter(action='ignore')

import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression, Lasso, ElasticNet
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

import warnings
warnings.filterwarnings("ignore")

# from Scripts.dur_data_gen import generate_labels, populate_durations
HOME = os.path.expanduser("~")
WORK_DIR = os.getcwd()
DIR_PATH = os.path.join(WORK_DIR,"Files for Tableau\\")
SAVE = False
PREFIX = ''
SUFFIX = ''

###

def pick_forecaster(df,
                    input_col:str='dim_week',
                    predict_col:str='application_id',
                    models:list=[LinearRegression()],
                    period_freq:str='datetime64[W]',
                    metric=mean_squared_error,
                    test_size=0.1,
                    ):
    train_df,test_df = train_test_split(df,test_size=test_size)
    #
    X_train = train_df[input_col].values.reshape(-1,1).astype(period_freq).astype('int64')
    Y_train = train_df[predict_col].values.reshape(-1,1)

    X_test = test_df[input_col].values.reshape(-1,1).astype(period_freq).astype('int64')
    Y_test = test_df[predict_col].values.reshape(-1,1)
    #
    fitted_models = []
    for model in models:
        fitted_models.append(model.fit(X_train,Y_train))
    #
    Y_preds = []
    for model in fitted_models:
        Y_preds.append(model.predict(X_test))
    #
    mses = []
    for y_pred in Y_preds:
        mses.append(metric(Y_test, y_pred))
    #
    argmin = np.array(mses).argmin()
    return models[argmin]

def train_forecaster(df,
                     input_col:str='dim_week',
                     predict_col:str='application_id',
                     models:list=[LinearRegression()],
                     period_freq:str='datetime64[W]',
                     ):
    model = pick_forecaster(df,
                            input_col=input_col,
                            predict_col=predict_col,
                            models=models,
                            period_freq=period_freq,
                            )
    #
    X = df[input_col].values.reshape(-1,1).astype(period_freq).astype('int64')
    Y = df[predict_col].values.reshape(-1,1)
    # 
    model = model.fit(X,Y)
    return model

def predict_forecast(last_date,
                     model,
                     input_col:str='dim_week_int',
                     predict_col:str='number_applications',
                     periods:int=500,
                     period_freq:str='datetime64[W]',
                     ):
    X_0 = pd.date_range(last_date,
                        periods=periods,
                        freq='W',
                        ).values.reshape(-1,1).astype(period_freq).astype('int64')
    #
    Y_0 = model.predict(X_0)
    #
    forecast_df = pd.DataFrame({input_col:np.reshape(X_0,(-1)).tolist(),
                                predict_col:np.reshape(Y_0,(-1)).tolist(),
                                })
    if '_int' in input_col:
        output_col = input_col.replace('_int','')
        forecast_df[output_col] = np.array(forecast_df[input_col].values).astype(period_freq)
    #
    return forecast_df

###

def main(hist_df,
         input_col,
         predict_col,
         output_col,
         output_pred_col,
         periods,
         models,
         ):
    model = train_forecaster(hist_df,
                             input_col=input_col,
                             predict_col=predict_col,
                             models=models,
                             )
    #
    last_date = hist_df[input_col].iloc[-1]
    forecast_df = predict_forecast(last_date,
                                   model,
                                   input_col=output_col,
                                   predict_col=output_pred_col,
                                   periods=periods,
                                   )
    #
    return forecast_df

if __name__=='__main__':
    files = ['retrofit_running_sum_all_provinces.csv',
             'app_history_projection.csv']
    alpha:float=0.1
    lf:str='squared_error'
    models = [LinearRegression(), 
              Lasso(alpha=0.1),
              #   SGDRegressor(loss=lf),
              ElasticNet(alpha=0.1),
              #   GradientBoostingRegressor(loss=lf),
              ]

    data_path = os.path.join(DIR_PATH,files[0])
    columns=['dim_week','province_group','total_grant_approved','running_sum']
    running_sum_df = pd.read_csv(data_path)
    running_sum_df.columns = columns
    running_sum_df = running_sum_df.sort_values(by=['dim_week']).reset_index(drop=True)

    periods=2500
    output_col='dim_week_int'
    output_pred_col='running_sum'
    forecast_grant_df = main(running_sum_df,
                             input_col='dim_week',
                             predict_col='running_sum',
                             output_col=output_col,
                             output_pred_col=output_pred_col,
                             periods=periods,
                             models=models,
                             )

    #

    data_path = os.path.join(DIR_PATH,files[1])
    app_hist_df = pd.read_csv(data_path)
    app_hist_df = app_hist_df.dropna().sort_values(by=['dim_week']).reset_index(drop=True)

    periods=1500
    output_pred_col='number_applications'
    forecast_applicants_df = main(app_hist_df,
                                  input_col='dim_week',
                                  predict_col='application_id',
                                  output_col=output_col,
                                  output_pred_col=output_pred_col,
                                  periods=periods,
                                  models=models,
                                  )
    
    forecast_df = forecast_grant_df[['dim_week','running_sum']]
    forecast_df = forecast_df.rename(columns={'running_sum':'forecast_value'})
    forecast_df['forecast_focus'] = 'grant_amount'

    temp_forecast_df = forecast_applicants_df[['dim_week','number_applications']]
    temp_forecast_df = temp_forecast_df.rename(columns={'number_applications':'forecast_value'})
    temp_forecast_df['forecast_focus'] = 'num_applicants'

    forecast_df = pd.concat([forecast_df,temp_forecast_df])
    
    forecast_df.to_csv(os.path.join(DIR_PATH,'forecasting.csv'))