package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;

@Accessors(chain = true)
@Data
@EqualsAndHashCode(callSuper = false)
public class FanBetsDto extends AbstractSegmentDto implements SportPageModuleDataItem {
  private String id;
  @NotNull private Integer noOfMaxSelections;

  private boolean enableBackedTimes;
  private Integer sportId;

  private String pageId;
  private PageType pageType = PageType.sport;
  private String title;

  @Override
  public SportPageId sportPageId() {
    return new SportPageId(getPageId(), getPageType(), SportModuleType.BETS_BASED_ON_OTHER_FANS);
  }
}
