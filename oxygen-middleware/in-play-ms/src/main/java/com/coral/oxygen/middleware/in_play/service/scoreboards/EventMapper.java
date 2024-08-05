package com.coral.oxygen.middleware.in_play.service.scoreboards;

import java.util.Optional;
import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonObjectBuilder;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@Slf4j
public class EventMapper {

  private static final String OB_EVENT_ID = "obEventId";

  private final FootballMapper footballMapper;

  public Optional<ScoreboardEvent> sportMapper(ScoreboardEvent scoreboardEvent) {
    return jsonSportMapper(scoreboardEvent)
        .map(json -> new ScoreboardEvent(scoreboardEvent.getObEventId(), json));
  }

  private Optional<String> jsonSportMapper(ScoreboardEvent scoreboardEvent) {
    return Optional.of(footballMapper.map(scoreboardEvent));
  }

  public String mapToUpdateStructure(JsonObject rawDiffStructure, String obEventId) {
    String sportCategoryKey = rawDiffStructure.keySet().iterator().next();
    JsonObjectBuilder builder =
        Json.createObjectBuilder(rawDiffStructure.getJsonObject(sportCategoryKey));
    builder.add(OB_EVENT_ID, obEventId);
    return builder.build().toString();
  }
}
