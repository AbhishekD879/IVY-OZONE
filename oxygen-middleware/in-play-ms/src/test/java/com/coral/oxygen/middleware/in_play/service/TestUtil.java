package com.coral.oxygen.middleware.in_play.service;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.Collectors;
import lombok.SneakyThrows;

public class TestUtil {

  @SneakyThrows(Exception.class)
  public static String getResourceByPath(String filePath) {
    return Files.lines(Paths.get(ClassLoader.getSystemResource(filePath).toURI()))
        .collect(Collectors.joining(" "));
  }
}
