package com.ladbrokescoral.oxygen.buildyourbetms.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;
import lombok.*;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MarketsGroupedDto {
  @JsonProperty("data")
  @Singular
  private List<MarketGroup> groupedMarkets;
}
