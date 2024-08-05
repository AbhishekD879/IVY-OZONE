package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.PopularBetConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import lombok.Data;
import org.springframework.util.ObjectUtils;

@Data
public class PopularBetDto implements SportPageModuleDataItem {
  private PopularBetConfig popularBetConfig;
  private Integer sportId;
  private String id;

  @Override
  public SportPageId sportPageId() {
    String id = ObjectUtils.isEmpty(sportId) ? null : String.valueOf(sportId);
    return new SportPageId(id, PageType.sport, SportModuleType.POPULAR_BETS);
  }
}
