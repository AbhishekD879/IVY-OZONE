package com.oxygen.publisher.sportsfeatured.model.module;

import com.oxygen.publisher.sportsfeatured.model.ModuleType;
import com.oxygen.publisher.sportsfeatured.model.module.data.InternationalToteRaceData;
import com.oxygen.publisher.sportsfeatured.visitor.FeaturedModuleVisitor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
public class InternationalToteRaceModule extends AbstractFeaturedModule<InternationalToteRaceData> {

  private String type = "InternationalToteRaceModule";
  private boolean active;

  @Override
  public ModuleType getModuleType() {
    return ModuleType.INTERNATIONAL_TOTE_RACING;
  }

  @Override
  public void accept(FeaturedModuleVisitor visitor) {
    visitor.visit(this);
  }
}
