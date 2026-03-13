import ast

try:
    ast.parse(open('secure_career_system/app.py').read())
    print('app.py: OK')
except Exception as e:
    print(f'app.py: ERROR - {e}')

try:
    ast.parse(open('secure_career_system/models.py').read())
    print('models.py: OK')
except Exception as e:
    print(f'models.py: ERROR - {e}')
