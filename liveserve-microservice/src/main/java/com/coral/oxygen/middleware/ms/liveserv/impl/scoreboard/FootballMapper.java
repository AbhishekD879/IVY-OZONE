package com.coral.oxygen.middleware.ms.liveserv.impl.scoreboard;

import com.coral.oxygen.middleware.ms.liveserv.model.scoreboard.ScoreboardEvent;
import java.util.Objects;
import javax.json.Json;
import javax.json.JsonArray;
import javax.json.JsonObject;
import javax.json.JsonObjectBuilder;
import javax.json.JsonValue;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class FootballMapper {

  private static final String FOOTBALL_JSON_PROPERTY = "football";
  private static final String OB_EVENT_ID_JSON_PROPERTY = "obEventId";
  private static final String PLAYERS_JSON_PROPERTY = "players";
  private static final String HOME_JSON_PROPERTY = "home";
  private static final String AWAY_JSON_PROPERTY = "away";

  public String map(ScoreboardEvent scoreboardEvent) {
    JsonObject eventStructure = scoreboardEvent.getEventStructure();
    JsonObjectBuilder footballBuilder = Json.createObjectBuilder(eventStructure);

    footballBuilder.add(OB_EVENT_ID_JSON_PROPERTY, scoreboardEvent.getObEventId());

    JsonObject players = eventStructure.getJsonObject(PLAYERS_JSON_PROPERTY);

    if (Objects.nonNull(players)) {
      JsonArray home = players.getJsonArray(HOME_JSON_PROPERTY);
      JsonArray away = players.getJsonArray(AWAY_JSON_PROPERTY);

      JsonObjectBuilder playerBuilder = Json.createObjectBuilder(players);
      playerBuilder
          .remove(HOME_JSON_PROPERTY)
          .remove(AWAY_JSON_PROPERTY)
          .add(HOME_JSON_PROPERTY, playersTeamMapper(home))
          .add(AWAY_JSON_PROPERTY, playersTeamMapper(away));

      footballBuilder
          .remove(PLAYERS_JSON_PROPERTY)
          .add(PLAYERS_JSON_PROPERTY, playerBuilder.build());
    }

    JsonObjectBuilder structureBuilder = Json.createObjectBuilder();
    structureBuilder.add(FOOTBALL_JSON_PROPERTY, footballBuilder.build());
    return structureBuilder.build().toString();
  }

  private JsonObject playersTeamMapper(JsonArray team) {
    JsonObjectBuilder objectBuilder = Json.createObjectBuilder();
    team.stream()
        .map(JsonValue::asJsonObject)
        .forEach(jsonObj -> objectBuilder.add(jsonObj.getString("id"), jsonObj));
    return objectBuilder.build();
  }
}
