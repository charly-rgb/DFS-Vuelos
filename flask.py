from flask import Flask, render_template
from Vuelo_3602 import Nodo

app = Flask(__name__)

# Definición de la función de búsqueda
def buscar_solucion_bfs(conexiones, estado_inicial, solucion):
    solucionado = False
    nodos_visitados = []
    nodos_frontera = []
    nodo_inicial = Nodo(estado_inicial)
    nodos_frontera.append(nodo_inicial)
    while not solucionado and len(nodos_frontera) != 0:
        nodo = nodos_frontera[0]
        nodos_visitados.append(nodos_frontera.pop(0))
        if nodo.get_datos() == solucion:
            solucionado = True
            return nodo
        else:
            dato_nodo = nodo.get_datos()
            lista_hijos = []
            for un_hijo in conexiones[dato_nodo]:
                hijo = Nodo(un_hijo)
                lista_hijos.append(hijo)
                if not hijo.en_lista(nodos_visitados) and not hijo.en_lista(nodos_frontera):
                    nodos_frontera.append(hijo)
            nodo.set_hijos(lista_hijos)

# Ruta principal
@app.route('/')
def index():
    conexiones = {
        'EDO.MEX': {'QRO', 'SLP', 'SONORA'},
        'PUEBLA': {'HIDALGO', 'SLP'},
        'CDMX': {'MICHOACAN'},
        'MICHOACAN': {'SONORA'},
        'SLP': {'QRO', 'PUEBLA', 'EDO.MEX', 'SONORA', 'GUADALAJARA'},
        'QRO': {'EDO.MEX', 'SLP'},
        'HIDALGO': {'PUEBLA', 'GUADALAJARA', 'SONORA'},
        'GUADALAJARA': {'HIDALGO', 'SLP'},
        'MONTERREY': {'SONORA'},
        'SONORA': {'MONTERREY', 'HIDALGO', 'SLP', 'EDO.MEX', 'MICHOACAN'}
    }
    estado_inicial = 'EDO.MEX'
    solucion = 'HIDALGO'
    nodo_solucion = buscar_solucion_bfs(conexiones, estado_inicial, solucion)

    resultado = []
    nodo = nodo_solucion
    while nodo.get_padre() is not None:
        resultado.append(nodo.get_datos())
        nodo = nodo.get_padre()
    resultado.append(estado_inicial)
    resultado.reverse()

    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
