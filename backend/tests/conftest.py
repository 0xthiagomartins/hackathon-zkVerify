import sys
import os
from pathlib import Path

# Adicionar o diretório raiz do projeto ao PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))
