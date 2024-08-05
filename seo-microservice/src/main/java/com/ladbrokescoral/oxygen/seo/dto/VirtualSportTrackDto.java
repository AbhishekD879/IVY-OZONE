package com.ladbrokescoral.oxygen.seo.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;
import java.util.Map;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

@Data
@NoArgsConstructor
@Accessors(chain = true)
public class VirtualSportTrackDto {
  private String id;
  private String title;
  private String classId;
  private String className;
  private String streamUrl;
  private Integer numberOfEvents;
  private boolean showRunnerImages;
  private boolean showRunnerNumber;

  @JsonIgnore private Map<String, String> eventAliases;
}
