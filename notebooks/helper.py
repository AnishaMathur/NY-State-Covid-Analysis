import matplotlib.pyplot as plt
import sklearn.metrics as metrics
import numpy as np


def plot_feature_importance(model, title="Feature importances using MDI"):
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
