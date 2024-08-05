package com.coral.oxygen.middleware.in_play.service.scoreboards;

import java.io.StringReader;
import java.util.Objects;
import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonReader;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.Transient;
import org.springframework.data.redis.core.RedisHash;

@RedisHash(value = "${df.scoreboard.messages}", timeToLive = 24 * 3600) // 24 hours
@NoArgsConstructor
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
@Slf4j
public class ScoreboardEvent {
  @Id @Getter @Setter @EqualsAndHashCode.Include private String obEventId;
  @Getter @EqualsAndHashCode.Include private String data;

  @Transient private JsonObject structure;
  @Transient private String sportCategory;

  public ScoreboardEvent(String obEventId, String data) {
    this.obEventId = obEventId;
    this.data = data;
    setRawStructure(data);
  }

  private void setRawStructure(String data) {
    try (StringReader reader = new StringReader(data);
        JsonReader jsonReader = Json.createReader(reader)) {
      this.structure = jsonReader.readObject();
    } catch (Exception e) {
      structure = null;
    }
  }

  public JsonObject getRawStructure() {
    if (Objects.isNull(structure)) {
      setRawStructure(data);
    }
    return structure;
  }

  public JsonObject getEventStructure() {
    return getRawStructure().getJsonObject(getSportCategory());
  }

  public String getSportCategory() {
    if (Objects.isNull(sportCategory)) {
      sportCategory = getRawStructure().keySet().iterator().next();
    }
    return sportCategory;
  }

  public Integer getSequenceId() {
    return getEventStructure().getInt("sequenceId");
  }

  public boolean isNewer(ScoreboardEvent otherEvent) {
    return this.getSequenceId() > otherEvent.getSequenceId();
  }
}
