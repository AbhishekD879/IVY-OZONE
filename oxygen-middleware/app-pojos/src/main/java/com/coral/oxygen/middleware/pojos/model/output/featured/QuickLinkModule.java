package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import java.math.BigDecimal;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "_id")
public class QuickLinkModule extends AbstractFeaturedModule<QuickLinkData> {

  private Map<String, SegmentView> moduleSegmentView = new HashMap<>();

  private Map<String, FanzoneSegmentView> fanzoneModuleSegmentView = new HashMap<>();

  public QuickLinkModule(SportModule cmsModule) {
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
    return ModuleType.QUICK_LINK;
  }

  @Override
  public String toString() {
    return super.toString();
  }

  public QuickLinkModule copyWithEmptySegmentedData(double segmentOrder) {
    QuickLinkModule result = (QuickLinkModule) copyWithEmptyData();
    result.setModuleSegmentView(null);
    result.setSegments(null);
    result.setFanzoneModuleSegmentView(null);
    result.setSegmentOrder(segmentOrder);
    return result;
  }
}
