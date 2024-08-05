package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "_id")
public class FanBetsModule extends AbstractFeaturedModule<FanBetsConfig> {

  private ModuleType moduleType = ModuleType.BETS_BASED_ON_OTHER_FANS;
  private Map<String, FanzoneSegmentView> fanzoneModuleSegmentView = new HashMap<>();
  private List<String> fanzoneSegments;

  public FanBetsModule(SportModule cmsModule) {
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

  public Map<String, FanzoneSegmentView> getFanzoneModuleSegmentView() {
    return fanzoneModuleSegmentView;
  }
}
