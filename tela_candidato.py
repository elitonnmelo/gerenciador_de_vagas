import panel as pn
import pandas as pd
from database import SessionLocal
from sqlalchemy.exc import IntegrityError
from models import Candidato, Candidatura, Curso, InscricaoCurso, Vaga, Denuncia, GrupoVulneravel, CandidatoGrupo
import datetime

pn.extension()

def tela_candidato():
    cpf_in = pn.widgets.TextInput(name="CPF do Candidato")
    nome_in = pn.widgets.TextInput(name="Nome")
    email_in = pn.widgets.TextInput(name="Email")
    tel_in = pn.widgets.TextInput(name="Telefone")
    pret_in = pn.widgets.FloatInput(name="Pretensão Salarial")
    end_in = pn.widgets.TextInput(name="Endereço")
    nasc_in = pn.widgets.DatePicker(name="Data de Nascimento")
    curr_in = pn.widgets.TextAreaInput(name="Currículo")

    msg = pn.pane.Markdown()

    cand_df = pn.pane.DataFrame(name="Candidaturas", width=800, height=200)
    cursos_insc_df = pn.pane.DataFrame(name="Cursos Inscritos", width=800, height=200)
    den_df = pn.pane.DataFrame(name="Denúncias", width=800, height=200)
    grupos_cand_df = pn.pane.DataFrame(name="Grupos Vulneráveis", width=800, height=200)

    _curr_cpf = None

    vagas_disp_sel = pn.widgets.Select(name="Vagas Disponíveis", options=[])
    btn_ins_vaga = pn.widgets.Button(name="Inscrever-se na Vaga", button_type="primary", disabled=True)
    msg_ins_vaga = pn.pane.Markdown()

    cand_id_canc_in = pn.widgets.TextInput(name="ID da Vaga para Cancelar Candidatura", placeholder="Ex: 1")
    btn_canc_cand = pn.widgets.Button(name="Cancelar Candidatura", button_type="danger", disabled=True)
    msg_canc_cand = pn.pane.Markdown()

    cursos_disp_sel = pn.widgets.Select(name="Cursos Disponíveis", options=[])
    btn_ins_curso = pn.widgets.Button(name="Inscrever-se no Curso", button_type="primary", disabled=True)
    msg_ins_curso = pn.pane.Markdown()

    insc_curso_id_ger_in = pn.widgets.TextInput(name="ID do Curso para Gerenciar Inscrição", placeholder="Ex: 1")
    status_curso_upd_sel = pn.widgets.Select(name="Novo Status", options=["em andamento", "concluído"])
    btn_upd_status_curso = pn.widgets.Button(name="Atualizar Status do Curso", button_type="warning", disabled=True)
    btn_canc_insc_curso = pn.widgets.Button(name="Cancelar Inscrição no Curso", button_type="danger", disabled=True)
    msg_ger_curso = pn.pane.Markdown()

    den_vaga_sel = pn.widgets.Select(name="Vaga Relacionada (Opcional)", options={"Nenhuma": None})
    den_desc_in = pn.widgets.TextAreaInput(name="Descrição da Denúncia", placeholder="Descreva a situação...", height=100)
    btn_fazer_den = pn.widgets.Button(name="Fazer Denúncia", button_type="danger", disabled=True)
    msg_den = pn.pane.Markdown()

    grupos_vul_sel = pn.widgets.Select(name="Grupo Vulnerável", options={})
    comp_grupo_in = pn.widgets.TextInput(name="Comprovante (URL/Texto)", placeholder="Link para documento ou descrição")
    btn_add_grupo = pn.widgets.Button(name="Inscrever-se no Grupo", button_type="success", disabled=True)
    msg_grupos = pn.pane.Markdown()

    grupo_id_rem_in = pn.widgets.TextInput(name="ID do Grupo para Sair", placeholder="Ex: 1")
    btn_rem_grupo = pn.widgets.Button(name="Sair do Grupo", button_type="danger", disabled=True)


    def hab_campos_cand(habilitar=True):
        nome_in.disabled = not habilitar
        email_in.disabled = not habilitar
        tel_in.disabled = not habilitar
        pret_in.disabled = not habilitar
        end_in.disabled = not habilitar
        nasc_in.disabled = not habilitar
        curr_in.disabled = not habilitar

    def carregar_vagas_disp():
        db = SessionLocal()
        try:
            vagas = db.query(Vaga).filter(Vaga.status_vaga == "aberta").all()
            vagas_options = {f"{v.titulo} (ID: {v.id_vaga})": v.id_vaga for v in vagas}
            vagas_disp_sel.options = vagas_options
            if vagas_options:
                vagas_disp_sel.value = list(vagas_options.values())[0]
            else:
                vagas_disp_sel.value = None
            den_vaga_sel.options = {"Nenhuma": None, **vagas_options}
        except Exception as e:
            print(f"Erro ao carregar vagas: {e}")
            vagas_disp_sel.options = {"Nenhuma vaga disponível": None}
            vagas_disp_sel.value = None
            den_vaga_sel.options = {"Nenhuma": None}
        finally:
            db.close()

    def carregar_cursos_disp():
        db = SessionLocal()
        try:
            cursos = db.query(Curso).all()
            cursos_options = {f"{c.titulo} (ID: {c.id_curso})": c.id_curso for c in cursos}
            cursos_disp_sel.options = cursos_options
            if cursos_options:
                cursos_disp_sel.value = list(cursos_options.values())[0]
            else:
                cursos_disp_sel.value = None
        except Exception as e:
            print(f"Erro ao carregar cursos: {e}")
            cursos_disp_sel.options = {"Nenhum curso disponível": None}
            cursos_disp_sel.value = None
        finally:
            db.close()

    def carregar_grupos_vul():
        db = SessionLocal()
        try:
            grupos = db.query(GrupoVulneravel).all()
            grupos_options = {f"{g.nome} (ID: {g.id_grupo})": g.id_grupo for g in grupos}
            grupos_vul_sel.options = grupos_options
            if grupos_options:
                grupos_vul_sel.value = list(grupos_options.values())[0]
            else:
                grupos_vul_sel.value = None
        except Exception as e:
            print(f"Erro ao carregar grupos vulneráveis: {e}")
            grupos_vul_sel.options = {"Nenhum grupo disponível": None}
            grupos_vul_sel.value = None
        finally:
            db.close()

    def _carregar_cand_data(db, candidato_obj):
        cand_data = []
        for cand in candidato_obj.candidaturas:
            vaga = db.query(Vaga).filter(Vaga.id_vaga == cand.id_vaga).first()
            titulo_vaga = vaga.titulo if vaga else "Vaga Desconhecida"
            cand_data.append({
                'ID Vaga': cand.id_vaga,
                'Vaga': titulo_vaga,
                'Data Candidatura': cand.data_candidatura,
                'Status': cand.status,
                'Feedback Empresa': cand.feedback_empresa
            })
        return cand_data

    def _carregar_cursos_insc_data(db, candidato_obj):
        cursos_data = []
        for insc in candidato_obj.inscricoes_cursos:
            curso = db.query(Curso).filter(Curso.id_curso == insc.id_curso).first()
            titulo_curso = curso.titulo if curso else "Curso Desconhecido"
            cursos_data.append({
                'ID Curso': insc.id_curso,
                'Curso': titulo_curso,
                'Data Inscrição': insc.data_inscricao,
                'Status': insc.status,
                'Avaliação': insc.comentario_avaliacao
            })
        return cursos_data

    def _carregar_den_data(db, candidato_obj):
        den_data = []
        for den in candidato_obj.denuncias:
            vaga_den = db.query(Vaga).filter(Vaga.id_vaga == den.id_vaga).first()
            titulo_vaga_den = vaga_den.titulo if vaga_den else "N/A"
            den_data.append({
                'ID Denúncia': den.id_denuncia,
                'Vaga': titulo_vaga_den,
                'Data Denúncia': den.data_denuncia,
                'Descrição': den.descricao,
                'Status': den.status_denuncia,
                'Ações Tomadas': den.acoes_tomadas
            })
        return den_data

    def _carregar_grupos_cand_data(db, candidato_obj):
        grupos_cand_data = []
        for cg in candidato_obj.grupos_candidato:
            grupo = db.query(GrupoVulneravel).filter(GrupoVulneravel.id_grupo == cg.id_grupo).first()
            nome_grupo = grupo.nome if grupo else "Grupo Desconhecido"
            grupos_cand_data.append({
                'ID Grupo': cg.id_grupo,
                'Nome do Grupo': nome_grupo,
                'Comprovante': cg.comprovante,
                'Data Inclusão': cg.data_inclusao,
                'Status Validação': cg.status_validacao
            })
        return grupos_cand_data


    def ins_vaga(event=None):
        nonlocal _curr_cpf
        if not _curr_cpf:
            msg_ins_vaga.object = "Por favor, busque um candidato primeiro."
            return

        id_vaga_sel = vagas_disp_sel.value
        if not id_vaga_sel:
            msg_ins_vaga.object = "Por favor, selecione uma vaga."
            return

        db = SessionLocal()
        try:
            cand_existente = db.query(Candidatura).filter(
                Candidatura.cpf_candidato == _curr_cpf,
                Candidatura.id_vaga == id_vaga_sel
            ).first()

            if cand_existente:
                msg_ins_vaga.object = "Candidato já se inscreveu nesta vaga."
            else:
                nova_cand = Candidatura(
                    cpf_candidato=_curr_cpf,
                    id_vaga=id_vaga_sel,
                    data_candidatura=datetime.date.today(),
                    status="Pendente",
                    feedback_empresa=None
                )
                db.add(nova_cand)
                db.commit()
                msg_ins_vaga.object = "Inscrição na vaga realizada com sucesso!"
                buscar_cand(update_only_extras=True)
        except Exception as e:
            db.rollback()
            msg_ins_vaga.object = f"Erro ao se inscrever na vaga: {e}"
        finally:
            db.close()

    def canc_cand(event=None):
        nonlocal _curr_cpf
        if not _curr_cpf:
            msg_canc_cand.object = "Por favor, busque um candidato primeiro."
            return

        try:
            id_vaga_para_canc = int(cand_id_canc_in.value)
        except ValueError:
            msg_canc_cand.object = "ID da Vaga inválido. Digite um número."
            return

        db = SessionLocal()
        try:
            cand = db.query(Candidatura).filter(
                Candidatura.cpf_candidato == _curr_cpf,
                Candidatura.id_vaga == id_vaga_para_canc
            ).first()

            if cand:
                cand.status = "Cancelada"
                db.commit()
                msg_canc_cand.object = "Candidatura cancelada com sucesso!"
                buscar_cand(update_only_extras=True)
            else:
                msg_canc_cand.object = "Candidatura não encontrada para este candidato e vaga."
        except Exception as e:
            db.rollback()
            msg_canc_cand.object = f"Erro ao cancelar candidatura: {e}"
        finally:
            db.close()

    def ins_curso(event=None):
        nonlocal _curr_cpf
        if not _curr_cpf:
            msg_ins_curso.object = "Por favor, busque um candidato primeiro."
            return

        id_curso_sel = cursos_disp_sel.value
        if not id_curso_sel:
            msg_ins_curso.object = "Por favor, selecione um curso."
            return

        db = SessionLocal()
        try:
            insc_existente = db.query(InscricaoCurso).filter(
                InscricaoCurso.cpf_candidato == _curr_cpf,
                InscricaoCurso.id_curso == id_curso_sel
            ).first()

            if insc_existente:
                msg_ins_curso.object = "Candidato já está inscrito neste curso."
            else:
                nova_insc = InscricaoCurso(
                    cpf_candidato=_curr_cpf,
                    id_curso=id_curso_sel,
                    data_inscricao=datetime.date.today(),
                    comentario_avaliacao=None,
                    status="em andamento"
                )
                db.add(nova_insc)
                db.commit()
                msg_ins_curso.object = "Inscrição no curso realizada com sucesso!"
                buscar_cand(update_only_extras=True)
        except Exception as e:
            db.rollback()
            msg_ins_curso.object = f"Erro ao se inscrever no curso: {e}"
        finally:
            db.close()

    def alt_status_curso(event=None):
        nonlocal _curr_cpf
        if not _curr_cpf:
            msg_ger_curso.object = "Por favor, busque um candidato primeiro."
            return

        try:
            id_curso_ger = int(insc_curso_id_ger_in.value)
        except ValueError:
            msg_ger_curso.object = "ID do Curso inválido. Digite um número."
            return

        db = SessionLocal()
        try:
            insc = db.query(InscricaoCurso).filter(
                InscricaoCurso.cpf_candidato == _curr_cpf,
                InscricaoCurso.id_curso == id_curso_ger
            ).first()

            if insc:
                insc.status = status_curso_upd_sel.value
                db.commit()
                msg_ger_curso.object = "Status do curso atualizado com sucesso!"
                buscar_cand(update_only_extras=True)
            else:
                msg_ger_curso.object = "Inscrição no curso não encontrada para este candidato e curso."
        except Exception as e:
            db.rollback()
            msg_ger_curso.object = f"Erro ao atualizar status do curso: {e}"
        finally:
            db.close()

    def canc_insc_curso(event=None):
        nonlocal _curr_cpf
        if not _curr_cpf:
            msg_ger_curso.object = "Por favor, busque um candidato primeiro."
            return

        try:
            id_curso_ger = int(insc_curso_id_ger_in.value)
        except ValueError:
            msg_ger_curso.object = "ID do Curso inválido. Digite um número."
            return

        db = SessionLocal()
        try:
            insc = db.query(InscricaoCurso).filter(
                InscricaoCurso.cpf_candidato == _curr_cpf,
                InscricaoCurso.id_curso == id_curso_ger
            ).first()

            if insc:
                db.delete(insc)
                db.commit()
                msg_ger_curso.object = "Inscrição no curso cancelada com sucesso!"
                buscar_cand(update_only_extras=True)
            else:
                msg_ger_curso.object = "Inscrição no curso não encontrada para este candidato e curso."
        except Exception as e:
            db.rollback()
            msg_ger_curso.object = f"Erro ao cancelar inscrição no curso: {e}"
        finally:
            db.close()

    def fazer_den(event=None):
        nonlocal _curr_cpf
        if not _curr_cpf:
            msg_den.object = "Por favor, busque um candidato primeiro."
            return
        if not den_desc_in.value:
            msg_den.object = "A descrição da denúncia não pode estar vazia."
            return

        db = SessionLocal()
        try:
            nova_den = Denuncia(
                cpf_candidato=_curr_cpf,
                id_vaga=den_vaga_sel.value if den_vaga_sel.value else None,
                data_denuncia=datetime.date.today(),
                descricao=den_desc_in.value,
                status_denuncia="Aberta",
                acoes_tomadas=None
            )
            db.add(nova_den)
            db.commit()
            msg_den.object = "Denúncia registrada com sucesso!"
            den_desc_in.value = ""
            den_vaga_sel.value = None
            buscar_cand(update_only_extras=True)
        except Exception as e:
            db.rollback()
            msg_den.object = f"Erro ao registrar denúncia: {e}"
        finally:
            db.close()

    def add_grupo_cand(event=None):
        nonlocal _curr_cpf
        if not _curr_cpf:
            msg_grupos.object = "Por favor, busque um candidato primeiro."
            return
        if not grupos_vul_sel.value:
            msg_grupos.object = "Por favor, selecione um grupo."
            return

        id_grupo_sel = grupos_vul_sel.value
        comprovante = comp_grupo_in.value
        status_validacao = "em análise"

        db = SessionLocal()
        try:
            grupo_existente = db.query(CandidatoGrupo).filter(
                CandidatoGrupo.cpf_candidato == _curr_cpf,
                CandidatoGrupo.id_grupo == id_grupo_sel
            ).first()

            if grupo_existente:
                msg_grupos.object = "Candidato já está associado a este grupo."
            else:
                novo_grupo_cand = CandidatoGrupo(
                    cpf_candidato=_curr_cpf,
                    id_grupo=id_grupo_sel,
                    comprovante=comprovante if comprovante else None,
                    data_inclusao=datetime.date.today(),
                    status_validacao=status_validacao
                )
                db.add(novo_grupo_cand)
                db.commit()
                msg_grupos.object = "Inscrição no grupo realizada com sucesso! Status: Em Análise."
                comp_grupo_in.value = ""
                buscar_cand(update_only_extras=True)
        except Exception as e:
            db.rollback()
            msg_grupos.object = f"Erro ao inscrever-se no grupo: {e}"
        finally:
            db.close()

    def rem_grupo_cand(event=None):
        nonlocal _curr_cpf
        if not _curr_cpf:
            msg_grupos.object = "Por favor, busque um candidato primeiro."
            return

        try:
            id_grupo_para_rem = int(grupo_id_rem_in.value)
        except ValueError:
            msg_grupos.object = "ID do Grupo inválido. Digite um número."
            return

        db = SessionLocal()
        try:
            grupo_cand = db.query(CandidatoGrupo).filter(
                CandidatoGrupo.cpf_candidato == _curr_cpf,
                CandidatoGrupo.id_grupo == id_grupo_para_rem
            ).first()

            if grupo_cand:
                db.delete(grupo_cand)
                db.commit()
                msg_grupos.object = "Candidato saiu do grupo com sucesso!"
                grupo_id_rem_in.value = ""
                buscar_cand(update_only_extras=True)
            else:
                msg_grupos.object = "Associação de grupo não encontrada para este candidato e grupo."
        except Exception as e:
            db.rollback()
            msg_grupos.object = f"Erro ao sair do grupo: {e}"
        finally:
            db.close()


    def criar_cand(event=None):
        db = SessionLocal()
        try:
            cand = Candidato(
                cpf=cpf_in.value,
                nome=nome_in.value,
                email=email_in.value,
                telefone=tel_in.value,
                pretensao_salarial=pret_in.value,
                endereco=end_in.value,
                data_nascimento=nasc_in.value,
                curriculo=curr_in.value
            )
            db.add(cand)
            db.commit()
            msg.object = "Candidato criado com sucesso!"
            limpar_campos_cand()
        except IntegrityError:
            db.rollback()
            msg.object = "Erro: CPF já existe ou violação de integridade."
        except Exception as e:
            db.rollback()
            msg.object = f"Erro ao criar candidato: {e}"
        finally:
            db.close()


    def buscar_cand(event=None, update_only_extras=False):
        nonlocal _curr_cpf
        db = SessionLocal()
        try:
            c = db.query(Candidato).filter(Candidato.cpf == cpf_in.value).first()
            if c:
                _curr_cpf = c.cpf

                if not update_only_extras:
                    nome_in.value = c.nome
                    email_in.value = c.email
                    tel_in.value = c.telefone
                    pret_in.value = float(c.pretensao_salarial) if c.pretensao_salarial else 0.0
                    end_in.value = c.endereco
                    nasc_in.value = c.data_nascimento
                    curr_in.value = c.curriculo
                    msg.object = "Candidato encontrado."
                    hab_campos_cand(False)

                cand_df.object = pd.DataFrame(_carregar_cand_data(db, c))
                btn_canc_cand.disabled = cand_df.object.empty

                cursos_insc_df.object = pd.DataFrame(_carregar_cursos_insc_data(db, c))
                btn_upd_status_curso.disabled = cursos_insc_df.object.empty
                btn_canc_insc_curso.disabled = cursos_insc_df.object.empty

                den_df.object = pd.DataFrame(_carregar_den_data(db, c))

                grupos_cand_df.object = pd.DataFrame(_carregar_grupos_cand_data(db, c))
                btn_rem_grupo.disabled = grupos_cand_df.object.empty


                btn_ins_vaga.disabled = False
                btn_ins_curso.disabled = False
                btn_fazer_den.disabled = False
                btn_add_grupo.disabled = False

                carregar_vagas_disp()
                carregar_cursos_disp()
                carregar_grupos_vul()

            else:
                _curr_cpf = None
                msg.object = "Candidato não encontrado."
                limpar_campos_cand(apenas_dados_extras=True)
                hab_campos_cand(True)
                btn_ins_vaga.disabled = True
                vagas_disp_sel.options = []
                vagas_disp_sel.value = None
                btn_canc_cand.disabled = True
                cand_id_canc_in.value = ""

                btn_ins_curso.disabled = True
                cursos_disp_sel.options = []
                cursos_disp_sel.value = None
                btn_upd_status_curso.disabled = True
                btn_canc_insc_curso.disabled = True
                insc_curso_id_ger_in.value = ""

                btn_fazer_den.disabled = True
                den_vaga_sel.options = {"Nenhuma": None}
                den_desc_in.value = ""

                btn_add_grupo.disabled = True
                grupos_vul_sel.options = {}
                grupos_vul_sel.value = None
                comp_grupo_in.value = ""
                btn_rem_grupo.disabled = True
                grupo_id_rem_in.value = ""


        except Exception as e:
            msg.object = f"Erro ao buscar candidato: {e}"
            limpar_campos_cand(apenas_dados_extras=True)
            hab_campos_cand(True)
            btn_ins_vaga.disabled = True
            vagas_disp_sel.options = []
            vagas_disp_sel.value = None
            btn_canc_cand.disabled = True
            cand_id_canc_in.value = ""

            btn_ins_curso.disabled = True
            cursos_disp_sel.options = []
            cursos_disp_sel.value = None
            btn_upd_status_curso.disabled = True
            btn_canc_insc_curso.disabled = True
            insc_curso_id_ger_in.value = ""

            btn_fazer_den.disabled = True
            den_vaga_sel.options = {"Nenhuma": None}
            den_desc_in.value = ""

            btn_add_grupo.disabled = True
            grupos_vul_sel.options = {}
            grupos_vul_sel.value = None
            comp_grupo_in.value = ""
            btn_rem_grupo.disabled = True
            grupo_id_rem_in.value = ""
        finally:
            db.close()


    def atualizar_cand(event=None):
        db = SessionLocal()
        try:
            c = db.query(Candidato).filter(Candidato.cpf == cpf_in.value).first()
            if c:
                c.nome = nome_in.value
                c.email = email_in.value
                c.telefone = tel_in.value
                c.pretensao_salarial = pret_in.value
                c.endereco = end_in.value
                c.data_nascimento = nasc_in.value
                c.curriculo = curr_in.value
                db.commit()
                msg.object = "Candidato atualizado."
            else:
                msg.object = "CPF não encontrado para atualização."
        except Exception as e:
            db.rollback()
            msg.object = f"Erro ao atualizar candidato: {e}"
        finally:
            db.close()

    def deletar_cand(event=None):
        nonlocal _curr_cpf
        db = SessionLocal()
        try:
            c = db.query(Candidato).filter(Candidato.cpf == cpf_in.value).first()
            if c:
                db.delete(c)
                db.commit()
                msg.object = "Candidato deletado com sucesso."
                limpar_campos_cand()
                _curr_cpf = None
            else:
                msg.object = "CPF não encontrado para exclusão."
        except IntegrityError:
            db.rollback()
            msg.object = "Não é possível deletar: este candidato está relacionado a outras tabelas (candidaturas, cursos, denúncias, grupos)."
        except Exception as e:
            db.rollback()
            msg.object = f"Erro ao deletar candidato: {e}"
        finally:
            db.close()

    def limpar_campos_cand(apenas_dados_extras=False):
        nonlocal _curr_cpf
        if not apenas_dados_extras:
            cpf_in.value = ""
            nome_in.value = ""
            email_in.value = ""
            tel_in.value = ""
            pret_in.value = 0.0
            end_in.value = ""
            nasc_in.value = None
            curr_in.value = ""
            msg.object = ""
            _curr_cpf = None
            hab_campos_cand(True)

        cand_df.object = pd.DataFrame()
        cursos_insc_df.object = pd.DataFrame()
        den_df.object = pd.DataFrame()
        grupos_cand_df.object = pd.DataFrame()

        vagas_disp_sel.options = []
        vagas_disp_sel.value = None
        btn_ins_vaga.disabled = True
        msg_ins_vaga.object = ""

        cand_id_canc_in.value = ""
        btn_canc_cand.disabled = True
        msg_canc_cand.object = ""

        cursos_disp_sel.options = []
        cursos_disp_sel.value = None
        btn_ins_curso.disabled = True
        msg_ins_curso.object = ""

        insc_curso_id_ger_in.value = ""
        status_curso_upd_sel.value = "em andamento"
        btn_upd_status_curso.disabled = True
        btn_canc_insc_curso.disabled = True
        msg_ger_curso.object = ""

        den_vaga_sel.options = {"Nenhuma": None}
        den_vaga_sel.value = None
        den_desc_in.value = ""
        btn_fazer_den.disabled = True
        msg_den.object = ""

        grupos_vul_sel.options = {}
        grupos_vul_sel.value = None
        comp_grupo_in.value = ""
        btn_add_grupo.disabled = True
        msg_grupos.object = ""
        grupo_id_rem_in.value = ""
        btn_rem_grupo.disabled = True


    btn_criar_cand = pn.widgets.Button(name="Criar", button_type="success")
    btn_criar_cand.on_click(criar_cand)

    btn_buscar_cand = pn.widgets.Button(name="Buscar", button_type="primary")
    btn_buscar_cand.on_click(buscar_cand)

    btn_atualizar_cand = pn.widgets.Button(name="Atualizar", button_type="warning")
    btn_atualizar_cand.on_click(atualizar_cand)

    btn_deletar_cand = pn.widgets.Button(name="Deletar", button_type="danger")
    btn_deletar_cand.on_click(deletar_cand)

    btn_limpar_campos_cand = pn.widgets.Button(name="Limpar Campos", button_type="default")
    btn_limpar_campos_cand.on_click(lambda event: limpar_campos_cand())

    btn_ins_vaga.on_click(ins_vaga)
    btn_canc_cand.on_click(canc_cand)
    btn_ins_curso.on_click(ins_curso)
    btn_upd_status_curso.on_click(alt_status_curso)
    btn_canc_insc_curso.on_click(canc_insc_curso)
    btn_fazer_den.on_click(fazer_den)
    btn_add_grupo.on_click(add_grupo_cand)
    btn_rem_grupo.on_click(rem_grupo_cand)


    btns_crud_cand = pn.Row(btn_criar_cand, btn_buscar_cand, btn_atualizar_cand, btn_deletar_cand, btn_limpar_campos_cand)

    abas_ext = pn.Tabs(
        ("Candidaturas", pn.Column(
            cand_df,
            pn.layout.Divider(),
            "### Cancelar Candidatura Existente",
            cand_id_canc_in,
            btn_canc_cand,
            msg_canc_cand
        )),
        ("Cursos Inscritos", pn.Column(
            cursos_insc_df,
            pn.layout.Divider(),
            "### Gerenciar Inscrição em Curso",
            insc_curso_id_ger_in,
            status_curso_upd_sel,
            pn.Row(btn_upd_status_curso, btn_canc_insc_curso),
            msg_ger_curso
        )),
        ("Inscrever em Vaga", pn.Column(
            "### Inscrever-se em uma Nova Vaga",
            vagas_disp_sel,
            btn_ins_vaga,
            msg_ins_vaga
        )),
        ("Inscrever em Curso", pn.Column(
            "### Inscrever-se em um Novo Curso",
            cursos_disp_sel,
            btn_ins_curso,
            msg_ins_curso
        )),
        ("Denúncias", pn.Column(
            den_df,
            pn.layout.Divider(),
            "### Fazer uma Nova Denúncia",
            den_vaga_sel,
            den_desc_in,
            btn_fazer_den,
            msg_den
        )),
        ("Grupos Vulneráveis", pn.Column(
            grupos_cand_df,
            pn.layout.Divider(),
            "### Inscrever-se em um Grupo",
            grupos_vul_sel,
            comp_grupo_in,
            btn_add_grupo,
            pn.layout.Divider(),
            "### Sair de um Grupo",
            grupo_id_rem_in,
            btn_rem_grupo,
            msg_grupos
        )),
    )

    hab_campos_cand(True)

    return pn.Column(
        "# Gerenciamento de Candidato",
        cpf_in,
        pn.Column(
            nome_in, email_in, tel_in,
            pret_in, end_in, nasc_in, curr_in,
            sizing_mode="stretch_width"
        ),
        btns_crud_cand, msg,
        pn.layout.Divider(),
        "## Informações Relacionadas e Ações",
        abas_ext
    )
