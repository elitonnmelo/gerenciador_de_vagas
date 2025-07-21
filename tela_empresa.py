import panel as pn
import pandas as pd
from database import SessionLocal
from sqlalchemy.exc import IntegrityError
# Importar os modelos necessários para a tela da empresa
from models import Empresa, Vaga, Publica, ResponsavelInclusao, Candidatura, Candidato, Denuncia, GrupoVulneravel, VagaGrupo

pn.extension()

def tela_empresa():
    cnpj_in = pn.widgets.TextInput(name="CNPJ da Empresa")
    nome_in = pn.widgets.TextInput(name="Nome")
    razao_s_in = pn.widgets.TextInput(name="Razão Social")
    site_in = pn.widgets.TextInput(name="Site")
    end_in = pn.widgets.TextInput(name="Endereço")
    tel_in = pn.widgets.TextInput(name="Telefone")
    email_in = pn.widgets.TextInput(name="Email")

    msg = pn.pane.Markdown()

    vagas_df = pn.pane.DataFrame(name="Vagas Publicadas", width=800, height=200)
    resps_df = pn.pane.DataFrame(name="Responsáveis por Inclusão", width=800, height=200)
    feedbacks_df = pn.pane.DataFrame(name="Feedbacks de Candidaturas", width=800, height=200)
    den_emp_df = pn.pane.DataFrame(name="Denúncias Recebidas", width=800, height=200)
    cands_vaga_df = pn.pane.DataFrame(name="Candidatos para a Vaga", width=800, height=200)
    vaga_grupo_df = pn.pane.DataFrame(name="Grupos Associados à Vaga", width=800, height=150)

    _curr_cnpj = None
    _curr_vaga_id = None

    vaga_id_in = pn.widgets.TextInput(name="ID da Vaga (para Buscar/Atualizar/Deletar)", placeholder="Gerado automaticamente ao criar")
    vaga_titulo_in = pn.widgets.TextInput(name="Título da Vaga")
    vaga_desc_in = pn.widgets.TextAreaInput(name="Descrição da Vaga", height=100)
    vaga_sal_in = pn.widgets.FloatInput(name="Salário")
    vaga_ben_in = pn.widgets.TextInput(name="Benefícios")
    vaga_status_sel = pn.widgets.Select(name="Status da Vaga", options=["aberta", "fechada", "pausada"])

    btn_criar_vaga = pn.widgets.Button(name="Criar Vaga", button_type="success", disabled=True)
    btn_buscar_vaga = pn.widgets.Button(name="Buscar Vaga", button_type="primary", disabled=True)
    btn_upd_vaga = pn.widgets.Button(name="Atualizar Vaga", button_type="warning", disabled=True)
    btn_del_vaga = pn.widgets.Button(name="Deletar Vaga", button_type="danger", disabled=True)
    msg_vaga = pn.pane.Markdown()

    resp_email_in = pn.widgets.TextInput(name="Email do Responsável")
    resp_nome_in = pn.widgets.TextInput(name="Nome do Responsável")
    resp_dep_in = pn.widgets.TextInput(name="Departamento")
    resp_cargo_in = pn.widgets.TextInput(name="Cargo")

    btn_criar_resp = pn.widgets.Button(name="Adicionar Responsável", button_type="success", disabled=True)
    btn_buscar_resp = pn.widgets.Button(name="Buscar Responsável", button_type="primary", disabled=True)
    btn_upd_resp = pn.widgets.Button(name="Atualizar Responsável", button_type="warning", disabled=True)
    btn_del_resp = pn.widgets.Button(name="Remover Responsável", button_type="danger", disabled=True)
    msg_resp = pn.pane.Markdown()

    den_id_in = pn.widgets.TextInput(name="ID da Denúncia", placeholder="Ex: 1")
    den_status_upd_sel = pn.widgets.Select(name="Novo Status da Denúncia", options=["Aberta", "Em Análise", "Resolvida", "Rejeitada"])
    den_acoes_in = pn.widgets.TextAreaInput(name="Ações Tomadas", placeholder="Descreva as ações...", height=80)
    btn_upd_den_status = pn.widgets.Button(name="Atualizar Status Denúncia", button_type="warning", disabled=True)
    msg_den_emp = pn.pane.Markdown()

    vaga_cands_sel = pn.widgets.Select(name="Selecione a Vaga", options={})
    cand_cpf_cand_in = pn.widgets.TextInput(name="CPF do Candidato na Vaga", placeholder="CPF do candidato")
    cand_status_upd_sel = pn.widgets.Select(name="Novo Status da Candidatura", options=["Pendente", "Em Análise", "Selecionado", "Rejeitado"])
    cand_feedback_in = pn.widgets.TextAreaInput(name="Feedback para o Candidato", placeholder="Ex: Experiência insuficiente", height=80)
    btn_upd_cand_status = pn.widgets.Button(name="Atualizar Status Candidatura", button_type="warning", disabled=True)
    msg_cand_status = pn.pane.Markdown()

    grupos_vaga_sel = pn.widgets.Select(name="Grupo Vulnerável", options={})
    perc_vaga_in = pn.widgets.FloatInput(name="Percentual da Vaga (%)", start=0.0, end=100.0, step=0.1, value=0.0)
    btn_add_vaga_grupo = pn.widgets.Button(name="Adicionar Grupo à Vaga", button_type="success", disabled=True)
    btn_rem_vaga_grupo = pn.widgets.Button(name="Remover Grupo da Vaga", button_type="danger", disabled=True)
    msg_vaga_grupo = pn.pane.Markdown()


    def hab_campos_emp(habilitar=True):
        nome_in.disabled = not habilitar
        razao_s_in.disabled = not habilitar
        site_in.disabled = not habilitar
        end_in.disabled = not habilitar
        tel_in.disabled = not habilitar
        email_in.disabled = not habilitar

    def hab_btns_vaga(habilitar=True):
        btn_criar_vaga.disabled = not habilitar
        btn_buscar_vaga.disabled = not habilitar
        btn_upd_vaga.disabled = not habilitar
        btn_del_vaga.disabled = not habilitar
        grupos_vaga_sel.disabled = not habilitar
        perc_vaga_in.disabled = not habilitar
        btn_add_vaga_grupo.disabled = not habilitar
        btn_rem_vaga_grupo.disabled = not habilitar

    def hab_btns_resp(habilitar=True):
        btn_criar_resp.disabled = not habilitar
        btn_buscar_resp.disabled = not habilitar
        btn_upd_resp.disabled = not habilitar
        btn_del_resp.disabled = not habilitar

    def hab_btns_den_emp(habilitar=True):
        btn_upd_den_status.disabled = not habilitar

    def hab_btns_cand_status(habilitar=True):
        btn_upd_cand_status.disabled = not habilitar
        vaga_cands_sel.disabled = not habilitar
        cand_cpf_cand_in.disabled = not habilitar
        cand_status_upd_sel.disabled = not habilitar
        cand_feedback_in.disabled = not habilitar


    def limpar_campos_vaga():
        vaga_id_in.value = ""
        vaga_titulo_in.value = ""
        vaga_desc_in.value = ""
        vaga_sal_in.value = 0.0
        vaga_ben_in.value = ""
        vaga_status_sel.value = "aberta"
        msg_vaga.object = ""
        vaga_grupo_df.object = pd.DataFrame()
        perc_vaga_in.value = 0.0
        msg_vaga_grupo.object = ""

    def limpar_campos_resp():
        resp_email_in.value = ""
        resp_nome_in.value = ""
        resp_dep_in.value = ""
        resp_cargo_in.value = ""
        msg_resp.object = ""

    def limpar_campos_den_emp():
        den_id_in.value = ""
        den_status_upd_sel.value = "Aberta"
        den_acoes_in.value = ""
        msg_den_emp.object = ""

    def limpar_campos_cand_status():
        vaga_cands_sel.value = None
        cands_vaga_df.object = pd.DataFrame()
        cand_cpf_cand_in.value = ""
        cand_status_upd_sel.value = "Pendente"
        cand_feedback_in.value = ""
        msg_cand_status.object = ""

    def carregar_grupos_vulneraveis_para_vaga():
        db = SessionLocal()
        try:
            grupos = db.query(GrupoVulneravel).all()
            grupos_options = {f"{g.nome} (ID: {g.id_grupo})": g.id_grupo for g in grupos}
            grupos_vaga_sel.options = grupos_options
            if grupos_options:
                grupos_vaga_sel.value = list(grupos_options.values())[0]
            else:
                grupos_vaga_sel.value = None
        except Exception as e:
            print(f"Erro ao carregar grupos vulneráveis para vaga: {e}")
            grupos_vaga_sel.options = {"Nenhum grupo disponível": None}
            grupos_vaga_sel.value = None
        finally:
            db.close()

    def _carregar_vaga_grupo_data(db, vaga_id):
        vaga_grupo_data = []
        assocs = db.query(VagaGrupo).filter(VagaGrupo.id_vaga == vaga_id).all()
        for assoc in assocs:
            grupo = db.query(GrupoVulneravel).filter(GrupoVulneravel.id_grupo == assoc.id_grupo).first()
            nome_grupo = grupo.nome if grupo else "Grupo Desconhecido"
            vaga_grupo_data.append({
                'ID Grupo': assoc.id_grupo,
                'Nome do Grupo': nome_grupo,
                'Percentual Vaga': assoc.percentual_vaga
            })
        return vaga_grupo_data


    def criar_vaga_func(event=None):
        nonlocal _curr_cnpj
        if not _curr_cnpj:
            msg_vaga.object = "Por favor, busque uma empresa primeiro."
            return

        db = SessionLocal()
        try:
            nova_vaga = Vaga(
                titulo=vaga_titulo_in.value,
                descricao=vaga_desc_in.value,
                salario=vaga_sal_in.value,
                beneficios=vaga_ben_in.value,
                status_vaga=vaga_status_sel.value
            )
            db.add(nova_vaga)
            db.flush()
            
            nova_pub = Publica(
                id_vaga=nova_vaga.id_vaga,
                cnpj_empresa=_curr_cnpj
            )
            db.add(nova_pub)
            db.commit()
            msg_vaga.object = f"Vaga '{nova_vaga.titulo}' (ID: {nova_vaga.id_vaga}) criada e publicada com sucesso!"
            limpar_campos_vaga()
            buscar_emp_func(update_only_extras=True) # Corrigido aqui
        except Exception as e:
            db.rollback()
            msg_vaga.object = f"Erro ao criar vaga: {e}"
        finally:
            db.close()

    def buscar_vaga_func(event=None):
        nonlocal _curr_cnpj, _curr_vaga_id
        if not _curr_cnpj:
            msg_vaga.object = "Por favor, busque uma empresa primeiro."
            return
        if not vaga_id_in.value:
            msg_vaga.object = "Por favor, digite o ID da Vaga para buscar."
            return
        
        db = SessionLocal()
        try:
            vaga_id = int(vaga_id_in.value)
            vaga = db.query(Vaga).join(Publica).filter(
                Vaga.id_vaga == vaga_id,
                Publica.cnpj_empresa == _curr_cnpj
            ).first()

            if vaga:
                _curr_vaga_id = vaga.id_vaga
                vaga_titulo_in.value = vaga.titulo
                vaga_desc_in.value = vaga.descricao
                vaga_sal_in.value = float(vaga.salario)
                vaga_ben_in.value = vaga.beneficios
                vaga_status_sel.value = vaga.status_vaga
                msg_vaga.object = "Vaga encontrada."
                
                vaga_grupo_df.object = pd.DataFrame(_carregar_vaga_grupo_data(db, _curr_vaga_id))
                carregar_grupos_vulneraveis_para_vaga() # Chamado aqui para popular o select

            else:
                _curr_vaga_id = None
                msg_vaga.object = "Vaga não encontrada para esta empresa."
                limpar_campos_vaga()
        except ValueError:
            msg_vaga.object = "ID da Vaga inválido. Digite um número."
        except Exception as e:
            msg_vaga.object = f"Erro ao buscar vaga: {e}"
        finally:
            db.close()

    def upd_vaga_func(event=None):
        nonlocal _curr_cnpj
        if not _curr_cnpj:
            msg_vaga.object = "Por favor, busque uma empresa primeiro."
            return
        if not vaga_id_in.value:
            msg_vaga.object = "Por favor, digite o ID da Vaga para atualizar."
            return

        db = SessionLocal()
        try:
            vaga_id = int(vaga_id_in.value)
            vaga = db.query(Vaga).join(Publica).filter(
                Vaga.id_vaga == vaga_id,
                Publica.cnpj_empresa == _curr_cnpj
            ).first()

            if vaga:
                vaga.titulo = vaga_titulo_in.value
                vaga.descricao = vaga_desc_in.value
                vaga.salario = vaga_sal_in.value
                vaga.beneficios = vaga_ben_in.value
                vaga.status_vaga = vaga_status_sel.value
                db.commit()
                msg_vaga.object = "Vaga atualizada com sucesso!"
                buscar_emp_func(update_only_extras=True) # Corrigido aqui
            else:
                msg_vaga.object = "Vaga não encontrada para esta empresa."
        except ValueError:
            msg_vaga.object = "ID da Vaga inválido. Digite um número."
        except Exception as e:
            db.rollback()
            msg_vaga.object = f"Erro ao atualizar vaga: {e}"
        finally:
            db.close()

    def del_vaga_func(event=None):
        nonlocal _curr_cnpj, _curr_vaga_id
        if not _curr_cnpj:
            msg_vaga.object = "Por favor, busque uma empresa primeiro."
            return
        if not vaga_id_in.value:
            msg_vaga.object = "Por favor, digite o ID da Vaga para deletar."
            return

        db = SessionLocal()
        try:
            vaga_id = int(vaga_id_in.value)
            db.query(VagaGrupo).filter(VagaGrupo.id_vaga == vaga_id).delete(synchronize_session=False)
            pub = db.query(Publica).filter(
                Publica.id_vaga == vaga_id,
                Publica.cnpj_empresa == _curr_cnpj
            ).first()

            if pub:
                db.delete(pub)
                db.commit()

                vaga = db.query(Vaga).filter(Vaga.id_vaga == vaga_id).first()
                if vaga:
                    db.delete(vaga)
                    db.commit()
                    msg_vaga.object = "Vaga deletada com sucesso!"
                    limpar_campos_vaga()
                    _curr_vaga_id = None
                    buscar_emp_func(update_only_extras=True) # Corrigido aqui
                else:
                    msg_vaga.object = "Vaga não encontrada para exclusão após remover publicação."
            else:
                msg_vaga.object = "Publicação da vaga não encontrada para esta empresa."

        except IntegrityError:
            db.rollback()
            msg_vaga.object = "Não é possível deletar a vaga: ela está relacionada a candidaturas ou outras tabelas."
        except ValueError:
            msg_vaga.object = "ID da Vaga inválido. Digite um número."
        except Exception as e:
            db.rollback()
            msg_vaga.object = f"Erro ao deletar vaga: {e}"
        finally:
            db.close()


    def criar_resp_func(event=None):
        nonlocal _curr_cnpj
        if not _curr_cnpj:
            msg_resp.object = "Por favor, busque uma empresa primeiro."
            return
        if not resp_email_in.value:
            msg_resp.object = "O email do responsável é obrigatório."
            return

        db = SessionLocal()
        try:
            novo_resp = ResponsavelInclusao(
                email=resp_email_in.value,
                cnpj_empresa=_curr_cnpj,
                nome=resp_nome_in.value,
                departamento=resp_dep_in.value,
                cargo=resp_cargo_in.value
            )
            db.add(novo_resp)
            db.commit()
            msg_resp.object = "Responsável por Inclusão adicionado com sucesso!"
            limpar_campos_resp()
            buscar_emp_func(update_only_extras=True) # Corrigido aqui
        except IntegrityError:
            db.rollback()
            msg_resp.object = "Erro: Email já existe para esta empresa ou violação de integridade."
        except Exception as e:
            db.rollback()
            msg_resp.object = f"Erro ao adicionar responsável: {e}"
        finally:
            db.close()

    def buscar_resp_func(event=None):
        nonlocal _curr_cnpj
        if not _curr_cnpj:
            msg_resp.object = "Por favor, busque uma empresa primeiro."
            return
        if not resp_email_in.value:
            msg_resp.object = "Por favor, digite o Email do Responsável para buscar."
            return

        db = SessionLocal()
        try:
            resp = db.query(ResponsavelInclusao).filter(
                ResponsavelInclusao.email == resp_email_in.value,
                ResponsavelInclusao.cnpj_empresa == _curr_cnpj
            ).first()

            if resp:
                resp_nome_in.value = resp.nome
                resp_dep_in.value = resp.departamento
                resp_cargo_in.value = resp.cargo
                msg_resp.object = "Responsável encontrado."
            else:
                msg_resp.object = "Responsável não encontrado para esta empresa."
                limpar_campos_resp()
        except Exception as e:
            msg_resp.object = f"Erro ao buscar responsável: {e}"
        finally:
            db.close()

    def upd_resp_func(event=None):
        nonlocal _curr_cnpj
        if not _curr_cnpj:
            msg_resp.object = "Por favor, busque uma empresa primeiro."
            return
        if not resp_email_in.value:
            msg_resp.object = "Por favor, digite o Email do Responsável para atualizar."
            return

        db = SessionLocal()
        try:
            resp = db.query(ResponsavelInclusao).filter(
                ResponsavelInclusao.email == resp_email_in.value,
                ResponsavelInclusao.cnpj_empresa == _curr_cnpj
            ).first()

            if resp:
                resp.nome = resp_nome_in.value
                resp.departamento = resp_dep_in.value
                resp.cargo = resp_cargo_in.value
                db.commit()
                msg_resp.object = "Responsável atualizado com sucesso!"
                buscar_emp_func(update_only_extras=True) # Corrigido aqui
            else:
                msg_resp.object = "Responsável não encontrado para esta empresa."
        except Exception as e:
            db.rollback()
            msg_resp.object = f"Erro ao atualizar responsável: {e}"
        finally:
            db.close()

    def del_resp_func(event=None):
        nonlocal _curr_cnpj
        if not _curr_cnpj:
            msg_resp.object = "Por favor, busque uma empresa primeiro."
            return
        if not resp_email_in.value:
            msg_resp.object = "Por favor, digite o Email do Responsável para remover."
            return

        db = SessionLocal()
        try:
            resp = db.query(ResponsavelInclusao).filter(
                ResponsavelInclusao.email == resp_email_in.value,
                ResponsavelInclusao.cnpj_empresa == _curr_cnpj
            ).first()

            if resp:
                db.delete(resp)
                db.commit()
                msg_resp.object = "Responsável removido com sucesso!"
                limpar_campos_resp()
                buscar_emp_func(update_only_extras=True) # Corrigido aqui
            else:
                msg_resp.object = "Responsável não encontrado para esta empresa."
        except Exception as e:
            db.rollback()
            msg_resp.object = f"Erro ao remover responsável: {e}"
        finally:
            db.close()


    def upd_status_den_func(event=None):
        nonlocal _curr_cnpj
        if not _curr_cnpj:
            msg_den_emp.object = "Por favor, busque uma empresa primeiro."
            return
        if not den_id_in.value:
            msg_den_emp.object = "Por favor, digite o ID da Denúncia."
            return

        db = SessionLocal()
        try:
            den_id = int(den_id_in.value)
            den = db.query(Denuncia).join(Vaga).join(Publica).filter(
                Denuncia.id_denuncia == den_id,
                Publica.cnpj_empresa == _curr_cnpj
            ).first()

            if den:
                den.status_denuncia = den_status_upd_sel.value
                den.acoes_tomadas = den_acoes_in.value
                db.commit()
                msg_den_emp.object = "Status da denúncia atualizado com sucesso!"
                buscar_emp_func(update_only_extras=True) # Corrigido aqui
            else:
                msg_den_emp.object = "Denúncia não encontrada ou não relacionada a esta empresa."
        except ValueError:
            msg_den_emp.object = "ID da Denúncia inválido. Digite um número."
        except Exception as e:
            db.rollback()
            msg_den_emp.object = f"Erro ao atualizar denúncia: {e}"
        finally:
            db.close()

    def carregar_cands_por_vaga_func(event=None):
        nonlocal _curr_cnpj
        if not _curr_cnpj:
            cands_vaga_df.object = pd.DataFrame()
            return

        id_vaga_sel = vaga_cands_sel.value
        if not id_vaga_sel:
            cands_vaga_df.object = pd.DataFrame()
            return

        db = SessionLocal()
        try:
            vaga_pertence_emp = db.query(Publica).filter(
                Publica.id_vaga == id_vaga_sel,
                Publica.cnpj_empresa == _curr_cnpj
            ).first()

            if not vaga_pertence_emp:
                cands_vaga_df.object = pd.DataFrame()
                msg_cand_status.object = "A vaga selecionada não pertence a esta empresa."
                return

            cands = db.query(Candidatura).filter(
                Candidatura.id_vaga == id_vaga_sel
            ).all()

            cands_data = []
            for cand in cands:
                cand_obj = db.query(Candidato).filter(Candidato.cpf == cand.cpf_candidato).first()
                nome_cand = cand_obj.nome if cand_obj else "Candidato Desconhecido"
                cands_data.append({
                    'CPF Candidato': cand.cpf_candidato,
                    'Nome Candidato': nome_cand,
                    'Data Candidatura': cand.data_candidatura,
                    'Status': cand.status,
                    'Feedback Empresa': cand.feedback_empresa
                })
            cands_vaga_df.object = pd.DataFrame(cands_data)
            msg_cand_status.object = ""
        except Exception as e:
            cands_vaga_df.object = pd.DataFrame()
            msg_cand_status.object = f"Erro ao carregar candidatos: {e}"
        finally:
            db.close()


    def upd_status_cand_func(event=None):
        nonlocal _curr_cnpj
        if not _curr_cnpj:
            msg_cand_status.object = "Por favor, busque uma empresa primeiro."
            return
        
        id_vaga_sel = vaga_cands_sel.value
        cand_cpf = cand_cpf_cand_in.value

        if not id_vaga_sel or not cand_cpf:
            msg_cand_status.object = "Selecione uma vaga e digite o CPF do candidato."
            return

        db = SessionLocal()
        try:
            vaga_pertence_emp = db.query(Publica).filter(
                Publica.id_vaga == id_vaga_sel,
                Publica.cnpj_empresa == _curr_cnpj
            ).first()

            if not vaga_pertence_emp:
                msg_cand_status.object = "A vaga selecionada não pertence a esta empresa."
                return

            cand = db.query(Candidatura).filter(
                Candidatura.id_vaga == id_vaga_sel,
                Candidatura.cpf_candidato == cand_cpf
            ).first()

            if cand:
                cand.status = cand_status_upd_sel.value
                cand.feedback_empresa = cand_feedback_in.value
                db.commit()
                msg_cand_status.object = "Status da candidatura atualizado com sucesso!"
                carregar_cands_por_vaga_func()
                buscar_emp_func(update_only_extras=True) # Corrigido aqui
            else:
                msg_cand_status.object = "Candidatura não encontrada para esta vaga e CPF."
        except Exception as e:
            db.rollback()
            msg_cand_status.object = f"Erro ao atualizar candidatura: {e}"
        finally:
            db.close()

    def add_vaga_grupo_func(event=None):
        nonlocal _curr_vaga_id
        if not _curr_vaga_id:
            msg_vaga_grupo.object = "Por favor, selecione uma vaga primeiro."
            return
        if not grupos_vaga_sel.value:
            msg_vaga_grupo.object = "Por favor, selecione um grupo."
            return
        
        db = SessionLocal()
        try:
            id_grupo_sel = grupos_vaga_sel.value
            perc_vaga = perc_vaga_in.value

            assoc_existente = db.query(VagaGrupo).filter(
                VagaGrupo.id_vaga == _curr_vaga_id,
                VagaGrupo.id_grupo == id_grupo_sel
            ).first()

            if assoc_existente:
                msg_vaga_grupo.object = "Esta vaga já está associada a este grupo."
            else:
                nova_assoc = VagaGrupo(
                    id_vaga=_curr_vaga_id,
                    id_grupo=id_grupo_sel,
                    percentual_vaga=perc_vaga
                )
                db.add(nova_assoc)
                db.commit()
                msg_vaga_grupo.object = "Associação Vaga-Grupo adicionada com sucesso!"
                perc_vaga_in.value = 0.0
                buscar_vaga_func() # Atualiza a tabela de grupos da vaga
        except Exception as e:
            db.rollback()
            msg_vaga_grupo.object = f"Erro ao adicionar associação Vaga-Grupo: {e}"
        finally:
            db.close()

    def rem_vaga_grupo_func(event=None):
        nonlocal _curr_vaga_id
        if not _curr_vaga_id:
            msg_vaga_grupo.object = "Por favor, selecione uma vaga primeiro."
            return
        if not grupos_vaga_sel.value:
            msg_vaga_grupo.object = "Por favor, selecione um grupo para remover."
            return
        
        db = SessionLocal()
        try:
            id_grupo_sel = grupos_vaga_sel.value
            assoc = db.query(VagaGrupo).filter(
                VagaGrupo.id_vaga == _curr_vaga_id,
                VagaGrupo.id_grupo == id_grupo_sel
            ).first()

            if assoc:
                db.delete(assoc)
                db.commit()
                msg_vaga_grupo.object = "Associação Vaga-Grupo removida com sucesso!"
                buscar_vaga_func() # Atualiza a tabela de grupos da vaga
            else:
                msg_vaga_grupo.object = "Associação Vaga-Grupo não encontrada."
        except Exception as e:
            db.rollback()
            msg_vaga_grupo.object = f"Erro ao remover associação Vaga-Grupo: {e}"
        finally:
            db.close()


    def criar_emp_func(event=None):
        db = SessionLocal()
        try:
            nova_emp = Empresa(
                cnpj=cnpj_in.value,
                nome=nome_in.value,
                razao_social=razao_s_in.value,
                site=site_in.value,
                endereco=end_in.value,
                telefone=tel_in.value,
                email=email_in.value
            )
            db.add(nova_emp)
            db.commit()
            msg.object = "Empresa criada com sucesso."
            limpar_campos_emp()
        except IntegrityError:
            db.rollback()
            msg.object = "CNPJ já existe ou erro de integridade."
        except Exception as e:
            db.rollback()
            msg.object = f"Erro: {str(e)}"
        finally:
            db.close()

    def buscar_emp_func(event=None, update_only_extras=False):
        nonlocal _curr_cnpj
        db = SessionLocal()
        try:
            e = db.query(Empresa).filter(Empresa.cnpj == cnpj_in.value).first()
            if e:
                _curr_cnpj = e.cnpj

                if not update_only_extras:
                    nome_in.value = e.nome
                    razao_s_in.value = e.razao_social
                    site_in.value = e.site
                    end_in.value = e.endereco
                    tel_in.value = e.telefone
                    email_in.value = e.email
                    msg.object = "Empresa encontrada."
                    hab_campos_emp(False)

                vagas_data = []
                vagas_options_para_sel = {"Selecione uma vaga": None}
                for pub in e.vagas_publicadas:
                    vaga = db.query(Vaga).filter(Vaga.id_vaga == pub.id_vaga).first()
                    if vaga:
                        vagas_data.append({
                            'ID Vaga': vaga.id_vaga,
                            'Título': vaga.titulo,
                            'Descrição': vaga.descricao,
                            'Salário': vaga.salario,
                            'Benefícios': vaga.beneficios,
                            'Status': vaga.status_vaga
                        })
                        vagas_options_para_sel[f"{vaga.titulo} (ID: {vaga.id_vaga})"] = vaga.id_vaga

                vagas_df.object = pd.DataFrame(vagas_data)
                hab_btns_vaga(True)
                vaga_cands_sel.options = vagas_options_para_sel
                if vagas_data:
                    vaga_cands_sel.value = list(vagas_options_para_sel.values())[1]
                else:
                    vaga_cands_sel.value = None

                resps_data = []
                for resp in e.responsaveis_inclusao:
                    resps_data.append({
                        'Email': resp.email,
                        'Nome': resp.nome,
                        'Departamento': resp.departamento,
                        'Cargo': resp.cargo
                    })
                resps_df.object = pd.DataFrame(resps_data)
                hab_btns_resp(True)

                feedbacks_data = []
                for pub in e.vagas_publicadas:
                    vaga = db.query(Vaga).filter(Vaga.id_vaga == pub.id_vaga).first()
                    if vaga:
                        for cand in vaga.candidaturas:
                            if cand.feedback_empresa:
                                cand_obj = db.query(Candidato).filter(Candidato.cpf == cand.cpf_candidato).first()
                                nome_cand = cand_obj.nome if cand_obj else "Candidato Desconhecido"
                                feedbacks_data.append({
                                    'Vaga': vaga.titulo,
                                    'Candidato (CPF)': cand.cpf_candidato,
                                    'Nome Candidato': nome_cand,
                                    'Data Candidatura': cand.data_candidatura,
                                    'Status Candidatura': cand.status,
                                    'Feedback': cand.feedback_empresa
                                })
                feedbacks_df.object = pd.DataFrame(feedbacks_data)

                den_rel = db.query(Denuncia).join(Vaga).join(Publica).filter(
                    Publica.cnpj_empresa == _curr_cnpj
                ).all()

                den_data = []
                for den in den_rel:
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
                den_emp_df.object = pd.DataFrame(den_data)
                hab_btns_den_emp(True)

                hab_btns_cand_status(True)
                if vaga_cands_sel.value:
                    carregar_cands_por_vaga_func()
                
                # Carrega grupos vulneráveis para o select de Vaga_Grupo
                carregar_grupos_vulneraveis_para_vaga()

            else:
                _curr_cnpj = None
                msg.object = "Empresa não encontrada."
                limpar_campos_emp(apenas_dados_extras=True)
                hab_campos_emp(True)
                hab_btns_vaga(False)
                hab_btns_resp(False)
                hab_btns_den_emp(False)
                hab_btns_cand_status(False)

        except Exception as e:
            msg.object = f"Erro ao buscar empresa: {e}"
            limpar_campos_emp(apenas_dados_extras=True)
            hab_campos_emp(True)
            hab_btns_vaga(False)
            hab_btns_resp(False)
            hab_btns_den_emp(False)
            hab_btns_cand_status(False)
        finally:
            db.close()

    def upd_emp_func(event=None):
        db = SessionLocal()
        try:
            e = db.query(Empresa).filter(Empresa.cnpj == cnpj_in.value).first()
            if e:
                e.nome = nome_in.value
                e.razao_social = razao_s_in.value
                e.site = site_in.value
                e.endereco = end_in.value
                e.telefone = tel_in.value
                e.email = email_in.value
                db.commit()
                msg.object = "Empresa atualizada."
            else:
                msg.object = "Empresa não encontrada."
        except Exception as e:
            db.rollback()
            msg.object = f"Erro ao atualizar empresa: {e}"
        finally:
            db.close()

    def del_emp_func(event=None):
        nonlocal _curr_cnpj
        db = SessionLocal()
        try:
            e = db.query(Empresa).filter(Empresa.cnpj == cnpj_in.value).first()
            if e:
                db.delete(e)
                db.commit()
                msg.object = "Empresa deletada."
                limpar_campos_emp()
                _curr_cnpj = None
                hab_btns_vaga(False)
                hab_btns_resp(False)
                hab_btns_den_emp(False)
                hab_btns_cand_status(False)
            else:
                msg.object = "Empresa não encontrada."
        except IntegrityError:
            db.rollback()
            msg.object = "Não é possível deletar. A empresa está vinculada a outras tabelas (vagas, responsáveis, denúncias)."
        except Exception as e:
            db.rollback()
            msg.object = f"Erro ao deletar empresa: {e}"
        finally:
            db.close()

    def limpar_campos_emp(apenas_dados_extras=False):
        nonlocal _curr_cnpj
        if not apenas_dados_extras:
            cnpj_in.value = ""
            nome_in.value = ""
            razao_s_in.value = ""
            site_in.value = ""
            end_in.value = ""
            tel_in.value = ""
            email_in.value = ""
            msg.object = ""
            _curr_cnpj = None
            hab_campos_emp(True)

        vagas_df.object = pd.DataFrame()
        resps_df.object = pd.DataFrame()
        feedbacks_df.object = pd.DataFrame()
        den_emp_df.object = pd.DataFrame()
        cands_vaga_df.object = pd.DataFrame()
        vaga_grupo_df.object = pd.DataFrame()


        limpar_campos_vaga()
        hab_btns_vaga(False)

        limpar_campos_resp()
        hab_btns_resp(False)

        limpar_campos_den_emp()
        hab_btns_den_emp(False)

        limpar_campos_cand_status()
        hab_btns_cand_status(False)

        # Limpa e reseta o select de grupos vulneráveis para vaga
        grupos_vaga_sel.options = {}
        grupos_vaga_sel.value = None


    btn_criar_emp = pn.widgets.Button(name="Criar", button_type="success")
    btn_criar_emp.on_click(criar_emp_func)

    btn_buscar_emp = pn.widgets.Button(name="Buscar", button_type="primary")
    btn_buscar_emp.on_click(buscar_emp_func)

    btn_upd_emp = pn.widgets.Button(name="Atualizar", button_type="warning")
    btn_upd_emp.on_click(upd_emp_func)

    btn_del_emp = pn.widgets.Button(name="Deletar", button_type="danger")
    btn_del_emp.on_click(del_emp_func)

    btn_limpar_emp_campos = pn.widgets.Button(name="Limpar Campos", button_type="default")
    btn_limpar_emp_campos.on_click(lambda event: limpar_campos_emp())

    btn_criar_vaga.on_click(criar_vaga_func)
    btn_buscar_vaga.on_click(buscar_vaga_func)
    btn_upd_vaga.on_click(upd_vaga_func)
    btn_del_vaga.on_click(del_vaga_func)

    btn_criar_resp.on_click(criar_resp_func)
    btn_buscar_resp.on_click(buscar_resp_func)
    btn_upd_resp.on_click(upd_resp_func)
    btn_del_resp.on_click(del_resp_func)

    btn_upd_den_status.on_click(upd_status_den_func)

    vaga_cands_sel.param.watch(carregar_cands_por_vaga_func, 'value')
    btn_upd_cand_status.on_click(upd_status_cand_func)

    btn_add_vaga_grupo.on_click(add_vaga_grupo_func)
    btn_rem_vaga_grupo.on_click(rem_vaga_grupo_func)


    btns_crud_emp = pn.Row(btn_criar_emp, btn_buscar_emp, btn_upd_emp, btn_del_emp, btn_limpar_emp_campos)

    abas_ext = pn.Tabs(
        ("Vagas Publicadas", pn.Column(
            vagas_df,
            pn.layout.Divider(),
            "### Gerenciar Vagas",
            vaga_id_in,
            vaga_titulo_in,
            vaga_desc_in,
            vaga_sal_in,
            vaga_ben_in,
            vaga_status_sel,
            pn.Row(btn_criar_vaga, btn_buscar_vaga, btn_upd_vaga, btn_del_vaga),
            msg_vaga,
            pn.layout.Divider(),
            "### Gerenciar Grupos por Vaga",
            grupos_vaga_sel,
            perc_vaga_in,
            pn.Row(btn_add_vaga_grupo, btn_rem_vaga_grupo),
            msg_vaga_grupo,
            vaga_grupo_df
        )),
        ("Responsáveis por Inclusão", pn.Column(
            resps_df,
            pn.layout.Divider(),
            "### Gerenciar Responsáveis",
            resp_email_in,
            resp_nome_in,
            resp_dep_in,
            resp_cargo_in,
            pn.Row(btn_criar_resp, btn_buscar_resp, btn_upd_resp, btn_del_resp),
            msg_resp
        )),
        ("Feedbacks", feedbacks_df),
        ("Gerenciar Denúncias", pn.Column(
            den_emp_df,
            pn.layout.Divider(),
            "### Atualizar Status de Denúncia",
            den_id_in,
            den_status_upd_sel,
            den_acoes_in,
            btn_upd_den_status,
            msg_den_emp
        )),
        ("Gerenciar Candidaturas por Vaga", pn.Column(
            "### Visualizar e Atualizar Candidaturas para uma Vaga",
            vaga_cands_sel,
            cands_vaga_df,
            pn.layout.Divider(),
            "### Atualizar Status de Candidato",
            cand_cpf_cand_in,
            cand_status_upd_sel,
            cand_feedback_in,
            btn_upd_cand_status,
            msg_cand_status
        )),
    )

    hab_campos_emp(True)
    hab_btns_vaga(False)
    hab_btns_resp(False)
    hab_btns_den_emp(False)
    hab_btns_cand_status(False)


    return pn.Column(
        "# Gerenciamento de Empresas",
        cnpj_in,
        pn.Column(
            nome_in, razao_s_in, site_in,
            end_in, tel_in, email_in,
            sizing_mode="stretch_width"
        ),
        btns_crud_emp, msg,
        pn.layout.Divider(),
        "## Informações Relacionadas e Ações",
        abas_ext
    )
