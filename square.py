import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import RadioButtons, Slider


#definicao dos vertices do quadrado
square_vertices = np.array([[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]]).T

#funcao que faz o processo de cisalhamento
#criacao da matriz identidade 2x2 e realizacao da operacao nos eixos x e y
def square_shearing(points, k, axs="x"):
    matrix = np.eye(2)

    if axs == "x":
        matrix[0, 1] = k
    else:
        matrix[1, 0] = k

    return matrix @ points

#cria a janela do matplotlib
def create_window():
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.subplots_adjust(bottom=0.5, left=0.3)
    plt.title("Transformações Lineares 2D")
    plt.grid(True, linestyle="--", alpha=0.3)

    ax.set_xlim(-3, 7)
    ax.set_ylim(-3, 7)
    ax.set_aspect("equal")

    return fig, ax

#faz a plotagem dos pontos
#plota os pontos iniciais e depois plota os pontos com base no fator de transformacao(k)
def initial_plot(ax, points):
    ax.plot(points[0, :], points[1, :], "k--", alpha=0.5, label="Inicial")
    (line,) = ax.plot(points[0, :], points[1, :], "r-",linewidth=2, alpha=1, label="Transformado")
    ax.legend()
    return line

#cria os controles do matplotlib para a selecao dos eixos e do valor de k
def create_controls():
    ax_k = plt.axes([0.2, 0.2, 0.65, 0.03])
    slider_k = Slider(
        ax_k, "Fator de transformação K", 0.0, 2.0, valinit=0.0, valstep=0.1
    )
    ax_radio = plt.axes([0.2, 0.05, 0.3, 0.10])
    radio = RadioButtons(ax_radio, ("X", "Y"))

    return slider_k, radio


if __name__ == "__main__":
    fig, ax = create_window()
    new_line = initial_plot(ax, square_vertices)
    slider_k, radio = create_controls()

#funcao de atualizacao para aplicar o cisalhamento em tempo real baseando-se na mudanca do fator k
    def update(val):
        k = slider_k.val
        option = radio.value_selected
        axs = "x" if option == "X" else "y"

        new_points = square_shearing(square_vertices, k, axs)
        new_line.set_xdata(new_points[0, :])
        new_line.set_ydata(new_points[1, :])
        fig.canvas.draw_idle()

    slider_k.on_changed(update)
    radio.on_clicked(update)

    plt.show()
