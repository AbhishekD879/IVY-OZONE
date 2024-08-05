package com.coral.oxygen.middleware.pojos.model.output;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.google.gson.annotations.SerializedName;
import java.util.Map;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public class InternationalToteRaceData extends BasicRacingEventData {

  @SerializedName("@type")
  @JsonProperty("@type")
  private String type = "InternationalToteRaceData";

  private String categoryId;
  private String categoryCode;
  private String typeName;
  private Boolean resulted;
  private Boolean started;
  private Boolean liveNowEvent;
  private Map<String, String> externalKeys;
}
