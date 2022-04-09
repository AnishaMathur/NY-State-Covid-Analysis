import matplotlib.pyplot as plt
import sklearn.metrics as metrics
import numpy as np
import matplotlib.colors as colors
import mapclassify
import contextily as cx
import geopandas as gpd
import pandas as pd


def plot_feature_importance(model, title="Feature importances using MDI", save_fig=None):
    features = None
    if (getattr(model, 'coef_', None) is not None):
        features = model.coef_
    else:
        features = model.feature_importances_

    fig, ax = plt.subplots(figsize=(15, 12))
    ax.bar(model.feature_names_in_, features)
    ax.set_title(title)
    ax.set_xticklabels(model.feature_names_in_, rotation=90)
    plt.axhline(y=0, color=".5")
    if save_fig:
        plt.savefig(f"../notebooks/plots/{save_fig}.png")
        plt.savefig(f"../notebooks/plots/{save_fig}.jpeg")
    fig.tight_layout()


def plot_feature_importance_cls(model, title="Feature importances using MDI"):
    features = None
    if (getattr(model, 'coef_', None) is not None):
        features = model.coef_[0]
    else:
        features = model.feature_importances_

    fig, ax = plt.subplots(figsize=(15, 8))
    ax.bar(model.feature_names_in_, features)
    ax.set_title(title)
    ax.set_xticklabels(model.feature_names_in_, rotation=90)
    ax.set_ylabel("Mean decrease in impurity")
    fig.tight_layout()


def top_k_hsp_predction_loss(model, subset_test, target, topK):
    unique_hsps = subset_test.index.get_level_values('Facility Name').unique()
    losses = []
    for analyse_hsp in unique_hsps:
        test_set = subset_test[subset_test.index.get_level_values(
            'Facility Name') == analyse_hsp]
        test_X = test_set.drop(target, axis=1)

        y_preds = model.predict(test_X)
        y_test = test_set[[target]]

        loss = metrics.mean_squared_error(y_test, y_preds)
        losses.append(loss)
    losses = np.asarray(losses)
    ind = np.argpartition(losses, -topK)[-topK:]
    print('Loss Min: ', losses.min(), ' | Loss Max: ', losses.max())
    return [(unique_hsps[idx], losses[idx]) for idx in ind[np.argsort(losses[ind])]]


def get_accuracy_error(model, subset_test, target):
    unique_hsps = subset_test.index.get_level_values('Facility Name').unique()
    mses = []
    r2s = []
    for analyse_hsp in unique_hsps:
        test_set = subset_test[subset_test.index.get_level_values(
            'Facility Name') == analyse_hsp]
        test_X = test_set.drop(target, axis=1)

        y_preds = model.predict(test_X)
        y_test = test_set[[target]]

        mse = metrics.mean_absolute_error(y_test, y_preds)
        r2 = metrics.r2_score(y_test, y_preds)
        mses.append(mse)
        r2s.append(r2)
    return mses, r2s


def residual(model, subset_test, target):
    X = subset_test.drop(target, axis=1)
    y = subset_test[target]

    y_preds = model.predict(X)
    diff = [y-y_preds]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(diff, bins=50)
    fig.show()


