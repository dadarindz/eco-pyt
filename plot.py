from matplotlib.figure import Figure

# ----------------------------------------------------------------------
# Plot Matplotlib
# ----------------------------------------------------------------------

def create_plot(dates, temperatures_min, temperatures_max):
    """Crée et retourne une Figure Matplotlib avec les courbes de températures min et max sur les dates fournies."""
    figure = Figure(figsize = (3.8, 3.2))
    axes = figure.add_subplot(111)

    ######################################

    # Les dates sont placées en abscisse aux positions 0, 1, 2, ... (voir set_xticks plus bas)
    x = range(len(dates))
    axes.plot(x, temperatures_max, "o-", color = "red", label = "Max")
    axes.plot(x, temperatures_min, "o-", color = "blue", label = "Min")
    # Zone grisée entre les deux courbes
    axes.fill_between(x, temperatures_min, temperatures_max, color = "grey", alpha = 0.2)

    axes.set_title("Températures (°C)")
    axes.grid(True)

    ######################################

    # Améliore la lisibilité
    axes.set_xticks(range(len(dates)))
    axes.set_xticklabels([d[5:] for d in dates], rotation = 45)
    figure.tight_layout()

    return figure