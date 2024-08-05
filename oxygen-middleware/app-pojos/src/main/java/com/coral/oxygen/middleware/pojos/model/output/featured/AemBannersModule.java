package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.PageType;
import java.math.BigDecimal;
import java.util.List;
import lombok.Builder;
import lombok.EqualsAndHashCode;
import lombok.Setter;

@Setter
@EqualsAndHashCode(callSuper = true)
public class AemBannersModule extends AbstractFeaturedModule<AemBannersImg> {
  private ModuleType moduleType = ModuleType.AEM_BANNERS;

  @Builder
  public AemBannersModule(
      String id,
      PageType pageType,
      Integer sportId,
      String title,
      BigDecimal displayOrder,
      double sortOrder,
      BigDecimal secondaryDisplayOrder,
      List<String> publishedDevices,
      List<AemBannersImg> data,
      Boolean showExpanded,
      String errorMessage,
      Integer maxOffers,
      Integer timePerSlide) {
    super(
        id,
        pageType,
        sportId,
        title,
        displayOrder,
        sortOrder,
        secondaryDisplayOrder,
        publishedDevices,
        data,
        showExpanded,
        errorMessage,
        false,
        0.0,
        null);
    this.maxOffers = maxOffers;
    this.timePerSlide = timePerSlide;
  }

  public AemBannersModule() {}

  @Override
  public ModuleType getModuleType() {
    return moduleType;
  }

  private Integer maxOffers;
  private Integer timePerSlide;

  @ChangeDetect
  public Integer getMaxOffers() {
    return maxOffers;
  }

  @ChangeDetect
  public Integer getTimePerSlide() {
    return timePerSlide;
  }
}
