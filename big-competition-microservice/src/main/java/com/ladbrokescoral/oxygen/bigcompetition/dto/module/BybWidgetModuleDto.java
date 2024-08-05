package com.ladbrokescoral.oxygen.bigcompetition.dto.module;

import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class BybWidgetModuleDto extends CompetitionModuleDto {
  private String title;
  private int marketCardVisibleSelections;
  private boolean showAll;
  private List<BybWidgetData> data;
}
