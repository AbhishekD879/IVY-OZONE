package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "_id")
public class SuperButtonModule extends AbstractFeaturedModule<SuperButtonConfig> {

  private ModuleType moduleType = ModuleType.SUPER_BUTTON;

  public SuperButtonModule(SportModule cmsModule) {
    super(cmsModule);
  }

  @Override
  public ModuleType getModuleType() {
    return moduleType;
  }

  @Override
  public String toString() {
    return super.toString();
  }
}
