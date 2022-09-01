def phase_velocity_calculation(f1, a1, c0, h):
    # Radius - Wavelength Ratio (RWR):
    rwr = f1 * a1 / c0

    i = 0
    while rwr >= h[i][0]:
        i += 1
        if i > 25:
            break

    # Interpolation of phase velocity from Bancroft's data table:
    if i < 25:
        phase_velocity = c0 * (
                (1 / (h[i][0] - h[i - 1][0])) * (rwr - h[i - 1][0]) * (h[i][1] - h[i - 1][1]) + h[i - 1][1])
    else:
        phase_velocity = 0.59 * c0

    return phase_velocity