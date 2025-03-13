# Поднятие Jenkins с Docker (Docker-in-Docker) 🚀

#
Данный гайд поможет вам развернуть Jenkins в Docker, при этом внутри контейнера будет доступен Docker хостовой машины. Это позволит запускать CI/CD-пайплайны с Docker внутри самого Jenkins.
--

> **ОЧЕНЬ Важно:** Перед тем как начинать тестирование в Jenkins убедитесь, что вы остановили все контейнеры данного приложения или других!!! Так как jenkins использует докер хостовой машины НЕЛЬЗЯ будет отсавить прилодение локально и запускать его в jenkins(это приведет к конфликту)

---


## 1. Сборка образа Jenkins
Выполните команду в директории CI:

```
docker build -t myjenkins .
```

Этот шаг создаст новый образ Docker с Jenkins, в котором установлен Docker CLI.

## 2. Создание сети Docker
Для удобного взаимодействия между контейнерами создайте Docker-сеть:

```
docker network create jenkins
```
## 3. Запуск контейнера с Jenkins
Запустите Jenkins-контейнер, передав ему доступ к Docker хостовой машины:

```
docker run \
  --name jenkins-with-docker \
  --restart=on-failure \
  --detach \
  --network jenkins \
  --publish 8080:8080 \
  --publish 50000:50000 \
  --volume jenkins-data-flask:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  myjenkins
```
Что здесь происходит:

Контейнер именуется jenkins-with-docker.
Контейнер перезапускается при сбое (--restart=on-failure).
Открыты порты:
8080 — для веб-интерфейса Jenkins.
50000 — для подключения агентов Jenkins.
Хостовой Docker-сокет передаётся в контейнер (-v /var/run/docker.sock:/var/run/docker.sock), что позволяет запускать Docker-контейнеры внутри Jenkins.
## 4. Получение пароля администратора Jenkins
Выполните команду:

```
docker exec jenkins-with-docker cat /var/jenkins_home/secrets/initialAdminPassword
```
Запомните этот пароль — он понадобится при первоначальной настройке Jenkins.

## 5. Настройка группы Docker внутри Jenkins
Чтобы Jenkins мог запускать пайплайны с Docker, нужно добавить пользователя jenkins в группу docker.

Войдите в контейнер от имени root:

```
docker exec -it --user root jenkins-with-docker bash

```
Внутри контейнера выполните следующие команды:

```
# Меняем права на Docker-сокет, чтобы обеспечить доступ
chmod 666 /var/run/docker.sock

# Выход из контейнера
exit
```
Перезапустите контейнер:

```
docker restart jenkins-with-docker
```

## 6. Проверка работы Docker внутри Jenkins
После перезапуска проверьте, что Docker внутри контейнера работает:

```
docker exec jenkins-with-docker docker ps
```
Если команда выполняется без ошибок — Docker настроен правильно.

## 7. Открытие Jenkins в браузере
Откройте Jenkins в браузере по адресу:


http://localhost:8080

При первом запуске введите пароль администратора из шага 5.

## 8. Установка плагинов

Установите предлагаемые плагины и создайте нового пользователя


## 9. Установка Allure

Перейдите в Manage Jenkins -> Plugins -> Available plugins

найдите Allure и установите

Перейдите в Manage Jenkins -> Tools -> Allure Commandline installations
введите allure и нажмите сохранить

после данных дейтсвий перезагрузите jenkins
```
docker restart jenkins-with-docker
```


## 9. Запуск тестов в Jenkins
Задача заключается в том, чтобы добиться успешной установки Jenkins и запустить любой тест в новой Jenkins-джобе. Для этого:

Создайте новую задачу (job) в Jenkins.
Настройте её так, чтобы запускались тесты вашего проекта (пример запуска предоставлен в Jenkinsfile)

Пример 

http://localhost:8080/view/all/newJob

введите имя и выберите тип Pipeline

Нажмите на чекбокс GitHub hook trigger for GITScm polling

В поле Pipeline -> Definition выберите Pipeline script from SCM

в SCM - git

в Branch Specifier - */main

в Repository URL укажите линк совего репозитория


## 10. Проброс Webhook для GitHub с помощью ngrok
Чтобы настроить вебхук для GitHub, понадобится ngrok.

Скачайте и установите ngrok.

Запустите команду для проброса локального порта:

```
ngrok http 8080
```

Ngrok выдаст публичный URL. Используйте его для настройки вебхука в репозитории GitHub.

## 11. Выствление Webhook

Перейдите в Github проект -> Settings -> Webhooks

в поле Payload URL ввидеите url полученный на 10 шаге добавив в конце /github-webhook/

пример:
```
https://7d23-209-206-23-75.ngrok-free.app/github-webhook/
```


После выполения данных дейтсвий у вас будет готовая джоба для запуска базовых тестов данного приложения.
