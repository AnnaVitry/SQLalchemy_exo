def calculer_moyenne(data: list) -> float:
    r"""
    Calcule la moyenne arithmétique d'une liste de nombres.
    La formule mathématique est la suivante :

    .. math::
       \bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i

    Comme indiqué dans la littérature [1]_, la moyenne est sensible
    aux valeurs aberrantes.

    Args:
        data (list): Une liste ou un array de nombres.

    Returns:
        float: La moyenne calculée.
    """
    return data.sum() / len(data)
