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

If everything goes right, you should see a dashboard of Pokemon metrics. Feel free to change to any pokemon to see its ability breakdown.

![image](https://user-images.githubusercontent.com/16984251/208857862-bbd6ecdf-a408-47be-a0b4-e28658ebacc5.png)

![image](https://user-images.githubusercontent.com/16984251/208857959-04f32bd2-8c5c-4d1e-93cd-5c69e52b6e64.png)

![image](https://user-images.githubusercontent.com/16984251/208858021-e1922584-2d8e-4c77-9133-01029a4234b6.png)
