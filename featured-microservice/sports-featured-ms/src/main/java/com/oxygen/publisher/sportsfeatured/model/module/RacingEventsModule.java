package com.oxygen.publisher.sportsfeatured.model.module;

import com.oxygen.publisher.sportsfeatured.model.ModuleType;
import com.oxygen.publisher.sportsfeatured.model.module.data.RacingEventsModuleData;
import com.oxygen.publisher.sportsfeatured.visitor.FeaturedModuleVisitor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
public class RacingEventsModule extends AbstractFeaturedModule<RacingEventsModuleData> {

  private String type = "RacingEventsModule";
  private String racingType;
  private boolean active;

  @Override
  public ModuleType getModuleType() {
    return ModuleType.RACING_EVENTS_MODULE;
  }

  @Override
  public void accept(FeaturedModuleVisitor visitor) {
    visitor.visit(this);
  }
}
