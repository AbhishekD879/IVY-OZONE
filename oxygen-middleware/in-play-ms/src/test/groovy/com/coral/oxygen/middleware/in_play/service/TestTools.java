package com.coral.oxygen.middleware.in_play.service;

import com.coral.oxygen.middleware.JsonFacade;
import com.coral.oxygen.middleware.pojos.model.cms.CmsInplayData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData;
import com.google.gson.Gson;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.Collectors;
import lombok.SneakyThrows;

/** Created by azayats on 28.01.17. */
public class TestTools {

  public static final Gson GSON = JsonFacade.PRETTY_GSON;

  public static InPlayData inPlayDataFromFile(String name) {
    return fromFile(name, InPlayData.class);
  }

  public static CmsInplayData initialDataFromFile(String name) {
    return fromFile(name, CmsInplayData.class);
  }

  public static <T> T fromFile(String name, Class<T> clazz) {
    InputStream stream = TestTools.class.getClassLoader().getResourceAsStream(name);
    return GSON.fromJson(new InputStreamReader(stream), clazz);
  }

  public static void store(Object o, String name) {
    String json = GSON.toJson(o);
    try {
      PrintWriter writer = new PrintWriter(name);
      writer.print(json);
      writer.close();
    } catch (FileNotFoundException e) {
      e.printStackTrace();
    }
  }

  @SneakyThrows(Exception.class)
  public static String getResourceByPath(String filePath) {
    return Files.lines(Paths.get(ClassLoader.getSystemResource(filePath).toURI()))
        .collect(Collectors.joining(" "));
  }
}
