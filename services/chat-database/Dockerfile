# syntax=docker/dockerfile:1

FROM eclipse-temurin:25-jdk-noble AS build
WORKDIR /workspace

COPY gradlew settings.gradle build.gradle ./
COPY gradle gradle
RUN chmod +x gradlew && ./gradlew --no-daemon dependencies

COPY src src
RUN ./gradlew --no-daemon bootJar

FROM eclipse-temurin:25-jre-noble

RUN groupadd --system app \
  && useradd --system \
  --gid app \
  --home-dir /home/app \
  --create-home \
  --shell /usr/sbin/nologin \
  app

WORKDIR /app

COPY --chown=app:app --from=build /workspace/build/libs/*.jar app.jar

USER app
EXPOSE 8080

ENTRYPOINT ["java", "-jar", "/app/app.jar"]
