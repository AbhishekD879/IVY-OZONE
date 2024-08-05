package com.coral.oxygen.middleware.ms.liveserv.impl.scoreboard;

import com.coral.oxygen.middleware.ms.liveserv.model.scoreboard.ScoreboardEvent;
import java.util.Optional;
import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonObjectBuilder;

public class EventMapper {

  public Optional<ScoreboardEvent> sportMapper(ScoreboardEvent scoreboardEvent) {
    return jsonSportMapper(scoreboardEvent)
        .map(json -> new ScoreboardEvent(scoreboardEvent.getObEventId(), json));
  }

  private Optional<String> jsonSportMapper(ScoreboardEvent scoreboardEvent) {
    switch (scoreboardEvent.getSportCategory()) {
      case "football":
        return Optional.of(new FootballMapper().map(scoreboardEvent));
      case "tennis":
      default:
        break;
    }
    return Optional.empty();
  }

  public String mapToUpdateStructure(JsonObject rawDiffStructure, String obEventId) {
    String sportCategoryKey = rawDiffStructure.keySet().iterator().next();
    JsonObjectBuilder builder =
        Json.createObjectBuilder(rawDiffStructure.getJsonObject(sportCategoryKey));
    builder.add("obEventId", obEventId);
    return builder.build().toString();
  }
}
