package com.coral.oxygen.middleware.ms.liveserv.model.incidents;

import java.io.StringReader;
import java.util.Objects;
import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonReader;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.Transient;

@NoArgsConstructor
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class IncidentsEvent {

  @Id @Getter @Setter @EqualsAndHashCode.Include private String eventId;
  @Getter @EqualsAndHashCode.Include private String incidentsData;

  @Transient private JsonObject jsonStructure;

  public IncidentsEvent(String eventId, String data) {
    this.eventId = eventId;
    this.incidentsData = data;
    setRawStructure(data);
  }

  private void setRawStructure(String data) {
    if (data != null) {
      try (StringReader reader = new StringReader(data);
          JsonReader jsonReader = Json.createReader(reader)) {
        this.jsonStructure = jsonReader.readObject();
      }
    }
  }

  private JsonObject getRawStructure() {
    if (Objects.isNull(jsonStructure)) {
      setRawStructure(incidentsData);
    }
    return jsonStructure;
  }

  public JsonObject getEventStructure() {
    return getRawStructure().getJsonObject(getKey());
  }

  public String getKey() {
    return getRawStructure().keySet().iterator().next();
  }
}
