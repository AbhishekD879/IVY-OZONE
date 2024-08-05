package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CompetitionKnockoutEvent {

  private Integer eventId; // OpenBet event id
  private String homeTeam;
  private String awayTeam;
  private String homeTeamRemark;
  private String awayTeamRemark;
  private String venue;
  private String startTime;
  private String round;
  private String abbreviation;
  private String eventName;
}
