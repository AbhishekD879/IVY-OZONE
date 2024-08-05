package com.entain.oxygen.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.List;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
@SuppressWarnings("java:S1820")
public class OutcomeDto {
  private String id;
  private String marketId;
  private String name;
  private String outcomeMeaningMajorCode;
  private String outcomeMeaningMinorCode;
  private String outcomeMeaningScores;
  private Integer runnerNumber;
  private Boolean isResulted;
  private Integer displayOrder;
  private String outcomeStatusCode;
  private Boolean isActive;
  private Boolean isDisplayed;
  private String siteChannels;
  private String liveServChannels;
  private String liveServChildrenChannels;
  private String liveServLastMsgId;
  private String drilldownTagNames;
  private Boolean isAvailable;
  private Boolean isFinished;
  private String hasRestrictedSet;
  private Boolean isEnhancedOdds;
  private String cashoutAvail;
  private String resultCode;
  private String position;
  private boolean hasPriceStream;
  private String teamExtIds;
  private String participantIds;
  private List<ChildrenDto> children;
}
