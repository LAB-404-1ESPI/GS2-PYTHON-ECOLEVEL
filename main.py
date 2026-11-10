"""
EcoLevel - protótipo acadêmico em Python
Execução: python main.py
"""

import json
import os
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).with_name("data.json")
ADMIN_PASSWORD = "TRIAGEM2026"  # senha demonstrativa; não usar em produção

MACHINES = [
    {"id": "M001", "name": "Ponto Centro", "address": "Praça Central (ponto demonstrativo)", "status": "Disponível"},
    {"id": "M002", "name": "Ponto Zona Sul", "address": "Mercado Parceiro (ponto demonstrativo)", "status": "Disponível"},
    {"id": "M003", "name": "Ponto Zona Oeste", "address": "Cooperativa Parceira (ponto demonstrativo)", "status": "Em manutenção"},
]

REWARDS = [
    {"id": "R01", "name": "Cupom de R$ 5 em parceiro", "cost": 50},
    {"id": "R02", "name": "Ecobag reutilizável", "cost": 100},
    {"id": "R03", "name": "Gift card demonstrativo", "cost": 200},
    {"id": "R04", "name": "Skin especial EcoLevel", "cost": 30},
]

# Marcos acumulados de XP e bônus por alcançar cada novo nível.
LEVELS = [
    (1, 0, "Semente", 0),
    (2, 100, "Broto", 10),
    (3, 250, "Guardião Verde", 10),
    (4, 500, "Protetor da Natureza", 10),
    (5, 850, "Lenda Sustentável", 15),
]


def default_data():
    return {
        "users": {},
        "sessions": [],
        "transactions": [],
        "redemptions": [],
        "next_user_number": 1,
    }


def load_data():
    """Lê o JSON; se ainda não existir, cria a estrutura inicial."""
    if not DATA_FILE.exists():
        data = default_data()
        save_data(data)
        return data
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, dict):
            raise ValueError("Formato principal inválido.")
        for key, value in default_data().items():
            data.setdefault(key, value)
        return data
    except (json.JSONDecodeError, OSError, ValueError) as error:
        print(f"Não foi possível ler data.json: {error}")
        print("Será utilizada uma estrutura vazia. Faça uma cópia do arquivo original antes de continuar.")
        return default_data()


