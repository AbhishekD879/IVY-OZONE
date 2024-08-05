package com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.banach;

/** Created by JacksonGenerator on 5/4/18. */
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class BetPlacementItem {
  private String date;
  private String betPotentialWin;
  private Integer numLines;
  private Integer betNo;
  private Long betId;
  private String receipt;
  private String totalStake;
}
