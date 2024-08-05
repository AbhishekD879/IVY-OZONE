package com.coral.oxygen.middleware.pojos.model.output;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.google.gson.annotations.SerializedName;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@EqualsAndHashCode(callSuper = true)
@Data
@NoArgsConstructor
public class VirtualRaceModuleData extends BasicRacingEventData {

  @SerializedName("@type")
  @JsonProperty("@type")
  private String type = "VirtualRaceModuleData";

  private String classId;
}
