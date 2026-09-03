import svgwrite
import requests
import re
from datetime import datetime, timedelta

username = 'macielguilherme'

# Buscar dados de contribuições
url = f'https://github.com/users/{username}/contributions'
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
html = response.text

# Extrair dados de contribuições
contributions = re.findall(r'data-count="(\d+)"', html)
dates = re.findall(r'data-date="(\d{4}-\d{2}-\d{2})"', html)

if not contributions:
    print("Não foi possível obter dados. Usando dados de exemplo...")
    # Dados de exemplo se falhar
    contributions = [str((i % 5)) for i in range(364)]
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(364)]

# Criar SVG
dwg = svgwrite.Drawing('dist/github-snake.svg', size=(800, 200))
dwg.add(dwg.rect(insert=(0,0), size=(800,200), fill='#ffffff'))

# Cores por intensidade
colors = ['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39']

# Desenhar contribuições
for i, count in enumerate(contributions[:364]):
    week = i // 7
    day = i % 7
    x = week * 15 + 10
    y = day * 25 + 10
    intensity = min(int(count) if count.isdigit() else 0, 4)
    dwg.add(dwg.rect(insert=(x,y), size=(12,12), fill=colors[intensity], rx=2))

# Adicionar cabeçalho
dwg.add(dwg.text('Contribuições no GitHub - 2026', insert=(10, 185), fill='#333', font_size='12'))

dwg.save()
print("SVG gerado com sucesso em dist/github-snake.svg!")