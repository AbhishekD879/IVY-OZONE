package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import com.fasterxml.jackson.annotation.JsonIgnore;
import java.math.BigDecimal;
import java.util.Optional;
import lombok.NoArgsConstructor;

@NoArgsConstructor
public class LuckyDipModule extends AbstractFeaturedModule<LuckyDipCategoryData> {

  public LuckyDipModule(SportModule cmsModule) {
    this.id = cmsModule.getId();
    super.sportId = cmsModule.getSportId();
    super.title = cmsModule.getTitle();
    super.displayOrder =
        BigDecimal.valueOf(Optional.ofNullable(cmsModule.getSortOrder()).orElse(0.0));
    super.showExpanded = true;
    super.pageType = cmsModule.getPageType();
  }

  @JsonIgnore
  @Override
  public ModuleType getModuleType() {
    return ModuleType.LUCKY_DIP;
  }
}
