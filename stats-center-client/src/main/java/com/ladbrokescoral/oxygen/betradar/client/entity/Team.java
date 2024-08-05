package com.ladbrokescoral.oxygen.betradar.client.entity;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class Team {
  private String id;
  private String betradarTeamId;
  private String name;
  private String gender;
  private String type;
  private String formation;
  private Country country;
  private String winner;
}
