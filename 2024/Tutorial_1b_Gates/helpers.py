""" 
Helper functions for Tutorial 1b: Quantum Dynamics and Single-Qubit Gates 
MIT 6.S089 Introduction to Quantum Computing
"""
import qutip as qt
from qutip.solver import Result

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from IPython.display import HTML


def plot_bloch(states, plotstyle="vector"):
    """
    Function to plot a list of states on the Bloch sphere.

    Args:
        states (List[qt.Qobj]): States to plot
        plotstyle (str): Either "vector" or "point"
    """
    try:
        length = len(states)
    except:
        length = 1
        states = [states]

    b = qt.Bloch()

    # Bloch sphere formatting
    b.vector_color = ["r"]
    b.point_color = ["b"]
    b.point_marker = ["o"]
    b.zlpos = [1.25, -1.35]

    for state in states:
        b.add_states(state, plotstyle)

    b.show()


def animate_bloch(states, interval=100, fig=None, ax=None, return_animation=False):
    """
    Function to animate a trajectory of a qubit state vector or density matrix on the Bloch
    sphere. Renders Bloch sphere via QuTuP, and saves via imageio. Adapted from
    https://sites.google.com/site/tanayroysite/articles/bloch-sphere-animation-using-qutip and
    https://qiskit.org/documentation/_modules/qiskit/visualization/transition_visualization.html

    Args:
        states (List[qt.Qobj] or QuTiP solver Result): States to plot
        interval (int): Time interval between frames
        fig, ax: Optional figure/axis to pass in
    """
    if type(states) is Result:
        states = states.states

    try:
        length = len(states)
    except:
        length = 1
        states = [states]

    if fig is None or ax is None:
        fig = plt.figure(figsize=(8, 8))
        ax = Axes3D(fig, auto_add_to_figure=False)
        fig.add_axes(ax)

    b = qt.Bloch(axes=ax)

    # Bloch sphere formatting
    b.vector_color = ["r"]
    b.point_color = ["b"]
    b.point_marker = ["o"]
    b.zlpos = [1.2, -1.35]

    def animate(i):
        b.clear()
        b.add_states(states[i])
        b.add_states(states[:i], "point")
        b.make_sphere()

        return ax

    ani = FuncAnimation(
        fig,
        animate,
        frames=length,
        interval=interval,
    )
    plt.close(fig)
    mpl.rcParams["animation.embed_limit"] = 50

    if return_animation:
        return ani
    return HTML(ani.to_jshtml())