def save_data(data):
    """Grava os dados no arquivo JSON."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except OSError as error:
        print(f"Erro ao salvar os dados: {error}")


def read_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("O campo não pode ficar vazio.")


def read_positive_float(prompt, allow_zero=False):
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            value = float(raw)
            if value < 0 or (value == 0 and not allow_zero):
                print("Informe um número válido maior que zero.")
                continue
            return round(value, 3)
        except ValueError:
            print("Valor inválido. Digite um número, por exemplo: 2.5")


def get_level(xp):
    """Retorna (nível, nome, XP do próximo nível)."""
    current = LEVELS[0]
    next_xp = None
    for index, level_info in enumerate(LEVELS):
        if xp >= level_info[1]:
            current = level_info
            if index + 1 < len(LEVELS):
                next_xp = LEVELS[index + 1][1]
            break
    # A busca acima percorre do maior marco alcançado para o menor.
    for level_info in LEVELS:
        if xp >= level_info[1]:
            current = level_info
    current_index = LEVELS.index(current)
    if current_index + 1 < len(LEVELS):
        next_xp = LEVELS[current_index + 1][1]
    else:
        next_xp = None
    return current[0], current[2], next_xp


def register_user(data):
    print("\n--- Cadastro EcoLevel ---")
    name = read_non_empty("Nome: ")
    email = read_non_empty("E-mail: ").lower()
    for user in data["users"].values():
        if user["email"] == email:
            print("Já existe uma conta com esse e-mail.")
            return None

    user_id = f"EC{data['next_user_number']:04d}"
    data["next_user_number"] += 1
    data["users"][user_id] = {
        "id": user_id,
        "name": name,
        "email": email,
        "coins": 0,
        "xp": 0,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    save_data(data)
    print(f"Cadastro concluído! Seu ID EcoLevel é {user_id}.")
    return user_id


def login_user(data):
    print("\n--- Entrar ---")
    user_id = read_non_empty("Informe seu ID EcoLevel (ex.: EC0001): ").upper()
    if user_id in data["users"]:
        print(f"Bem-vindo(a), {data['users'][user_id]['name']}!")
        return user_id
    print("ID não encontrado. Faça seu cadastro primeiro.")
    return None


def show_machines():
    print("\n--- Mapa demonstrativo de pontos ---")
    for machine in MACHINES:
        print(f"{machine['id']} | {machine['name']} | {machine['address']} | {machine['status']}")
    print("Os endereços são fictícios e servem apenas para demonstrar o protótipo.")


def start_disposal(data, user_id):
    show_machines()
    machine_id = read_non_empty("\nDigite o ID do ponto: ").upper()
    machine = next((item for item in MACHINES if item["id"] == machine_id), None)
    if machine is None:
        print("Ponto não encontrado.")
        return
    if machine["status"] != "Disponível":
        print("Este ponto está indisponível no momento.")
        return

    gross_weight = read_positive_float("Peso bruto do saco em kg: ")
    session_number = len(data["sessions"]) + 1
    session_id = f"SES{session_number:05d}"
    session = {
        "id": session_id,
        "user_id": user_id,
        "machine_id": machine_id,
        "gross_weight": gross_weight,
        "approved_weight": None,
        "rejected_weight": None,
        "status": "Aguardando triagem",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "reviewed_at": None,
        "reviewer": None,
        "coins_credited": 0,
        "xp_credited": 0,
    }
    data["sessions"].append(session)
    save_data(data)

    print("\n========== ETIQUETA DEMONSTRATIVA ==========")
    print(f"EcoLevel | Sessão: {session_id}")
    print(f"Usuário: {user_id}")
    print(f"Ponto: {machine_id}")
    print(f"Peso bruto: {gross_weight:.3f} kg")
    print(f"Data: {session['created_at']}")
    print("Cole esta identificação no saco (simulação).")
    print("============================================")
    print("Descarte registrado e enviado para a fila de triagem.")


def show_wallet(data, user_id):
    user = data["users"][user_id]
    level, level_name, next_xp = get_level(user["xp"])
    print("\n--- Minha carteira ---")
    print(f"Usuário: {user['name']} ({user_id})")
    print(f"Moedas: {user['coins']}")
    print(f"XP: {user['xp']}")
    print(f"Nível {level} - {level_name}")
    if next_xp is None:
        print("Você alcançou o nível máximo!")
    else:
        print(f"Faltam {max(0, next_xp - user['xp'])} XP para o próximo nível.")


def user_history(data, user_id):
    print("\n--- Histórico de descartes ---")
    found = False
    for session in data["sessions"]:
        if session["user_id"] == user_id:
            found = True
            approved = session["approved_weight"]
            approved_text = "Pendente" if approved is None else f"{approved:.3f} kg"
            print(
                f"{session['id']} | Bruto: {session['gross_weight']:.3f} kg | "
                f"Aprovado: {approved_text} | Status: {session['status']}"
            )
    if not found:
        print("Você ainda não possui descartes registrados.")


def show_rewards():
    print("\n--- Catálogo de recompensas ---")
    for reward in REWARDS:
        print(f"{reward['id']} | {reward['name']} | {reward['cost']} moedas")


def redeem_reward(data, user_id):
    show_rewards()
    reward_id = read_non_empty("\nCódigo da recompensa: ").upper()
    reward = next((item for item in REWARDS if item["id"] == reward_id), None)
    if reward is None:
        print("Recompensa não encontrada.")
        return
    user = data["users"][user_id]
    if user["coins"] < reward["cost"]:
        print("Saldo insuficiente.")
        return
    confirmation = input(f"Confirmar resgate de '{reward['name']}'? (s/n): ").strip().lower()
    if confirmation != "s":
        print("Resgate cancelado.")
        return
    user["coins"] -= reward["cost"]
    redemption = {
        "id": f"RES{len(data['redemptions']) + 1:05d}",
        "user_id": user_id,
        "reward_id": reward_id,
        "reward_name": reward["name"],
        "cost": reward["cost"],
        "date": datetime.now().isoformat(timespec="seconds"),
    }
    data["redemptions"].append(redemption)
    data["transactions"].append({
        "user_id": user_id,
        "type": "Resgate",
        "amount": -reward["cost"],
        "reference": redemption["id"],
        "date": redemption["date"],
    })
    save_data(data)
    print("Resgate registrado no protótipo. Em uma versão real, o parceiro precisaria validar o benefício.")


def user_menu(data, user_id):
    while True:
        print("\n========== MENU DO USUÁRIO ==========")
        print("1 - Encontrar pontos de descarte")
        print("2 - Registrar descarte / pesar saco")
        print("3 - Ver carteira, XP e nível")
        print("4 - Histórico de descartes")
        print("5 - Ver recompensas")
        print("6 - Resgatar recompensa")
        print("0 - Sair da conta")
        option = input("Escolha: ").strip()
        match option:
            case "1":
                show_machines()
            case "2":
                start_disposal(data, user_id)
            case "3":
                show_wallet(data, user_id)
            case "4":
                user_history(data, user_id)
            case "5":
                show_rewards()
            case "6":
                redeem_reward(data, user_id)
            case "0":
                break
            case _:
                print("Opção inválida. Escolha uma opção do menu.")


def pending_sessions(data):
    return [session for session in data["sessions"] if session["status"] == "Aguardando triagem"]


def triage_panel(data):
    print("\n--- Painel da equipe de triagem ---")
    pending = pending_sessions(data)
    if not pending:
        print("Não há sacos aguardando triagem.")
        return
    for session in pending:
        print(
            f"{session['id']} | Usuário: {session['user_id']} | "
            f"Peso bruto: {session['gross_weight']:.3f} kg | Ponto: {session['machine_id']}"
        )

    session_id = read_non_empty("\nInforme o código da sessão para analisar (ou 0 para voltar): ").upper()
    if session_id == "0":
        return
    session = next((item for item in pending if item["id"] == session_id), None)
    if session is None:
        print("Sessão não encontrada ou já analisada. Uma sessão só pode ser validada uma vez.")
        return

    approved = read_positive_float("Peso reciclável aprovado em kg (0 se nenhum): ", allow_zero=True)
    if approved > session["gross_weight"]:
        print("O peso aprovado não pode ser maior que o peso bruto.")
        return
    rejected = round(session["gross_weight"] - approved, 3)
    reviewer = read_non_empty("Nome ou código do responsável pela triagem: ")

    # Regra definida no projeto: 10 moedas por kg aprovado.
    # Para o protótipo, também são atribuídos 10 XP por kg aprovado.
    coins = round(approved * 10)
    xp = round(approved * 10)
    user = data["users"].get(session["user_id"])
    if user is None:
        print("Usuário associado à sessão não foi encontrado. Triagem não registrada.")
        return

    old_level = get_level(user["xp"])[0]
    user["coins"] += coins
    user["xp"] += xp
    new_level = get_level(user["xp"])[0]
    level_bonus = 0
    if new_level > old_level:
        for level_info in LEVELS:
            if old_level < level_info[0] <= new_level:
                level_bonus += level_info[3]
        user["coins"] += level_bonus

    session["approved_weight"] = approved
    session["rejected_weight"] = rejected
    session["status"] = "Aprovado" if rejected == 0 else ("Aprovado parcialmente" if approved > 0 else "Não aprovado")
    session["reviewed_at"] = datetime.now().isoformat(timespec="seconds")
    session["reviewer"] = reviewer
    session["coins_credited"] = coins
    session["xp_credited"] = xp

    data["transactions"].append({
        "user_id": user["id"],
        "type": "Crédito por reciclagem",
        "amount": coins,
        "reference": session["id"],
        "date": session["reviewed_at"],
    })
    if level_bonus:
        data["transactions"].append({
            "user_id": user["id"],
            "type": "Bônus de evolução",
            "amount": level_bonus,
            "reference": session["id"],
            "date": session["reviewed_at"],
        })
    save_data(data)

    print("\nTriagem concluída!")
    print(f"Peso bruto: {session['gross_weight']:.3f} kg")
    print(f"Peso aprovado: {approved:.3f} kg")
    print(f"Peso descontado: {rejected:.3f} kg")
    print(f"Crédito: {coins} moedas e {xp} XP.")
    if level_bonus:
        print(f"Bônus por evolução de nível: {level_bonus} moedas.")
    print(f"Status: {session['status']}")


def admin_menu(data):
    print("\n--- Acesso da equipe ---")
    password = input("Senha demonstrativa: ")
    if password != ADMIN_PASSWORD:
        print("Senha incorreta.")
        return
    while True:
        print("\n========== MENU DA TRIAGEM ==========")
        print("1 - Ver sessões aguardando triagem")
        print("2 - Analisar uma sessão")
        print("0 - Voltar")
        option = input("Escolha: ").strip()
        match option:
            case "1":
                queue = pending_sessions(data)
                if not queue:
                    print("Fila vazia.")
                for session in queue:
                    print(f"{session['id']} | {session['user_id']} | {session['gross_weight']:.3f} kg")
            case "2":
                triage_panel(data)
            case "0":
                break
            case _:
                print("Opção inválida.")


def print_header():
    print("\n" + "=" * 48)
    print("                 ECOLEVEL")
    print(" Recicle, evolua e transforme sua cidade.")
    print("=" * 48)


def main():
    data = load_data()
    while True:
        print_header()
        print("1 - Criar conta")
        print("2 - Entrar")
        print("3 - Painel da equipe de triagem")
        print("0 - Encerrar")
        option = input("Escolha uma opção: ").strip()
        match option:
            case "1":
                user_id = register_user(data)
                if user_id:
                    user_menu(data, user_id)
            case "2":
                user_id = login_user(data)
                if user_id:
                    user_menu(data, user_id)
            case "3":
                admin_menu(data)
            case "0":
                save_data(data)
                print("Obrigado por utilizar o EcoLevel!")
                break
            case _:
                print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma encerrado pelo usuário.")
    except Exception as error:
        print(f"\nOcorreu um erro inesperado: {error}")
        print("Verifique os dados e tente executar o programa novamente.")
