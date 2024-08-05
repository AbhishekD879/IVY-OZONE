package com.coral.oxygen.middleware.ms.quickbet.connector.dto.request;

import java.io.Serializable;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class CalculateOddsRequestDto implements Serializable {
  private Integer betType;
  private Integer conditionType;
  private String conditionValue;
  private Integer game1Id;
  private Integer game2Id;
  private Integer game3Id;
  private Integer game4Id;
  private Integer player1Id;
  private Integer player2Id;
  private Integer player3Id;
  private Integer player4Id;
  private Integer statisticId;
}
