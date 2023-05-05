import requests
import json

# Hacemos una solicitud GET a la API de GitHub para obtener información de nuestro usuario
response = requests.get('https://api.github.com/users/dmarsal90/repos')

# Convertimos la respuesta a un objeto JSON
data = response.json()

# Obtenemos el número total de repositorios
num_repos = len(data)

# Inicializamos las variables para contar los commits y push
num_commits = 0
num_push = 0

# Recorremos todos los repositorios y contamos los commits y push
for repo in data:
    # Hacemos una solicitud GET a la API de GitHub para obtener información sobre los commits del repositorio
    commits_response = requests.get(f"https://api.github.com/repos/dmarsal90/{repo['name']}/commits")

    # Convertimos la respuesta a un objeto JSON
    commits_data = commits_response.json()

    # Añadimos el número de commits al total
    num_commits += len(commits_data)

    # Recorremos todos los commits y contamos los push
    for commit in commits_data:
        if 'pushed_at' in commit['commit']['author']:
            num_push += 1

# Imprimimos las estadísticas para verificar que se hayan obtenido correctamente
print(f"Number of public repositories: {num_repos}")
print(f"Number of commits: {num_commits}")
print(f"Number of pushes: {num_push}")
