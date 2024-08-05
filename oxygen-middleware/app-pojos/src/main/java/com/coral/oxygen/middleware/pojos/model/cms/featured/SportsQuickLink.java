package com.coral.oxygen.middleware.pojos.model.cms.featured;

import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.PageType;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public class SportsQuickLink extends SportPageModuleDataItem {
  private String id;
  private String destination;
  private String title;
  private Integer displayOrder;
  private String svgId;
  private Integer sportId;

  @Builder
  public SportsQuickLink(
      String type,
      PageType pageType,
      String id,
      String destination,
      String title,
      Integer displayOrder,
      String svgId,
      Integer sportId) {
    super(type, pageType);
    this.id = id;
    this.destination = destination;
    this.title = title;
    this.displayOrder = displayOrder;
    this.svgId = svgId;
    this.sportId = sportId;
  }
}
