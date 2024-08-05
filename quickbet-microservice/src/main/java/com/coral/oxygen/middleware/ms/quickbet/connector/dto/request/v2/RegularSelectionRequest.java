package com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2;

import java.util.List;
import lombok.Data;
import lombok.NoArgsConstructor;

/** Created by azayats on 23.11.17. */
@Data
@NoArgsConstructor
public class RegularSelectionRequest {
  public static final String SIMPLE_SELECTION_TYPE = "simple";
  public static final String SCORECAST_SELECTION_TYPE = "scorecast";

  private List<Long> outcomeIds;
  private String selectionType;
  private AdditionalParameters additional;
  private String token;
  private boolean oddsBoost;
  private String fanzoneTeamId;

  @Data
  @NoArgsConstructor
  public static class AdditionalParameters {

    private Long scorecastMarketId;

    @Override
    public String toString() {
      return "AdditionalParameters{" + "scorecastMarketId=" + scorecastMarketId + '}';
    }
  }
}
