import numpy as np
from pylatex import Document, Section, Subsection, Math, Matrix, Command

# Funciones para generar matrices
def generar_matriz_cuadrada(n, min_val=-10, max_val=10):
    """Genera una matriz cuadrada aleatoria de tamaño n x n"""
    return np.random.randint(min_val, max_val, (n, n))

def generar_matriz_fila(n, min_val=-10, max_val=10):
    """Genera una matriz fila aleatoria de tamaño 1 x n"""
    return np.random.randint(min_val, max_val, (1, n))

def generar_matriz_columna(m, min_val=-10, max_val=10):
    """Genera una matriz columna aleatoria de tamaño m x 1"""
    return np.random.randint(min_val, max_val, (m, 1))

def generar_matriz_rectangular(m, n, min_val=-10, max_val=10):
    """Genera una matriz rectangular aleatoria de tamaño m x n"""
    return np.random.randint(min_val, max_val, (m, n))

def generar_matriz_diagonal(n, min_val=-10, max_val=10):
    """Genera una matriz diagonal aleatoria de tamaño n x n"""
    diag = np.random.randint(min_val, max_val, n)
    return np.diag(diag)

def generar_matriz_triangular_superior(n, min_val=-10, max_val=10):
    """Genera una matriz triangular superior aleatoria"""
    mat = np.random.randint(min_val, max_val, (n, n))
    return np.triu(mat)

def generar_matriz_triangular_inferior(n, min_val=-10, max_val=10):
    """Genera una matriz triangular inferior aleatoria"""
    mat = np.random.randint(min_val, max_val, (n, n))
    return np.tril(mat)

def generar_matriz_identidad(n):
    """Genera una matriz identidad de tamaño n x n"""
    return np.eye(n)

def generar_matriz_nula(m, n):
    """Genera una matriz nula de tamaño m x n"""
    return np.zeros((m, n))

def mostrar_matriz_latex(matriz, nombre=None):
    """Muestra una matriz en formato LaTeX con mejor formato"""
    if nombre:
        return Math(data=[r'\displaystyle ', nombre + ' = ', Matrix(matriz)], escape=False)
    return Math(data=[r'\displaystyle ', Matrix(matriz)], escape=False)

def seccion_matrices_aleatorias():
    """Genera la sección de matrices aleatorias"""
    contenido = []
    
    matrices = [
        ('Matriz Fila', generar_matriz_fila(4), 'A'),
        ('Matriz Columna', generar_matriz_columna(4), 'B'),
        ('Matriz Cuadrada', generar_matriz_cuadrada(3), 'C'),
        ('Matriz Rectangular', generar_matriz_rectangular(2, 5), 'D'),
        ('Matriz Diagonal', generar_matriz_diagonal(4), 'E'),
        ('Matriz Triangular Superior', generar_matriz_triangular_superior(3), 'F'),
        ('Matriz Triangular Inferior', generar_matriz_triangular_inferior(3), 'G'),
        ('Matriz Identidad', generar_matriz_identidad(4), 'I'),
        ('Matriz Nula', generar_matriz_nula(3, 3), '0')
    ]
    
    for titulo, matriz, nombre in matrices:
        contenido.append({
            'titulo': titulo,
            'contenido': mostrar_matriz_latex(matriz, nombre)
        })
    
    return {
        'titulo': 'Matrices Aleatorias',
        'subsecciones': contenido
    }

