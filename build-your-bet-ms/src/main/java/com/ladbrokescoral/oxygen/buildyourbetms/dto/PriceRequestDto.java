package com.ladbrokescoral.oxygen.buildyourbetms.dto;

import com.ladbrokescoral.oxygen.byb.banach.dto.external.VirtualSelectionDto;
import java.util.List;
import lombok.*;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PriceRequestDto {
  private Long obEventId;
  @Singular private List<Long> selectionIds;
  @Singular private List<VirtualSelectionDto> playerSelections;
}
