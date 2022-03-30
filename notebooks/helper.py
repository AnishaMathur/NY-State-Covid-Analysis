import matplotlib.pyplot as plt


def plot_feature_importance(model, title="Feature importances using MDI"):
    features = None
    if (getattr(model, 'coef_', None) is not None):
        features = model.coef_
    else:
        features = model.feature_importances_

    fig, ax = plt.subplots(figsize=(15, 4))
    ax.bar(model.feature_names_in_, features)
    ax.set_title(title)
    ax.set_ylabel("Mean decrease in impurity")
    fig.tight_layout()