def plot_geo_data(df, col_name, ax, fig, title="", show_base_cbar=False, show_base_map=False, cmap='Reds'):
    k = 1600  # I find that the more colors, the smoother the viz becomes as data points are spread across gradients
    cmap = cmap
    figsize = (20, 15)
    scheme = 'Quantiles'
    crs = {'init': 'epsg:4326'}

    subset = df.copy()
    subset['pop_density'] = subset['POP2020']/subset['CALC_SQ_MI']

    subset = subset.to_crs(crs)
    subset.plot(column=col_name, cmap=cmap, figsize=figsize, ax=ax,
                scheme=scheme, k=k, legend=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    # Adding Colorbar for legibility

    # normalize color
    vmin, vmax, vcenter = subset[col_name].min(
    ), subset[col_name].max(), subset[col_name].mean()
    divnorm = colors.TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
    # create a normalized colorbar
    if show_base_cbar:
        cbar = plt.cm.ScalarMappable(norm=divnorm, cmap=cmap)
        fig.colorbar(cbar, ax=ax)
    ax.set(ylabel="Lattitude", xlabel="Longitude")
    ax.set_title(title, fontsize=20)
    if show_base_map:
        cx.add_basemap(ax, crs=crs, source=cx.providers.Stamen.TonerLite)


def prepare_df_for_geo_plot(df, model, target, cols,  date='2022-01-01'):
    # Plot Prediction VS ACtual of County overload on a day.
    temp = df.copy()
    X = temp[cols].drop(target, axis=1)
    temp['predicted'] = model.predict(X)
    temp['predicted_availability'] = temp['predicted']/temp['Total Beds']
    temp['actual_availability'] = temp['overload-14day']/temp['Total Beds']
    temp.replace([np.inf, -np.inf], 0, inplace=True)
    temp['class_predicted'] = (
        temp['predicted_availability'] < 0.3).astype(int)
    temp['class_actual'] = (temp['actual_availability'] < 0.3).astype(int)

    temp1 = temp.groupby(by=['county', 'date']).sum()
    temp1 = temp1[['class_actual', 'class_predicted']]

    temp2 = temp.reset_index().groupby(by=['county', 'date']).count()
    temp2 = temp2[['Facility Name']]

    joined = temp1.join(temp2)
    joined = joined.rename(
        columns={'Facility Name': 'total_hsp', 'class_actual': 'actual_overloaded_hsp', 'class_predicted': 'predicted_overloaded_hsp'})
    joined['actual_overload_%'] = joined['actual_overloaded_hsp'] / \
        joined['total_hsp']
    joined['predicted_overload_%'] = joined['predicted_overloaded_hsp'] / \
        joined['total_hsp']

    # shape file
    street_map = gpd.read_file(
        '../data/raw_datasets/NYS_Civil_Boundaries.shp.zip',)

    df_temp = joined.copy()
    df_temp = df_temp[df_temp.index.get_level_values(
        'date') == date].reset_index()
    df_temp = df_temp.rename(columns={'county': 'COUNTY'})
    df_temp = pd.merge(street_map, df_temp, on='COUNTY', how='left')
    return df_temp


def prepare_input_data(df, train_start_date, train_end_date, test_start_date, test_end_date,
                       features, features_diff, nshift=4, forecast=14):

    subset = df.copy()
    subset['day_of_week'] = subset.index.get_level_values('date').dayofweek
    subset['day_of_month'] = subset.index.get_level_values('date').day
    subset['overload'] = subset['Number of Beds Available'] + \
        subset['Number of ICU Beds Available'] - \
        subset['Patients Newly Admitted']

    # diff column with difference between yesterday and day
    diff_cols = []
    for i in range(1, nshift):
        subset.loc[:, 'overload_T-' +
                   str(i)] = subset.groupby(level=0)['overload'].shift(i)
        subset.loc[:, 'overload_T-' +
                   str(i) + '_diff'] = subset.groupby(level=0)['overload_T-'+str(i)].diff()
        diff_cols.append('overload_T-' +
                         str(i))
        diff_cols.append('overload_T-'+str(i) + '_diff')

    for col in features_diff:
        subset.loc[:, col+'_diff'] = subset.groupby(level=0)[col].diff()
        diff_cols.append(col)
        diff_cols.append(col+'_diff')

    # overload days in future
    subset.loc[:, f'overload-{forecast}day'] = subset.groupby(
        level=0)['overload'].shift(forecast)
    # dropping NAs
    subset = subset.dropna()

    target = f'overload-{forecast}day'
    cols = features + diff_cols

    subset_temp_test = subset[(
        subset.index.get_level_values('date') > test_start_date)]

    subset = subset[cols]

    # subset date range
    subset_test = subset[(subset.index.get_level_values('date') > test_start_date) & (
        subset.index.get_level_values('date') <= test_end_date)]

    subset = subset[(subset.index.get_level_values('date') >= train_start_date) & (
        subset.index.get_level_values('date') <= train_end_date)]

    return subset, subset_test, target, subset_temp_test, cols
