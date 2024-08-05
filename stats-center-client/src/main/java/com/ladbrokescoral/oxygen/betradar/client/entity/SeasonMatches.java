package com.ladbrokescoral.oxygen.betradar.client.entity;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import java.util.List;
import lombok.Data;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class SeasonMatches {
  private String _id;
  private String kickOffTime;
  private long date;
  private Team teamA;
  private Team teamB;
  private String canceled;
  private Result result;
  private String id;
  private List<Goals> goals;
  private Season season;
}
