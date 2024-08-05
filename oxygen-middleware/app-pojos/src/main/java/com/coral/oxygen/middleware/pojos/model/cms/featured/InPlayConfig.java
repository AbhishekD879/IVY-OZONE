package com.coral.oxygen.middleware.pojos.model.cms.featured;

import java.util.ArrayList;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class InPlayConfig extends SportPageModuleDataItem {
  private Integer sportId;
  private int maxEventCount;
  private List<InplayDataSportItem> homeInplaySports = new ArrayList<>();
}
