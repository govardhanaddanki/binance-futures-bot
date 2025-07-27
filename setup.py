import os

folders = [
    "src",
    "src/advanced"
]

files = {
    "src/market_orders.py": "",
    "src/limit_orders.py": "",
    "src/advanced/oco.py": "",
    "src/advanced/twap.py": "",
    "src/advanced/grid_strategy.py": "",
    "bot.log": "",
    "README.md": ""
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files
for file_path, content in files.items():
    with open(file_path, "w") as f:
        f.write(content)

print("Project structure created successfully.")

