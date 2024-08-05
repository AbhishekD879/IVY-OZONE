package com.oxygen.publisher.sportsfeatured.model.module;

import com.oxygen.publisher.sportsfeatured.model.ModuleType;
import com.oxygen.publisher.sportsfeatured.model.module.data.VirtualRaceCarouselData;
import com.oxygen.publisher.sportsfeatured.visitor.FeaturedModuleVisitor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
public class VirtualRaceModule extends AbstractFeaturedModule<VirtualRaceCarouselData> {

  private String type = "VirtualRaceModule";
  private boolean active;

  @Override
  public ModuleType getModuleType() {
    return ModuleType.VIRTUAL_RACE_CAROUSEL;
  }

  @Override
  public void accept(FeaturedModuleVisitor visitor) {
    visitor.visit(this);
  }
}
