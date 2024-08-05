package com.oxygen.publisher.sportsfeatured.model.module.data;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.Map;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
public class InternationalToteRaceData extends AbstractModuleData {
  private String name;
  private String categoryId;
  private String categoryCode;
  private String typeName;
  private String startTime;

  @JsonProperty("isResulted")
  @JsonAlias("resulted")
  private Boolean resulted;

  @JsonProperty("isStarted")
  @JsonAlias("started")
  private Boolean started;

  @JsonProperty("isLiveNowEvent")
  @JsonAlias("liveNowEvent")
  private Boolean liveNowEvent;

  private Map<String, String> externalKeys;
  private String effectiveGpStartTime;
}
