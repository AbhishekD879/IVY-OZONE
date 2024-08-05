package com.coral.oxygen.middleware.pojos.model.cms.featured;

import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class BybWidget extends SportPageModuleDataItem {
  private String id;
  private Integer sportId;
  private String title;
  private List<BybWidgetData> data;
  private int marketCardVisibleSelections;
  private boolean showAll;
}
