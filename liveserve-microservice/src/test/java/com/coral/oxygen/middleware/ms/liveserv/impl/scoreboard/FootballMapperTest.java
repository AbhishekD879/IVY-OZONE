package com.coral.oxygen.middleware.ms.liveserv.impl.scoreboard;

import static org.junit.jupiter.api.Assertions.assertFalse;

import com.coral.oxygen.middleware.ms.liveserv.model.scoreboard.ScoreboardEvent;
import com.google.common.io.CharStreams;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.StringReader;
import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonReader;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class FootballMapperTest {

  private FootballMapper footballMapper;

  @Before
  public void setup() {
    footballMapper = new FootballMapper();
  }

  @Test
  public void mappingTest() throws IOException {
    JsonObject football = getJsonObjectFromStream("datafeed/scoreboard0.json");
    ScoreboardEvent footballEvent = new ScoreboardEvent("123123", football);

    JsonObject jsonObject =
        getJsonObject(footballMapper.map(footballEvent)).getJsonObject("football");

    assertFalse(jsonObject.isNull("obEventId"));
    assertFalse(jsonObject.isNull("players"));
  }

  private JsonObject getJsonObjectFromStream(String s) throws IOException {
    try (InputStreamReader inputStreamReader =
            new InputStreamReader(getClass().getClassLoader().getResourceAsStream(s));
        StringReader reader = new StringReader(CharStreams.toString(inputStreamReader));
        JsonReader jsonReader = Json.createReader(reader)) {
      return jsonReader.readObject();
    }
  }

  private JsonObject getJsonObject(String data) {
    try (StringReader reader = new StringReader(data);
        JsonReader jsonReader = Json.createReader(reader)) {
      return jsonReader.readObject();
    }
  }
}
