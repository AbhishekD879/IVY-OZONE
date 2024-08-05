package com.entain.oxygen;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.Collectors;
import lombok.SneakyThrows;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.web.reactive.server.WebTestClient;

public abstract class AbstractControllerTest {

  @Autowired protected WebTestClient webTestClient;

  @SneakyThrows(Exception.class)
  public static String getResourceByPath(String filePath) {
    return Files.lines(Paths.get(ClassLoader.getSystemResource(filePath).toURI()))
        .collect(Collectors.joining(" "));
  }
}
