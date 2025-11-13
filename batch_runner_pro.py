# -*- coding: utf-8 -*-
import csv
import os
import random
import json
from collections import defaultdict
from scraping import Youtube
from utils import tools


# ===========================
# CONFIGURAÇÕES
# ===========================
TRAIN_PROPORTION = 0.7
TEST_PROPORTION = 0.2
VALIDATION_PROPORTION = 0.1

BASE_DIR = "dist"
CACHE_FILE = os.path.join(BASE_DIR, "completed_users.json")


# ===========================
# FUNÇÕES AUXILIARES
# ===========================
def load_completed_users():
    """Carrega usernames já processados com sucesso do cache."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                return set()
    return set()


def save_completed_user(username):
    """Adiciona um username processado com sucesso ao cache."""
    completed = load_completed_users()
    completed.add(username)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(list(completed)), f, ensure_ascii=False, indent=2)


def split_usernames(usernames):
    """Divide usernames nas proporções de treino, teste e validação."""
    random.shuffle(usernames)
    total = len(usernames)

    train_end = int(total * TRAIN_PROPORTION)
    test_end = train_end + int(total * TEST_PROPORTION)

    return (
        usernames[:train_end],
        usernames[train_end:test_end],
        usernames[test_end:],
    )


def ensure_dirs(base_dir):
    """Cria estrutura de diretórios esperada."""
    tools.make_dir(base_dir)
    for split in ["train", "test", "validation"]:
        tools.make_dir(f"{base_dir}/{split}")
        for category in ["real", "brainrot"]:
            tools.make_dir(f"{base_dir}/{split}/{category}")


def clean_text(value):
    """Remove quebras de linha, tabs e espaços extras do texto."""
    if not isinstance(value, str):
        return value
    return (
        value.replace("\n", " ")
             .replace("\r", " ")
             .replace("\t", " ")
             .strip()
    )


def init_csv(csv_path):
    """Inicializa CSV com cabeçalho."""
    if not os.path.exists(csv_path):
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "post_id", "username", "name", "post_desc", "post_title", "platform", "date"
            ])


def append_to_csv(csv_path, platform, profile, posts):
    """Adiciona dados de posts ao CSV."""
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        for post in posts:
            writer.writerow([
                post.get("id"), # "post_id"
                clean_text(profile.get("username")), # "username"
                clean_text(profile.get("name")), # "name"
                clean_text(post.get("description")), # "post_desc"
                clean_text(post.get("title")), # "post_title"
                platform, # "platform"
                post.get("date"), # "date"
            ])

# ===========================
# FUNÇÃO PRINCIPAL
# ===========================
def run_batch_by_category(strategy, usernames_real, usernames_brainrot, save_imgs=False):
    """Executa scraping dividido por categoria e salva datasets."""
    ensure_dirs(BASE_DIR)

    completed = load_completed_users()

    if strategy == "y":
        key = tools.read_settings("env.json").get("yt_api_key")
        if not key:
            raise Exception("yt_api_key is missing")
        scraper = Youtube(key)
        platform = "youtube"
    else:
        raise ValueError(f"Invalid strategy '{strategy}', must be 'y'")

    # Estatísticas de execução
    report = defaultdict(lambda: {"posts": 0, "users": set()})

    # Divide listas
    splits = ["train", "test", "validation"]
    real_splits = split_usernames(usernames_real)
    brainrot_splits = split_usernames(usernames_brainrot)

    for i, split in enumerate(splits):
        for category, usernames in [("real", real_splits[i]), ("brainrot", brainrot_splits[i])]:
            csv_path = os.path.join(BASE_DIR, split, f"dataset_{split}_{category}.csv")
            init_csv(csv_path)

            for username in usernames:
                if not username:
                    continue

                # Pula usernames já processados
                if username in completed:
                    print(f"[skip] {username} já processado anteriormente.")
                    continue

                try:
                    print(f"[{split.upper()}] {category} -> {username}")

                    data = scraper.get(username, type="clean" if not save_imgs else "bs64")
                    dir_name = os.path.join(BASE_DIR, split, category)
                    scraper.save(dir_name)

                    if data:
                        profile = data.get("profile", {})
                        posts = data.get("posts", [])

                        append_to_csv(csv_path, platform, profile, posts)

                        # Atualiza relatório
                        key = f"{split}_{category}"
                        report[key]["users"].add(profile.get("username"))
                        report[key]["posts"] += len(posts)

                        # Marca como completo
                        save_completed_user(username)

                except Exception as e:
                    print(f"❌ ERROR with {username}: {e}")
                    continue

    # Exibe relatório final
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO FINAL DE EXECUÇÃO")
    print("=" * 60)

    for key, data in report.items():
        split, category = key.split("_")
        print(f"{split.upper()} - {category.capitalize()}")
        print(f"  • Usernames distintos: {len(data['users'])}")
        print(f"  • Total de posts: {data['posts']}\n")

    print("✅ Dataset gerado com sucesso em /dist/")
    print("=" * 60 + "\n")


# ===========================
# EXECUÇÃO
# ===========================
if __name__ == "__main__":
    usernames_real = [
        "@JoojNatu",
        "@triplecharm",
        "@ryan_samuel8",
        "@emozgaming",
        "@GrimShorts",
        "@julseyhiphop",
        "@SwiftieTikToks",
        "@realjulianbanks",
        "@iiNoodleDoodleii",
        "@GLArt",
    ]

    usernames_brainrot = [
        "@SHORT9999-s3t", 
        "@warungtungtung", 
        "@Kerstle", 
        "@SamShortFunny9999",
        "@B.hai20k",
        "@sungkepgameshorts",
        "@Ronalvagundes-r9",
        "@JANNATIYT1",
        "@TalezoraAi",
        "@catlove-b4x"
    ]

    run_batch_by_category(
        strategy="y",
        usernames_real=usernames_real,
        usernames_brainrot=usernames_brainrot,
        save_imgs=True
    )
