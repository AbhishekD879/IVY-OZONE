package com.ladbrokescoral.oxygen.betradar.client.entity;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class Season {

  private String id;
  private String startDate;
  private String sportId;
  private String name;
  private String endDate;
  private String year;
  private String competitionId;
  private String areaId;
  private String uniqueId;
}
