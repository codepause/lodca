def linear_interpolation(A: tuple, B: tuple) -> callable:
    """
    Helper function for interface mapping. Depends on interface scale.

    Args:
        A: coordinates (X, Y) of the first point
        B: coordinates (X, Y) of the second point

    Returns:
        linear function of one argument X (callable).
    """
    assert abs(B[0] - A[0]) > 1e-6
    k = (B[1] - A[1]) / (B[0] - A[0])
    b = A[1] - k * A[0]
    return lambda game_config: k * game_config.settings.scale + b
