package com.ladbrokescoral.oxygen.cms.api.entity.timeline.spotlight;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class SpotlightEventInfo {
  String raceName;
  String verdict;
  List<HorseInfo> horses = new ArrayList<>();

  Object error;

  @Data
  @JsonIgnoreProperties(ignoreUnknown = true)
  public static class HorseInfo {
    private String rpHorseId;
    private String horseName;
    private String spotlight;
    private String saddle;
    private String selectionId;
  }
}
