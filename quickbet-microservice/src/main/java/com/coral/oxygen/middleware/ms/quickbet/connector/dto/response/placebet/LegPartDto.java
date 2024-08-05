package com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet;

import lombok.Data;

@Data
public class LegPartDto {
  private String eventId;
  private String eventDesc;
  private String marketId;
  private String marketDesc;
  private String outcomeId;
  private String outcomeDesc;
  private Integer eachWayNum;
  private Integer eachWayDen;
  private Integer eachWayPlaces;
  private String handicap;
}