def calcular_determinante_gauss(matriz, pasos=True):
    """Calcula el determinante mostrando cada cambio real en la matriz"""
    if matriz.shape[0] != matriz.shape[1]:
        raise ValueError("La matriz debe ser cuadrada")
    
    n = matriz.shape[0]
    det = 1.0
    pasos_latex = []
    mat = matriz.astype(float).copy()
    
    # Paso 0: Matriz original
    pasos_latex.append({
        'titulo': 'Matriz Original',
        'contenido': Math(data=[
            r'\det(A) = \det\left(', Matrix(mat), r'\right) = 1.00'
        ], escape=False)
    })

    for i in range(n):
        # Guardar copia antes de modificaciones
        mat_antes = mat.copy()
        
        # Paso 1: Pivoteo parcial
        max_row = i
        for k in range(i+1, n):
            if abs(mat[k, i]) > abs(mat[max_row, i]):
                max_row = k
        
        if max_row != i:
            # Mostrar estado antes del cambio
            pasos_latex.append({
                'titulo': f'Antes de Paso {i+1}.1: Estado actual',
                'contenido': Math(data=[Matrix(mat_antes)], escape=False)
            })
            
            # Intercambio de filas
            mat[[i, max_row]] = mat[[max_row, i]]
            det *= -1
            
            # Mostrar cambio
            pasos_latex.append({
                'titulo': f'Paso {i+1}.1: Intercambio F{i+1} ↔ F{max_row+1}',
                'contenido': Math(data=[
                    r'\begin{aligned}',
                    r'\text{Operación:} &\quad F_{%d} \leftrightarrow F_{%d} \\' % (i+1, max_row+1),
                    r'\text{Determinante:} &\quad \det \leftarrow -1 \times \det \\',
                    rf'&\quad = -1 \times {det/-1:.2f} = {det:.2f}',
                    r'\end{aligned}',
                    r'\quad \rightarrow \quad',
                    Matrix(mat)
                ], escape=False)
            })
        
        # Paso 2: Verificar pivote cero
        if np.isclose(mat[i, i], 0):
            det = 0
            pasos_latex.append({
                'titulo': f'Paso {i+1}.2: Pivote cero - det = 0',
                'contenido': Math(data=[r'\det(A) = 0'], escape=False)
            })
            break
        
        # Paso 3: Mostrar factor diagonal
        old_det = det
        det *= mat[i, i]
        pasos_latex.append({
            'titulo': f'Paso {i+1}.2: Factor diagonal a_{i+1},{i+1} = {mat[i,i]:.2f}',
            'contenido': Math(data=[
                r'\begin{aligned}',
                r'\text{Operación:} &\quad \det \leftarrow a_{%d,%d} \times \det \\' % (i+1, i+1),
                rf'&\quad = {mat[i,i]:.2f} \times {old_det:.2f} \\',
                rf'&\quad = {det:.2f}',
                r'\end{aligned}',
                r'\quad \text{Matriz actual:} \quad',
                Matrix(mat)
            ], escape=False)
        })
        
        # Paso 4: Eliminación gaussiana
        for j in range(i+1, n):
            mat_antes_eliminacion = mat.copy()
            factor = mat[j, i] / mat[i, i]
            mat[j, i:] -= factor * mat[i, i:]
            
            if pasos:
                # Mostrar estado antes de la operación
                pasos_latex.append({
                    'titulo': f'Antes de Paso {i+1}.{j+1}: Estado actual',
                    'contenido': Math(data=[Matrix(mat_antes_eliminacion)], escape=False)
                })
                
                # Mostrar operación
                paso = r'F_{%d} \leftarrow F_{%d} - %.2f \cdot F_{%d}' % (j+1, j+1, factor, i+1)
                pasos_latex.append({
                    'titulo': f'Paso {i+1}.{j+1}: Eliminación en F{j+1}',
                    'contenido': Math(data=[
                        r'\begin{aligned}',
                        r'\text{Operación:} &\quad ' + paso + r' \\',
                        r'\text{Efecto:} &\quad \text{No cambia el determinante} \\',
                        rf'&\quad \det = {det:.2f}',
                        r'\end{aligned}',
                        r'\quad \rightarrow \quad',
                        Matrix(mat)
                    ], escape=False)
                })
    
    # Resultado final
    elementos = [f"{x:.2f}" for x in np.diag(mat)]
    producto = r' \times '.join(elementos)
    signo = "-" if det < 0 else ""
    
    pasos_latex.append({
        'titulo': 'Matriz Triangular Final',
        'contenido': Math(data=[
            r'\text{Matriz triangular:}',
            r'\quad \det = ' + f'{det:.2f}',
            r'\quad \rightarrow \quad',
            Matrix(mat)
        ], escape=False)
    })
    
    pasos_latex.append({
        'titulo': 'Cálculo Final del Determinante',
        'contenido': Math(data=[
            r'\begin{aligned}',
            r'\det(A) &= ' + signo + r' \times '.join(elementos),
            rf'\\ &= ' + signo + f'{abs(det):.2f}',
            rf'\\ &= {det:.2f}',
            r'\end{aligned}'
        ], escape=False)
    })
    
    return det, pasos_latex

def seccion_determinante():
    """Genera la sección de cálculo de determinante"""
    mat = generar_matriz_cuadrada(3)
    det, pasos = calcular_determinante_gauss(mat)
    
    contenido = [{
        'titulo': 'Matriz Original',
        'contenido': mostrar_matriz_latex(mat, 'A')
    }]
    
    contenido.extend(pasos)
    
    return {
        'titulo': 'Cálculo de Determinante por Eliminación Gaussiana',
        'subsecciones': contenido
    }

def generar_documento(nombre, contenido):
    """Genera el documento LaTeX con configuración mejorada"""
    doc = Document(nombre, documentclass='article', document_options=['12pt'])
    
    # Preámbulo con paquetes matemáticos
    doc.preamble.append(Command('usepackage', 'amsmath'))
    doc.preamble.append(Command('usepackage', 'amssymb'))
    doc.preamble.append(Command('usepackage', 'geometry'))
    doc.preamble.append(Command('geometry', 'a4paper, margin=1.5cm'))
    
    # Configuración del documento
    doc.preamble.append(Command('title', 'Operaciones con Matrices'))
    doc.preamble.append(Command('author', 'Generado automáticamente'))
    doc.preamble.append(Command('date', ''))
    doc.append(Command('maketitle'))
    
    for seccion in contenido:
        with doc.create(Section(seccion['titulo'])):
            if 'subsecciones' in seccion:
                for subsec in seccion['subsecciones']:
                    with doc.create(Subsection(subsec['titulo'])):
                        doc.append(subsec['contenido'])
            else:
                doc.append(seccion['contenido'])
    
    doc.generate_pdf(clean_tex=True, compiler='pdflatex')
    return doc

def main():
    """Función principal"""
    np.random.seed(42)  # Para resultados reproducibles
    np.set_printoptions(precision=3, suppress=True)
    
    contenido = [
        seccion_matrices_aleatorias(),
        seccion_determinante()
    ]
    
    try:
        doc = generar_documento('operaciones_matrices', contenido)
        print("Documento generado exitosamente como 'operaciones_matrices.pdf'")
    except Exception as e:
        print(f"Error al generar el documento: {str(e)}")

if __name__ == '__main__':
    main()