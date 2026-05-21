#FROM openjdk:25-rc-jdk-slim-trixie
FROM gradle:9.4.1-jdk25 AS build

WORKDIR /app

COPY . .
#COPY build.gradle ./
#COPY /application-server/src ./src

RUN gradle :application-server:bootJar --no-daemon

#FROM eclipse-temurin:25
FROM openjdk:25-rc-jdk-slim-trixie

WORKDIR /app

COPY --from=build /app/application-server/build/libs/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]