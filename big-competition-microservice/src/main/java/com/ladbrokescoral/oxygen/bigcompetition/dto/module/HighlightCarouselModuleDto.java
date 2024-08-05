package com.ladbrokescoral.oxygen.bigcompetition.dto.module;

import java.util.ArrayList;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class HighlightCarouselModuleDto extends CompetitionModuleDto {
  private List<String> highlightCarousels = new ArrayList<>();
}
