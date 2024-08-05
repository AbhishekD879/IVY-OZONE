package com.oxygen.publisher.sportsfeatured.model.module;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.oxygen.publisher.sportsfeatured.model.ModuleType;
import com.oxygen.publisher.sportsfeatured.model.module.data.AemBannersImg;
import com.oxygen.publisher.sportsfeatured.visitor.FeaturedModuleVisitor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public class AemBannersModule extends AbstractFeaturedModule<AemBannersImg> {

  private Integer maxOffers;
  private Integer timePerSlide;

  @Override
  @JsonProperty("@type")
  protected String getType() {
    return ModuleType.AEM_BANNERS.name();
  }

  @Override
  public ModuleType getModuleType() {
    return ModuleType.AEM_BANNERS;
  }

  @Override
  public void accept(FeaturedModuleVisitor visitor) {
    visitor.visit(this);
  }
}
