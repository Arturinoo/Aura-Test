@echo off
chcp 65001 > nul
echo 🔧 Oprava chyby importu AIAssistant...
echo.

cd /d "C:\Aura Test"

echo 🗑️  Vymazávam Python cache...
if exist "core\__pycache__" rmdir /s /q "core\__pycache__"
if exist "__pycache__" rmdir /s /q "__pycache__"

echo 📄 Kontrolujem core\assistant.py...
python -c "
import ast
with open('core/assistant.py', 'r', encoding='utf-8') as f:
    content = f.read()
    try:
        tree = ast.parse(content)
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        print('Triedy v assistant.py:', classes)
        if 'AIAssistant' in classes:
            print('✅ AIAssistant nájdená!')
        else:
            print('❌ AIAssistant nenájdená!')
    except Exception as e:
        print('❌ Chyba syntaxe:', e)
"

echo.
echo 🚀 Spúšťam aplikáciu...
python main.py

pause