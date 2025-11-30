#bibliotecas usadas
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import RadioButtons, Slider, CheckButtons
from mpl_toolkits.mplot3d import Axes3D

#definicao dos vertices do cubo
cube_vertices = np.array([
    [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],  
    [-1, -1, 1],  [1, -1, 1],  [1, 1, 1],  [-1, 1, 1]    
]).T

cube_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0), 
    (4, 5), (5, 6), (6, 7), (7, 4),  
    (0, 4), (1, 5), (2, 6), (3, 7)   
]

#base 3D generica rotacionada/cisalhada
EXAMPLE_BASIS_3D = np.array([
    [1, 0, 0.5],
    [0, 1, 0.5],
    [0.2, 0.2, 1]
])

#funcao para construir as arestas do cubo
def build_cube_lines(points):
    x_list, y_list, z_list = [], [], []
    for (start, end) in cube_edges:
        x_list.extend([points[0, start], points[0, end], np.nan])
        y_list.extend([points[1, start], points[1, end], np.nan])
        z_list.extend([points[2, start], points[2, end], np.nan])
    return x_list, y_list, z_list

def cube_shearing(points, k, axs="x", use_custom_basis=False):
    #funcao que faz o processo de cisalhamento padrao
    matrix = np.eye(3)
    if axs == "x":
        matrix[0, 1] = k 
    elif axs == "y":
        matrix[1, 0] = k 
    elif axs == "z":
        matrix[2, 0] = k 

    if not use_custom_basis:
        return matrix @ points

    #mudanca de base
    P = EXAMPLE_BASIS_3D.T
    try:
        P_inv = np.linalg.inv(P)
        final_matrix = P @ matrix @ P_inv
        return final_matrix @ points
    except:
        return points

#cria a janela do matplotlib
def create_window():
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    #define o nome que aparece na janela
    manager = fig.canvas.manager
    manager.set_window_title("Transformações Lineares 3D")

    plt.subplots_adjust(bottom=0.35)
    plt.title("Transformações Lineares 3D")
    
    #define os limites do grafico
    limit = 4
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_zlim(-limit, limit)
    
    #nome dos eixos
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    return fig, ax

#faz a plotagem dos pontos
#plota os pontos iniciais e depois plota os pontos com base no fator de tranformacao(k)
def initial_plot(ax, points):
    ix, iy, iz = build_cube_lines(points)
    ax.plot(ix, iy, iz, "k--", alpha=0.3, label="Original")
    (line,) = ax.plot(ix, iy, iz, "r-", linewidth=2, label="Transformado")
    ax.legend()
    return line

#funcao para atualizar os dados de uma linha no espaco 3d
def update_line_data(line, x, y, z):
    line.set_data(x, y)
    line.set_3d_properties(z)

#cria os controles do matplotlib para a selecao dos eixos e do valor de k
def create_controls():
    #slider para o valor de cisalhamento k
    ax_slider = plt.axes([0.2, 0.2, 0.65, 0.03])
    slider_k = Slider(ax_slider, "Fator K", 0.0, 2.0, valinit=0.0, valstep=0.1)
    
    #botoes de selecao do eixo
    ax_radio = plt.axes([0.2, 0.05, 0.15, 0.10])
    radio = RadioButtons(ax_radio, ("X", "Y", "Z"))

    #check button para 3d
    ax_check = plt.axes([0.4, 0.05, 0.25, 0.10])
    check_basis = CheckButtons(ax_check, ["Usar Base Genérica"], [False])
    
    return slider_k, radio, check_basis

if __name__ == "__main__":
    fig, ax = create_window()              
    line = initial_plot(ax, cube_vertices)          
    slider_k, radio, check_basis = create_controls()        

    def update(val):
        k = slider_k.val #pega valor do slider
        option = radio.value_selected #eixo selecionado
        axs = option.lower()
        
        status = check_basis.get_status()
        use_custom = status[0] if status else False

        new_vertices = cube_shearing(cube_vertices, k, axs, use_custom)
        nx, ny, nz = build_cube_lines(new_vertices)
        update_line_data(line, nx, ny, nz)
        fig.canvas.draw_idle()

    slider_k.on_changed(update)
    radio.on_clicked(update)
    check_basis.on_clicked(update)

    #exibe a interface grafica
    plt.show()