package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import com.coral.oxygen.middleware.pojos.model.output.AbstractModuleData;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public abstract class AbstractRacingEventsModule<D extends AbstractModuleData>
    extends AbstractFeaturedModule<D> {

  private boolean active;

  public AbstractRacingEventsModule(SportModule cmsModule, boolean active) {
    super(cmsModule);
    this.active = active;
  }

  @Override
  public boolean isValid() {
    return true;
  }

  @Override
  public boolean hasStructureChanges(AbstractFeaturedModule previous) {
    return super.hasStructureChanges(previous)
        || this.getClass() != previous.getClass()
        || isActive() != this.getClass().cast(previous).isActive();
  }
}
