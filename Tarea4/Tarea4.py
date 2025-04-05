
from graphviz import Digraph

class NAVL:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class AAVL:
    def insertar(self, raiz, valor):
        if not raiz:
            return NAVL(valor)
        elif valor < raiz.valor:
            raiz.izquierda = self.insertar(raiz.izquierda, valor)
        else:
            raiz.derecha = self.insertar(raiz.derecha, valor)

        raiz.altura = 1 + max(self.obtener_altura(raiz.izquierda),
                              self.obtener_altura(raiz.derecha))

        balance = self.obtener_balance(raiz)

        # Rotaciones
        if balance > 1 and valor < raiz.izquierda.valor:
            return self.rotar_derecha(raiz)
        if balance < -1 and valor > raiz.derecha.valor:
            return self.rotar_izquierda(raiz)
        if balance > 1 and valor > raiz.izquierda.valor:
            raiz.izquierda = self.rotar_izquierda(raiz.izquierda)
            return self.rotar_derecha(raiz)
        if balance < -1 and valor < raiz.derecha.valor:
            raiz.derecha = self.rotar_derecha(raiz.derecha)
            return self.rotar_izquierda(raiz)

        return raiz

    def buscar(self, raiz, valor):
        if not raiz or raiz.valor == valor:
            return raiz
        if valor < raiz.valor:
            return self.buscar(raiz.izquierda, valor)
        return self.buscar(raiz.derecha, valor)

    def eliminar(self, raiz, valor):
        if not raiz:
            return raiz
        if valor < raiz.valor:
            raiz.izquierda = self.eliminar(raiz.izquierda, valor)
        elif valor > raiz.valor:
            raiz.derecha = self.eliminar(raiz.derecha, valor)
        else:
            if not raiz.izquierda:
                return raiz.derecha
            elif not raiz.derecha:
                return raiz.izquierda
            temp = self.obtener_min(raiz.derecha)
            raiz.valor = temp.valor
            raiz.derecha = self.eliminar(raiz.derecha, temp.valor)

        if not raiz:
            return raiz

        raiz.altura = 1 + max(self.obtener_altura(raiz.izquierda),
                              self.obtener_altura(raiz.derecha))
        balance = self.obtener_balance(raiz)

        if balance > 1 and self.obtener_balance(raiz.izquierda) >= 0:
            return self.rotar_derecha(raiz)
        if balance < -1 and self.obtener_balance(raiz.derecha) <= 0:
            return self.rotar_izquierda(raiz)
        if balance > 1 and self.obtener_balance(raiz.izquierda) < 0:
            raiz.izquierda = self.rotar_izquierda(raiz.izquierda)
            return self.rotar_derecha(raiz)
        if balance < -1 and self.obtener_balance(raiz.derecha) > 0:
            raiz.derecha = self.rotar_derecha(raiz.derecha)
            return self.rotar_izquierda(raiz)

        return raiz

    def obtener_min(self, nodo):
        while nodo.izquierda:
            nodo = nodo.izquierda
        return nodo

    def obtener_altura(self, nodo):
        return nodo.altura if nodo else 0

    def obtener_balance(self, nodo):
        return self.obtener_altura(nodo.izquierda) - self.obtener_altura(nodo.derecha) if nodo else 0

    def rotar_izquierda(self, z):
        y = z.derecha
        T2 = y.izquierda
        y.izquierda = z
        z.derecha = T2
        z.altura = 1 + max(self.obtener_altura(z.izquierda), self.obtener_altura(z.derecha))
        y.altura = 1 + max(self.obtener_altura(y.izquierda), self.obtener_altura(y.derecha))
        return y

    def rotar_derecha(self, z):
        y = z.izquierda
        T3 = y.derecha
        y.derecha = z
        z.izquierda = T3
        z.altura = 1 + max(self.obtener_altura(z.izquierda), self.obtener_altura(z.derecha))
        y.altura = 1 + max(self.obtener_altura(y.izquierda), self.obtener_altura(y.derecha))
        return y

    def detectar_codificacion(self, archivo):
        with open(archivo, 'rb') as f:
            resultado = chardet.detect(f.read())
        return resultado['encoding']

    def cargar_desde_csv(self, ruta):
        codificacion = self.detectar_codificacion(ruta)
        with open(ruta, newline='', encoding=codificacion) as archivo:
            lector = csv.reader(archivo)
            raiz = None
            for fila in lector:
                for valor in fila:
                    if valor.strip().isdigit():
                        raiz = self.insertar(raiz, int(valor))
        return raiz

    def graficar(self, raiz, nombre_archivo="arbol_avl"):
        def agregar_nodos_edges(dot, nodo):
            if nodo:
                dot.node(str(nodo.valor))
                if nodo.izquierda:
                    dot.edge(str(nodo.valor), str(nodo.izquierda.valor))
                    agregar_nodos_edges(dot, nodo.izquierda)
                if nodo.derecha:
                    dot.edge(str(nodo.valor), str(nodo.derecha.valor))
                    agregar_nodos_edges(dot, nodo.derecha)

        dot = Digraph()
        agregar_nodos_edges(dot, raiz)
        dot.render(nombre_archivo, format='png', cleanup=True)
        print(f"Árbol generado como {nombre_archivo}.png")

# CLI
def menu():
    arbol = AAVL()
    raiz = None

    while True:
        print("\======MENU======")
        print("1. Ingresar un numero")
        print("2. Buscar un numero")
        print("3. Eliminar un numero")
        print("4. Cargar desde archivo CSV")
        print("5.Generar imagen")
        print("6. Salir")
        opcion = input("Seleccione una opción:")

        if opcion == '1':
            n = int(input("Ingrese numero a insertar: "))
            raiz = arbol.insertar(raiz, n)
        elif opcion == '2':
            n = int(input("Ingrese numero a buscar: "))
            resultado = arbol.buscar(raiz, n)
            print("✅ Encontrado" if resultado else "❌ No encontrado")
        elif opcion == '3':
            n = int(input("Ingrese numero a eliminar: "))
            raiz = arbol.eliminar(raiz, n)
        elif opcion == '4':
            ruta = input("Ingrese ruta del archivo CSV: ")
            raiz = arbol.cargar_desde_csv(ruta)
            print("📄 Datos cargados.")
        elif opcion == '5':
            arbol.graficar(raiz)
        elif opcion == '6':
            break
        else:
            print(" Opción inválida")

if __name__ == "__main__":
    menu()
