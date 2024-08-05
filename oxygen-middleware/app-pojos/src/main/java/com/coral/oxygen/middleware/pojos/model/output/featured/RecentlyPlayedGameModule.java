package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import java.math.BigDecimal;
import java.util.Optional;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
public class RecentlyPlayedGameModule extends AbstractFeaturedModule<RpgConfig> {

  private ModuleType moduleType = ModuleType.RECENTLY_PLAYED_GAMES;

  public RecentlyPlayedGameModule(SportModule cmsModule) {
    super.id = cmsModule.getId();
    super.sportId = cmsModule.getSportId();
    super.title = cmsModule.getTitle();
    setPublishedDevices(cmsModule.getPublishedDevices());
    super.displayOrder =
        BigDecimal.valueOf(Optional.ofNullable(cmsModule.getSortOrder()).orElse(0.0));
    super.showExpanded = true;
    super.pageType = cmsModule.getPageType();
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
