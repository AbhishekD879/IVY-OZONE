package com.ladbrokescoral.oxygen.buildyourbetms.dto;

import com.ladbrokescoral.oxygen.byb.banach.dto.external.GetMarketResponseDto;
import java.util.List;
import lombok.*;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MarketGroup {
  private String marketGroupName;
  @Singular private List<GetMarketResponseDto> markets;
}
