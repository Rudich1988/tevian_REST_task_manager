## Проект анализатор страниц
Task_manager - сервис с REST API на основе HTTP с передачей данных в формате
JSON. Сервис ведет список заданий. В задание загружаются изображения в выбранную вами директорию. С помощью стороннего сервиса на изображениях находятся лица,
определяются их пол и возраст. На основе полученных данных сервис ведет статистику.

### Как развернуть проект:
- Создайте в корне проекта файл .env
- Изучите документацию по ссылке [Tevian](https://docs.facecloud.tevian.ru/), создайте свой аккаунт и получите токен
- Изучите содержимое файла .env.example. В нем содержатся примеры переменных, которые Вы должны создать в файле .env
- В FILEPATH должен содержаться путь к директории, куда будут загружаться файлы
- Экспортируйте переменные, например:
```bash
export FILEPATH=filepath
```
- Запуск:
```bash
poetry install
poetry shell
make dev
```

### Примеры запросов:
- Создание задачи
```bash
curl -u "yourmail@gmail.com:password" -H "Content-Type: application/json" -X POST -d '{"title": "task_name"}' http://hostname:port/tasks
```
- Загрузка файла в задачу
```bash
curl -u "yourmail@gmail.com:password" -F "file=@/путь/до/Изображения/image.jpg" -F "task_id={task_id}" http://host:port/images
```
- Просмотр задачи
```bash
curl -u "yourmail@gmail.com:password" http://host:port/tasks/id
```