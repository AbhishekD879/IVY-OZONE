package com.coral.oxygen.middleware.in_play.service.scoreboards;

import javax.json.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
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

    JsonValue jsonValue = eventStructure.get(PLAYERS_JSON_PROPERTY);

    if (jsonValue instanceof JsonObject) {
      JsonObject players = (JsonObject) jsonValue;
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
