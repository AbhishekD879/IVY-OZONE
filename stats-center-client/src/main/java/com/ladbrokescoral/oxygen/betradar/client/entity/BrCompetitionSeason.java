package com.ladbrokescoral.oxygen.betradar.client.entity;

import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode
public class BrCompetitionSeason {
  private Integer sportId; // 1
  private String sportName; // Soccer
  private Integer areaId; // 4
  private String areaName; // International
  private Integer competitionId; // 3961
  private String competitionName; // "World Cup, Group H"
  private List<StatsCompetition> allCompetitions;
  private List<StatsSeason> allSeasons;
}
