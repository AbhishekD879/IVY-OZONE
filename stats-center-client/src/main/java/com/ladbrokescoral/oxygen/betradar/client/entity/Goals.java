package com.ladbrokescoral.oxygen.betradar.client.entity;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class Goals {

  private String id;
  private String time;
  private String playerID;
  private String playerName;
  private String team;
  private String shootout;
  private String date;
  private String type;
  private String homeTeamScore;
  private String awayTeamScore;
}
