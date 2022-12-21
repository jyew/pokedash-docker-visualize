# Docker Dash Example with Pokemon Visualization
A simple containerized dash app that shows basic visualization of pokemon stats.

### Structure
```
├── app.py
├── pokemon_jpg
├── Dockerfile
├── pokemon.csv
├── requirements.txt
└── README.md
```

### Run docker image locally
cd into the pokedash-docker-visualize folder and:
```
docker build -t pokedash .
```
And run the container
```
docker run -p 8050:8050 pokedash
```
The app is up and running on your local machine http://0.0.0.0:8050/.