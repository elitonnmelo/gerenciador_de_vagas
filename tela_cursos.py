import panel as pn
import pandas as pd
from database import SessionLocal
from sqlalchemy.exc import IntegrityError
from models import Curso, InscricaoCurso, Candidato
import datetime

pn.extension()

def tela_cursos():
    id_curso_in = pn.widgets.TextInput(name="ID do Curso (para Buscar/Atualizar/Deletar)", placeholder="Gerado automaticamente ao criar")
    titulo_in = pn.widgets.TextInput(name="Título do Curso")
    desc_in = pn.widgets.TextAreaInput(name="Descrição", height=100)
    carga_h_in = pn.widgets.IntInput(name="Carga Horária")
    modalidade_in = pn.widgets.TextInput(name="Modalidade")
    inst_in = pn.widgets.TextInput(name="Instituição")
    link_in = pn.widgets.TextInput(name="Link")

    msg = pn.pane.Markdown("")

    insc_df = pn.pane.DataFrame(name="Inscrições no Curso", width=800, height=200)

    _curr_id_curso = None

    cands_disp_sel = pn.widgets.Select(name="Candidato para Inscrição", options={})
    btn_ins_cand_curso = pn.widgets.Button(name="Inscrever Candidato", button_type="primary", disabled=True)
    msg_ins_cand_curso = pn.pane.Markdown()

    insc_cpf_ger_in = pn.widgets.TextInput(name="CPF do Candidato na Inscrição", placeholder="CPF do candidato")
    insc_status_upd_sel = pn.widgets.Select(name="Novo Status da Inscrição", options=["em andamento", "concluído"])
    insc_aval_in = pn.widgets.TextAreaInput(name="Comentário / Avaliação", height=80)
    btn_upd_insc = pn.widgets.Button(name="Atualizar Inscrição", button_type="warning", disabled=True)
    btn_canc_insc = pn.widgets.Button(name="Cancelar Inscrição", button_type="danger", disabled=True)
    msg_ger_insc = pn.pane.Markdown()


    def hab_campos_curso(habilitar=True):
        titulo_in.disabled = not habilitar
        desc_in.disabled = not habilitar
        carga_h_in.disabled = not habilitar
        modalidade_in.disabled = not habilitar
        inst_in.disabled = not habilitar
        link_in.disabled = not habilitar

    def hab_btns_insc(habilitar=True):
        btn_ins_cand_curso.disabled = not habilitar
        cands_disp_sel.disabled = not habilitar
        insc_cpf_ger_in.disabled = not habilitar
        insc_status_upd_sel.disabled = not habilitar
        insc_aval_in.disabled = not habilitar
        btn_upd_insc.disabled = not habilitar
        btn_canc_insc.disabled = not habilitar

    def limpar_campos_curso():
        id_curso_in.value = ""
        titulo_in.value = ""
        desc_in.value = ""
        carga_h_in.value = 0
        modalidade_in.value = ""
        inst_in.value = ""
        link_in.value = ""
        msg.object = ""

    def limpar_campos_insc():
        cands_disp_sel.options = {}
        cands_disp_sel.value = None
        msg_ins_cand_curso.object = ""
        insc_cpf_ger_in.value = ""
        insc_status_upd_sel.value = "em andamento"
        insc_aval_in.value = ""
        msg_ger_insc.object = ""

    def carregar_cands_disp():
        db = SessionLocal()
        try:
            cands = db.query(Candidato).all()
            cands_options = {f"{c.nome} (CPF: {c.cpf})": c.cpf for c in cands}
            cands_disp_sel.options = cands_options
            if cands_options:
                cands_disp_sel.value = list(cands_options.values())[0]
            else:
                cands_disp_sel.value = None
        except Exception as e:
            print(f"Erro ao carregar candidatos: {e}")
            cands_disp_sel.options = {"Nenhum candidato disponível": None}
            cands_disp_sel.value = None
        finally:
            db.close()


    def ins_cand_curso(event=None):
        nonlocal _curr_id_curso
        if not _curr_id_curso:
            msg_ins_cand_curso.object = "Por favor, busque um curso primeiro."
            return

        cpf_cand_sel = cands_disp_sel.value
        if not cpf_cand_sel:
            msg_ins_cand_curso.object = "Por favor, selecione um candidato."
            return

        db = SessionLocal()
        try:
            insc_existente = db.query(InscricaoCurso).filter(
                InscricaoCurso.cpf_candidato == cpf_cand_sel,
                InscricaoCurso.id_curso == _curr_id_curso
            ).first()

            if insc_existente:
                msg_ins_cand_curso.object = "Candidato já está inscrito neste curso."
            else:
                nova_insc = InscricaoCurso(
                    cpf_candidato=cpf_cand_sel,
                    id_curso=_curr_id_curso,
                    data_inscricao=datetime.date.today(),
                    comentario_avaliacao=None,
                    status="em andamento"
                )
                db.add(nova_insc)
                db.commit()
                msg_ins_cand_curso.object = "Candidato inscrito no curso com sucesso!"
                buscar_curso(update_only_extras=True)
        except Exception as e:
            db.rollback()
            msg_ins_cand_curso.object = f"Erro ao inscrever candidato: {e}"
        finally:
            db.close()

    def upd_insc_curso(event=None):
        nonlocal _curr_id_curso
        if not _curr_id_curso:
            msg_ger_insc.object = "Por favor, busque um curso primeiro."
            return
        if not insc_cpf_ger_in.value:
            msg_ger_insc.object = "Por favor, digite o CPF do candidato para gerenciar a inscrição."
            return

        db = SessionLocal()
        try:
            insc = db.query(InscricaoCurso).filter(
                InscricaoCurso.cpf_candidato == insc_cpf_ger_in.value,
                InscricaoCurso.id_curso == _curr_id_curso
            ).first()

            if insc:
                insc.status = insc_status_upd_sel.value
                insc.comentario_avaliacao = insc_aval_in.value
                db.commit()
                msg_ger_insc.object = "Inscrição atualizada com sucesso!"
                buscar_curso(update_only_extras=True)
            else:
                msg_ger_insc.object = "Inscrição não encontrada para este curso e candidato."
        except Exception as e:
            db.rollback()
            msg_ger_insc.object = f"Erro ao atualizar inscrição: {e}"
        finally:
            db.close()

    def canc_insc_curso(event=None):
        nonlocal _curr_id_curso
        if not _curr_id_curso:
            msg_ger_insc.object = "Por favor, busque um curso primeiro."
            return
        if not insc_cpf_ger_in.value:
            msg_ger_insc.object = "Por favor, digite o CPF do candidato para cancelar a inscrição."
            return

        db = SessionLocal()
        try:
            insc = db.query(InscricaoCurso).filter(
                InscricaoCurso.cpf_candidato == insc_cpf_ger_in.value,
                InscricaoCurso.id_curso == _curr_id_curso
            ).first()

            if insc:
                db.delete(insc)
                db.commit()
                msg_ger_insc.object = "Inscrição cancelada com sucesso!"
                limpar_campos_insc()
                buscar_curso(update_only_extras=True)
            else:
                msg_ger_insc.object = "Inscrição não encontrada para este curso e candidato."
        except Exception as e:
            db.rollback()
            msg_ger_insc.object = f"Erro ao cancelar inscrição: {e}"
        finally:
            db.close()


    def criar_curso(event=None):
        db = SessionLocal()
        try:
            curso = Curso(
                titulo=titulo_in.value,
                descricao=desc_in.value,
                carga_horaria=carga_h_in.value,
                modalidade=modalidade_in.value,
                instituicao=inst_in.value,
                link=link_in.value
            )
            db.add(curso)
            db.commit()
            msg.object = "Curso criado com sucesso!"
            limpar_campos_curso()
        except IntegrityError:
            db.rollback()
            msg.object = "Erro: ID do Curso já existe ou violação de integridade."
        except Exception as e:
            db.rollback()
            msg.object = f"Erro ao criar curso: {e}"
        finally:
            db.close()

    def buscar_curso(event=None, update_only_extras=False):
        nonlocal _curr_id_curso
        db = SessionLocal()
        try:
            curso = db.query(Curso).filter(Curso.id_curso == int(id_curso_in.value)).first()
            if curso:
                _curr_id_curso = curso.id_curso

                if not update_only_extras:
                    titulo_in.value = curso.titulo
                    desc_in.value = curso.descricao
                    carga_h_in.value = curso.carga_horaria
                    modalidade_in.value = curso.modalidade
                    inst_in.value = curso.instituicao
                    link_in.value = curso.link
                    msg.object = "Curso encontrado!"
                    hab_campos_curso(False)

                insc_data = []
                for insc in curso.inscricoes:
                    cand = db.query(Candidato).filter(Candidato.cpf == insc.cpf_candidato).first()
                    nome_cand = cand.nome if cand else "Candidato Desconhecido"
                    insc_data.append({
                        'CPF Candidato': insc.cpf_candidato,
                        'Nome Candidato': nome_cand,
                        'Data Inscrição': insc.data_inscricao,
                        'Status': insc.status,
                        'Avaliação': insc.comentario_avaliacao
                    })
                insc_df.object = pd.DataFrame(insc_data)
                hab_btns_insc(True)
                carregar_cands_disp()

            else:
                _curr_id_curso = None
                msg.object = "Curso não encontrado."
                limpar_campos_curso()
                limpar_campos_insc()
                hab_campos_curso(True)
                hab_btns_insc(False)
        except ValueError:
            msg.object = "ID do Curso inválido. Digite um número."
            limpar_campos_curso()
            limpar_campos_insc()
            hab_campos_curso(True)
            hab_btns_insc(False)
        except Exception as e:
            msg.object = f"Erro ao buscar curso: {e}"
            limpar_campos_curso()
            limpar_campos_insc()
            hab_campos_curso(True)
            hab_btns_insc(False)
        finally:
            db.close()

    def atualizar_curso(event=None):
        db = SessionLocal()
        try:
            curso = db.query(Curso).filter(Curso.id_curso == int(id_curso_in.value)).first()
            if curso:
                curso.titulo = titulo_in.value
                curso.descricao = desc_in.value
                curso.carga_horaria = carga_h_in.value
                curso.modalidade = modalidade_in.value
                curso.instituicao = inst_in.value
                curso.link = link_in.value
                db.commit()
                msg.object = "Curso atualizado com sucesso!"
            else:
                msg.object = "Curso não encontrado."
        except ValueError:
            msg.object = "ID do Curso inválido. Digite um número."
        except Exception as e:
            db.rollback()
            msg.object = f"Erro ao atualizar curso: {e}"
        finally:
            db.close()

    def deletar_curso(event=None):
        nonlocal _curr_id_curso
        db = SessionLocal()
        try:
            curso = db.query(Curso).filter(Curso.id_curso == int(id_curso_in.value)).first()
            if curso:
                db.delete(curso)
                db.commit()
                msg.object = "Curso deletado com sucesso!"
                limpar_campos_curso()
                limpar_campos_insc()
                _curr_id_curso = None
                hab_campos_curso(True)
                hab_btns_insc(False)
            else:
                msg.object = "Curso não encontrado para deletar."
        except IntegrityError:
            db.rollback()
            msg.object = "Não é possível deletar: este curso está relacionado a inscrições."
        except ValueError:
            msg.object = "ID do Curso inválido. Digite um número."
        except Exception as e:
            db.rollback()
            msg.object = f"Erro ao deletar curso: {e}"
        finally:
            db.close()

    btn_criar_curso = pn.widgets.Button(name="Criar", button_type="success")
    btn_criar_curso.on_click(criar_curso)

    btn_buscar_curso = pn.widgets.Button(name="Buscar", button_type="primary")
    btn_buscar_curso.on_click(buscar_curso)

    btn_atualizar_curso = pn.widgets.Button(name="Atualizar", button_type="warning")
    btn_atualizar_curso.on_click(atualizar_curso)

    btn_deletar_curso = pn.widgets.Button(name="Deletar", button_type="danger")
    btn_deletar_curso.on_click(deletar_curso)

    btn_limpar_curso_campos = pn.widgets.Button(name="Limpar Campos", button_type="default")
    btn_limpar_curso_campos.on_click(lambda event: limpar_campos_curso())

    btn_ins_cand_curso.on_click(ins_cand_curso)
    btn_upd_insc.on_click(upd_insc_curso)
    btn_canc_insc.on_click(canc_insc_curso)


    btns_crud_curso = pn.Row(btn_criar_curso, btn_buscar_curso, btn_atualizar_curso, btn_deletar_curso, btn_limpar_curso_campos)

    abas_ext = pn.Tabs(
        ("Inscrições no Curso", pn.Column(
            insc_df,
            pn.layout.Divider(),
            "### Gerenciar Inscrição Existente",
            insc_cpf_ger_in,
            insc_status_upd_sel,
            insc_aval_in,
            pn.Row(btn_upd_insc, btn_canc_insc),
            msg_ger_insc
        )),
        ("Inscrever Candidato", pn.Column(
            "### Inscrever Candidato em Curso",
            cands_disp_sel,
            btn_ins_cand_curso,
            msg_ins_cand_curso
        )),
    )

    hab_campos_curso(True)
    hab_btns_insc(False)


    return pn.Column(
        "# Gerenciamento de Cursos",
        id_curso_in,
        pn.Column(
            titulo_in, desc_in, carga_h_in,
            modalidade_in, inst_in, link_in,
            sizing_mode="stretch_width"
        ),
        btns_crud_curso, msg,
        pn.layout.Divider(),
        "## Informações Relacionadas e Ações",
        abas_ext
    )
