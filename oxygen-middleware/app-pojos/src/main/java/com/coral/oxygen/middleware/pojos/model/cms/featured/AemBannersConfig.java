package com.coral.oxygen.middleware.pojos.model.cms.featured;

import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.PageType;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
@AllArgsConstructor
@NoArgsConstructor
@Builder
@EqualsAndHashCode(callSuper = true)
public class AemBannersConfig extends SportPageModuleDataItem {

  @Data
  @Builder
  @AllArgsConstructor
  public static class SportPageId {
    private final String id;
    private final PageType pageType;
    private String type;
    private final Integer moduleDataId;
  }

  private SportPageId sportPageId;
  private String title;
  private Integer maxOffers;
  private Integer timePerSlide;
}
