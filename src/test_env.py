import sys
import numpy as np
import sweetviz as sv

print("✅ Ambiente virtual em uso:")
print(sys.executable)   # mostra o caminho do Python ativo (.venv/bin/python)

print("\n✅ Teste NumPy:")
a = np.array([1, 2, 3])
print("Array:", a)
print("Soma:", np.sum(a))

print("\n✅ Teste Sweetviz:")
print("Versão Sweetviz:", sv.__version__)