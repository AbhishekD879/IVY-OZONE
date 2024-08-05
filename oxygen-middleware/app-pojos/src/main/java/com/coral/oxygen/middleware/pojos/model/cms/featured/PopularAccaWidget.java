package com.coral.oxygen.middleware.pojos.model.cms.featured;

import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class PopularAccaWidget extends SportPageModuleDataItem {
  private Integer sportId;
  private String title;
  private String cardCta;
  private String cardCtaAfterAdd;
  private List<PopularAccaWidgetData> data;
}
