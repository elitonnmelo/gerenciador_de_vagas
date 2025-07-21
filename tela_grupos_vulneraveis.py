import panel as pn
import pandas as pd
from database import SessionLocal
from sqlalchemy.exc import IntegrityError
from models import GrupoVulneravel, Candidato, CandidatoGrupo
import datetime

pn.extension()

def tela_grupos_vulneraveis():
    id_grupo_in = pn.widgets.TextInput(name="ID do Grupo (para Buscar/Atualizar/Deletar)", placeholder="Gerado automaticamente ao criar")
    nome_in = pn.widgets.TextInput(name="Nome do Grupo", placeholder="Ex: Pessoas com deficiência")
    desc_in = pn.widgets.TextAreaInput(name="Descrição do Grupo", placeholder="Descreva o grupo vulnerável", height=100)

    msg = pn.pane.Markdown("")
    tabela_grupos = pn.pane.DataFrame(name="Lista de Grupos Vulneráveis", width=800, height=200)

    cands_grupo_assoc_df = pn.pane.DataFrame(name="Associações Candidato-Grupo", width=800, height=200)

    cpf_assoc_in = pn.widgets.TextInput(name="CPF do Candidato na Associação", placeholder="CPF do candidato")
    id_grupo_assoc_in = pn.widgets.TextInput(name="ID do Grupo na Associação", placeholder="ID do grupo")

    status_val_assoc_sel = pn.widgets.Select(name="Novo Status de Validação", options=["em análise", "validado", "rejeitado"])
    comp_assoc_in = pn.widgets.TextInput(name="Novo Comprovante (URL/Texto)", placeholder="Link para documento ou descrição (opcional)")

    btn_upd_assoc = pn.widgets.Button(name="Atualizar Associação", button_type="warning")
    btn_rem_assoc = pn.widgets.Button(name="Remover Associação", button_type="danger")
    msg_assoc = pn.pane.Markdown("")


    def carregar_todos_grupos():
        db = SessionLocal()
        try:
            grupos = db.query(GrupoVulneravel).all()
            grupos_data = []
            for g in grupos:
                grupos_data.append({
                    'ID Grupo': g.id_grupo,
                    'Nome': g.nome,
                    'Descrição': g.descricao
                })
            tabela_grupos.object = pd.DataFrame(grupos_data)
        except Exception as e:
            msg.object = f"Erro ao carregar grupos: {e}"
        finally:
            db.close()

    def carregar_assocs_cand_grupo():
        db = SessionLocal()
        try:
            assocs = db.query(CandidatoGrupo).all()
            assocs_data = []
            for assoc in assocs:
                cand = db.query(Candidato).filter(Candidato.cpf == assoc.cpf_candidato).first()
                grupo = db.query(GrupoVulneravel).filter(GrupoVulneravel.id_grupo == assoc.id_grupo).first()
                
                nome_cand = cand.nome if cand else "Candidato Desconhecido"
                nome_grupo = grupo.nome if grupo else "Grupo Desconhecido"

                assocs_data.append({
                    'CPF Candidato': assoc.cpf_candidato,
                    'Nome Candidato': nome_cand,
                    'ID Grupo': assoc.id_grupo,
                    'Nome Grupo': nome_grupo,
                    'Comprovante': assoc.comprovante,
                    'Data Inclusão': assoc.data_inclusao,
                    'Status Validação': assoc.status_validacao
                })
            cands_grupo_assoc_df.object = pd.DataFrame(assocs_data)
        except Exception as e:
            msg_assoc.object = f"Erro ao carregar associações: {e}"
        finally:
            db.close()

    def limpar_campos_grupo():
        id_grupo_in.value = ""
        nome_in.value = ""
        desc_in.value = ""
        msg.object = ""

    def limpar_campos_assoc():
        cpf_assoc_in.value = ""
        id_grupo_assoc_in.value = ""
        status_val_assoc_sel.value = "em análise"
        comp_assoc_in.value = ""
        msg_assoc.object = ""


    def criar_grupo_func(event=None):
        db = SessionLocal()
        try:
            novo_grupo = GrupoVulneravel(
                nome=nome_in.value,
                descricao=desc_in.value
            )
            db.add(novo_grupo)
            db.commit()
            msg.object = "Grupo vulnerável criado com sucesso!"
            limpar_campos_grupo()
            carregar_todos_grupos()
            carregar_assocs_cand_grupo()
        except IntegrityError:
            db.rollback()
            msg.object = "Erro: Nome do Grupo já existe ou violação de integridade."
        except Exception as e:
            db.rollback()
            msg.object = f"Erro ao criar grupo: {e}"
        finally:
            db.close()

    def buscar_grupo_func(event=None):
        db = SessionLocal()
        try:
            if not id_grupo_in.value:
                msg.object = "Por favor, digite o ID do Grupo para buscar."
                return

            grupo_id = int(id_grupo_in.value)
            grupo = db.query(GrupoVulneravel).filter(GrupoVulneravel.id_grupo == grupo_id).first()

            if grupo:
                nome_in.value = grupo.nome
                desc_in.value = grupo.descricao
                msg.object = "Grupo encontrado!"
            else:
                msg.object = "Grupo não encontrado."
                limpar_campos_grupo()
        except ValueError:
            msg.object = "ID do Grupo inválido. Digite um número."
        except Exception as e:
            msg.object = f"Erro ao buscar grupo: {e}"
        finally:
            db.close()

    def upd_grupo_func(event=None):
        db = SessionLocal()
        try:
            if not id_grupo_in.value:
                msg.object = "Por favor, digite o ID do Grupo para atualizar."
                return

            grupo_id = int(id_grupo_in.value)
            grupo = db.query(GrupoVulneravel).filter(GrupoVulneravel.id_grupo == grupo_id).first()

            if grupo:
                grupo.nome = nome_in.value
                grupo.descricao = desc_in.value
                db.commit()
                msg.object = "Grupo atualizado com sucesso!"
                carregar_todos_grupos()
                carregar_assocs_cand_grupo()
            else:
                msg.object = "Grupo não encontrado para atualização."
        except ValueError:
            msg.object = "ID do Grupo inválido. Digite um número."
        except Exception as e:
            db.rollback()
            msg.object = f"Erro ao atualizar grupo: {e}"
        finally:
            db.close()

    def del_grupo_func(event=None):
        db = SessionLocal()
        try:
            if not id_grupo_in.value:
                msg.object = "Por favor, digite o ID do Grupo para deletar."
                return

            grupo_id = int(id_grupo_in.value)
            grupo = db.query(GrupoVulneravel).filter(GrupoVulneravel.id_grupo == grupo_id).first()

            if grupo:
                db.delete(grupo)
                db.commit()
                msg.object = "Grupo deletado com sucesso!"
                limpar_campos_grupo()
                carregar_todos_grupos()
                carregar_assocs_cand_grupo()
            else:
                msg.object = "Grupo não encontrado para exclusão."
        except IntegrityError:
            db.rollback()
            msg.object = "Não é possível deletar: este grupo está relacionado a vagas ou candidatos."
        except ValueError:
            msg.object = "ID do Grupo inválido. Digite um número."
        except Exception as e:
            db.rollback()
            msg.object = f"Erro ao deletar grupo: {e}"
        finally:
            db.close()


    def upd_assoc_func(event=None):
        db = SessionLocal()
        try:
            cpf = cpf_assoc_in.value
            grupo_id = int(id_grupo_assoc_in.value)

            if not cpf or not id_grupo_assoc_in.value:
                msg_assoc.object = "Preencha o CPF do Candidato e o ID do Grupo."
                return

            assoc = db.query(CandidatoGrupo).filter(
                CandidatoGrupo.cpf_candidato == cpf,
                CandidatoGrupo.id_grupo == grupo_id
            ).first()

            if assoc:
                assoc.status_validacao = status_val_assoc_sel.value
                assoc.comprovante = comp_assoc_in.value if comp_assoc_in.value else None
                db.commit()
                msg_assoc.object = "Associação atualizada com sucesso!"
                carregar_assocs_cand_grupo()
            else:
                msg_assoc.object = "Associação não encontrada para o CPF e ID do Grupo informados."
        except ValueError:
            msg_assoc.object = "ID do Grupo inválido. Digite um número."
        except Exception as e:
            db.rollback()
            msg_assoc.object = f"Erro ao atualizar associação: {e}"
        finally:
            db.close()

    def rem_assoc_func(event=None):
        db = SessionLocal()
        try:
            cpf = cpf_assoc_in.value
            grupo_id = int(id_grupo_assoc_in.value)

            if not cpf or not id_grupo_assoc_in.value:
                msg_assoc.object = "Preencha o CPF do Candidato e o ID do Grupo para remover."
                return

            assoc = db.query(CandidatoGrupo).filter(
                CandidatoGrupo.cpf_candidato == cpf,
                CandidatoGrupo.id_grupo == grupo_id
            ).first()

            if assoc:
                db.delete(assoc)
                db.commit()
                msg_assoc.object = "Associação removida com sucesso!"
                limpar_campos_assoc()
                carregar_assocs_cand_grupo()
            else:
                msg_assoc.object = "Associação não encontrada para o CPF e ID do Grupo informados."
        except ValueError:
            msg_assoc.object = "ID do Grupo inválido. Digite um número."
        except Exception as e:
            db.rollback()
            msg_assoc.object = f"Erro ao remover associação: {e}"
        finally:
            db.close()


    btn_criar_grupo = pn.widgets.Button(name="Criar Grupo", button_type="success")
    btn_criar_grupo.on_click(criar_grupo_func)

    btn_buscar_grupo = pn.widgets.Button(name="Buscar Grupo", button_type="primary")
    btn_buscar_grupo.on_click(buscar_grupo_func)

    btn_upd_grupo = pn.widgets.Button(name="Atualizar Grupo", button_type="warning")
    btn_upd_grupo.on_click(upd_grupo_func)

    btn_del_grupo = pn.widgets.Button(name="Deletar Grupo", button_type="danger")
    btn_del_grupo.on_click(del_grupo_func)

    btn_limpar_grupo_campos = pn.widgets.Button(name="Limpar Campos Grupo", button_type="default")
    btn_limpar_grupo_campos.on_click(lambda event: limpar_campos_grupo())

    btn_upd_assoc.on_click(upd_assoc_func)
    btn_rem_assoc.on_click(rem_assoc_func)


    btns_crud_grupo = pn.Row(btn_criar_grupo, btn_buscar_grupo, btn_upd_grupo, btn_del_grupo, btn_limpar_grupo_campos)

    abas_princ = pn.Tabs(
        ("Gerenciar Grupos", pn.Column(
            "## Gerenciamento de Grupos Vulneráveis",
            id_grupo_in,
            nome_in,
            desc_in,
            btns_crud_grupo,
            msg,
            pn.layout.Divider(),
            "### Todos os Grupos Cadastrados",
            tabela_grupos
        )),
        ("Gerenciar Associações Candidato-Grupo", pn.Column(
            "## Gerenciar Associações de Candidatos a Grupos",
            cands_grupo_assoc_df,
            pn.layout.Divider(),
            "### Atualizar ou Remover Associação",
            pn.Row(cpf_assoc_in, id_grupo_assoc_in),
            status_val_assoc_sel,
            comp_assoc_in,
            pn.Row(btn_upd_assoc, btn_rem_assoc),
            msg_assoc
        )),
    )

    carregar_todos_grupos()
    carregar_assocs_cand_grupo()

    return abas_princ
