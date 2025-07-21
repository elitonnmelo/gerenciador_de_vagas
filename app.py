import panel as pn

from tela_candidato import tela_candidato
from tela_empresa import tela_empresa
from tela_cursos import tela_cursos
from tela_grupos_vulneraveis import tela_grupos_vulneraveis 

pn.extension()

app = pn.Tabs(
    ("Candidatos", tela_candidato()),
    ("Empresas", tela_empresa()),
    ("Cursos", tela_cursos()),
    ("Grupos Vulneráveis", tela_grupos_vulneraveis()),

)

app.servable()
