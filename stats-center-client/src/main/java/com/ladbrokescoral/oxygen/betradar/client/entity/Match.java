package com.ladbrokescoral.oxygen.betradar.client.entity;

import lombok.Data;

@Data
public class Match {
  private MatchResult result;
  private Team teamA;
  private Team teamB;
}
