package com.coral.oxygen.middleware.pojos.model.cms.featured;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class TeamAndFanBets extends SportPageModuleDataItem {
  private String id;
  private Integer sportId;
  private String title;

  private Integer noOfMaxSelections;
  private boolean enableBackedTimes;
}
