# Чтоб работало

## Склонировать репозиторий 
```
git clone https://github.com/bvh2vgtp-k/PITlab.git
```
## Собрать проект спомощю docker-compose
```
docker-compose up --build
```
всё должно работать 

## Если не работает 
Собрать образ
```
docker build -t myapp .
```

запустить контейнер 
```
docker run -d -p 8080:8080 --name myapp-server myapp
```

## Использование
`index.html` отдаётся с бека, такчто всё что надо после запуска сервера это перейти на `http://localhost:8080/` он отдаст `index.html`

