package com.coral.oxygen.middleware.pojos.model.cms.featured;

import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class HighlightCarousel extends SportPageModuleDataItem {
  private String id;
  private Integer sportId;
  private String title;
  private String svgId;
  private Integer limit;
  private Boolean inPlay = Boolean.TRUE;
  private Integer typeId;
  private List<String> typeIds; // Fanzone BMA-62182
  private List<String> events;
  private Integer displayOrder;
  private String displayMarketType;
  private Boolean displayOnDesktop;
}
