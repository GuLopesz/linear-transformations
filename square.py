#bibliotecas usadas
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import RadioButtons, Slider, CheckButtons

#definicao dos vertices do quadrado
square_vertices = np.array([[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]]).T

#base de exemplo (vetores não ortogonais) para provar que o código funciona
#vetores v1=(1, 0.5) e v2=(0.5, 1)
EXAMPLE_BASIS = np.array([[1, 0.5], [0.5, 1]])

def square_shearing(points, k, axs="x", use_custom_basis=False):
    #matriz de transformação na base local (cisalhamento)
    matrix = np.eye(2)
    if axs == "x":
        matrix[0, 1] = k  #T(x,y) = (x + ky, y)
    else:
        matrix[1, 0] = k  #T(x,y) = (x, y + kx)

    #se for base canonica, aplica direto
    if not use_custom_basis:
        return matrix @ points

    #logica de mudanca de base (P * M * P^-1)
    #p é a matriz onde as colunas são os vetores da nova base
    P = EXAMPLE_BASIS.T 
    try:
        P_inv = np.linalg.inv(P) #inversa para trazer os pontos para a base local
        
        #a transformação completa: pega a base passada -> base canonica -> cisalha -> volta para a base passada
        final_matrix = P @ matrix @ P_inv
        return final_matrix @ points
    except np.linalg.LinAlgError:
        print("Erro: Base inválida.")
        return points

def create_window():
    fig, ax = plt.subplots(figsize=(10, 8))
    manager = fig.canvas.manager
    manager.set_window_title("Transformações Lineares 2D") 

    plt.subplots_adjust(bottom=0.5, left=0.3)
    plt.title("Transformações Lineares 2D (Cisalhamento)")
    plt.grid(True, linestyle="--", alpha=0.3)


    ax.set_xlim(-5, 8)
    ax.set_ylim(-5, 8)
    ax.set_aspect("equal")

    return fig, ax

def initial_plot(ax, points):
    ax.plot(points[0, :], points[1, :], "k--", alpha=0.5, label="Inicial")
    (line,) = ax.plot(points[0, :], points[1, :], "r-", linewidth=2, alpha=1, label="Transformado")
    
    #plota vetores da base alternativa (apenas visualização)
    origin = [0], [0]
    vec1 = EXAMPLE_BASIS[0]
    vec2 = EXAMPLE_BASIS[1]
    #seta verde e azul para mostrar a base passada
    ax.quiver(*origin, vec1[0], vec1[1], color=['g'], scale=1, scale_units='xy', angles='xy', alpha=0.3)
    ax.quiver(*origin, vec2[0], vec2[1], color=['b'], scale=1, scale_units='xy', angles='xy', alpha=0.3)
    
    ax.legend()
    return line

def create_controls():
    #slider k
    ax_k = plt.axes([0.2, 0.2, 0.65, 0.03])
    slider_k = Slider(ax_k, "Fator K", 0.0, 2.0, valinit=0.0, valstep=0.1)

    #botoes
    ax_radio = plt.axes([0.2, 0.05, 0.15, 0.10])
    radio = RadioButtons(ax_radio, ("X", "Y"))

    #botao para ativar a base personalizada
    ax_check = plt.axes([0.4, 0.05, 0.25, 0.10])
    check_basis = CheckButtons(ax_check, ["Usar Base Genérica"], [False])

    return slider_k, radio, check_basis

if __name__ == "__main__":
    fig, ax = create_window()
    new_line = initial_plot(ax, square_vertices)
    slider_k, radio, check_basis = create_controls()

    def update(val):
        k = slider_k.val
        option = radio.value_selected
        axs = "x" if option == "X" else "y"
        
        #verifica se o checkbox foi marcado
        status = check_basis.get_status()
        use_custom = status[0] if status else False

        new_points = square_shearing(square_vertices, k, axs, use_custom)
        new_line.set_xdata(new_points[0, :])
        new_line.set_ydata(new_points[1, :])
        fig.canvas.draw_idle()

    slider_k.on_changed(update)
    radio.on_clicked(update)
    check_basis.on_clicked(update)

    #exibe a interface gráfica
    plt.show()