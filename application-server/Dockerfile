#FROM openjdk:25-rc-jdk-slim-trixie
FROM gradle:9.4.1-jdk25 AS build

WORKDIR /app

COPY build.gradle ./
COPY src ./src

RUN gradle bootJar --no-daemon

#FROM eclipse-temurin:25
FROM openjdk:25-rc-jdk-slim-trixie

WORKDIR /app

COPY --from=build /app/build/libs/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]