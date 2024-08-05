package com.coral.oxygen.middleware.pojos.model.cms.featured;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class VirtualEvent extends SportPageModuleDataItem {
  private String id;
  private Integer sportId;

  private Integer limit;

  private String typeIds;
  private String displayMarketType = "PrimaryMarket";

  private String title;
  private boolean disabled;
  private String mobileImageId;
  private String desktopImageId;
  private String sportCategoryId;
  private Integer displayOrder;
  private String buttonText;
  private String redirectionUrl;
}
