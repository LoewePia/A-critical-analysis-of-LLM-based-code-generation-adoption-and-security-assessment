<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
   <modelVersion>4.0.0</modelVersion>
   <parent>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-parent</artifactId>
      <version>2.6.3</version> <!-- Updated version -->
      <relativePath/> <!-- lookup parent from repository -->
   </parent>
   <groupId>com.baseGPT</groupId>
   <artifactId>spring-rest-api-base-GPT</artifactId>
   <version>0.0.1-SNAPSHOT</version>
   <name>spring-rest-api-base-GPT</name>
   <description>project for Spring Boot created by GPT4</description>
   <properties>
      <java.version>17</java.version>
   </properties>
   <dependencies>
      <!-- Spring Boot Starter Web -->
      <dependency>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-starter-web</artifactId>
      </dependency>
      <!-- Spring Boot Starter Security -->
      <dependency>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-starter-security</artifactId>
      </dependency>
      <!-- Spring Boot Starter Test -->
      <dependency>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-starter-test</artifactId>
         <scope>test</scope>
      </dependency>
      <!-- JWT -->
      <dependency>
         <groupId>io.jsonwebtoken</groupId>
         <artifactId>jjwt-api</artifactId>
         <version>0.11.2</version>
      </dependency>
      <dependency>
         <groupId>io.jsonwebtoken</groupId>
         <artifactId>jjwt-impl</artifactId>
         <version>0.11.2</version>
         <scope>runtime</scope>
      </dependency>
      <dependency>
         <groupId>io.jsonwebtoken</groupId>
         <artifactId>jjwt-jackson</artifactId>
         <version>0.11.2</version>
         <scope>runtime</scope>
      </dependency>
   </dependencies>

   <build>
      <plugins>
         <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
         </plugin>
      </plugins>
   </build>
</project>