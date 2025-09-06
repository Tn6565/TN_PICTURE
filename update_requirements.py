import pkg_resources
import os

# 追記したいパッケージリスト
packages_to_add = ["matplotlib", "sentence-transformers", "torch", "python-dotenv"]

# 現在の環境でインストールされているパッケージとバージョンを取得
installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}

# requirements.txt の既存内容を取得（存在しない場合は空リスト）
requirements_path = "requirements.txt"
existing_lines = []
if os.path.exists(requirements_path):
    with open(requirements_path, "r") as f:
        existing_lines = [line.strip().lower() for line in f if line.strip()]

# 重複を避けつつ追記
with open(requirements_path, "a") as f:
    for pkg in packages_to_add:
        pkg_lower = pkg.lower()
        line_to_add = f"{pkg}=={installed_packages[pkg_lower]}"
        if not any(line_lower.startswith(pkg_lower + "==") for line_lower in existing_lines):
            f.write(line_to_add + "\n")
            print(f"追加: {line_to_add}")
        else:
            print(f"既存: {pkg} はすでに requirements.txt にあります")

print("requirements.txt の更新が完了しました。")
