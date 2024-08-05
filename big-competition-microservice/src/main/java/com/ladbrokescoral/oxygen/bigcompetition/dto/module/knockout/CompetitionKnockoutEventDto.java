package com.ladbrokescoral.oxygen.bigcompetition.dto.module.knockout;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.ladbrokescoral.oxygen.bigcompetition.dto.ParticipantDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.EventDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.statsCenter.MatchResultDto;
import java.util.HashMap;
import java.util.Map;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_EMPTY)
public class CompetitionKnockoutEventDto {
  private Integer eventId;
  private String homeTeam;
  private String awayTeam;
  private String homeTeamRemark;
  private String awayTeamRemark;
  private String venue;
  private String startTime;
  private String round;
  private String abbreviation;
  private boolean isResulted;
  private MatchResultDto result;
  private String eventName;
  private EventDto obEvent;
  private Map<String, ParticipantDto> participants = new HashMap<>();
}
