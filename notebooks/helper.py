import matplotlib.pyplot as plt
import sklearn.metrics as metrics
import numpy as np


def plot_feature_importance(model, title="Feature importances using MDI", save_fig=None):
    features = None
    if (getattr(model, 'coef_', None) is not None):
        features = model.coef_
    else:
        features = model.feature_importances_

    fig, ax = plt.subplots(figsize=(15, 8))
    ax.bar(model.feature_names_in_, features)
    ax.set_title(title)
    ax.set_xticklabels(model.feature_names_in_, rotation=90)
    ax.set_ylabel("Mean decrease in impurity")
    if save_fig:
        plt.savefig(f"./plots/{save_fig}.png")
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
