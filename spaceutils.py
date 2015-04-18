import matplotlib.pyplot as plt
import scipy.constants as consts


def set_graph_title(s):
    plt.title(s)
    fig = plt.gcf()
    fig.canvas.set_window_title(s)


def maximize_plot_window():
    fig_manager = plt.get_current_fig_manager()
    backend_name = plt.get_backend().lower()
    if backend_name.find('qt') >= 0:
        fig_manager.window.showMaximized()
    elif backend_name.find('tk') >= 0:
        maxsz = fig_manager.window.maxsize()
        fig_manager.resize(maxsz[0] - 80, maxsz[1] - 80)


def remove_plot_border():
    plt.figure(1).tight_layout(pad=0)


def show_maximized_plot(title):
    set_graph_title(title)
    remove_plot_border()
    maximize_plot_window()
    plt.show()
    plt.close()


#================================================================================================


def parsec_to_lightyear(dist):
    LIGHT_YEARS_IN_PARSEC = 3.2615638
    return dist * LIGHT_YEARS_IN_PARSEC


def megaparsec_to_lightyear(dist):
    return parsec_to_lightyear(dist * consts.mega)


def kiloparsec_to_lightyear(dist):
    return parsec_to_lightyear(dist * consts.kilo)


def parallax_millisecond_to_light_year(p):
    d = 1 / (p * consts.milli)
    return parsec_to_lightyear(d)

