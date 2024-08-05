package com.ladbrokescoral.oxygen.cms.api.entity.timeline.spotlight;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.Map;
import lombok.Data;

@Data
public class SpotlightItems {
  @JsonProperty("document")
  private Map<String, SpotlightEventInfo> spotlightPostsByEventId;

  @JsonProperty("Error")
  private Boolean error;
}
