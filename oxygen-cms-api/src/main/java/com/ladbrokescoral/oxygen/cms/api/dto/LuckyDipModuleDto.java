package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class LuckyDipModuleDto implements SportPageModuleDataItem {

  private Integer sportId;
  private String title;
  private List<LuckyDipMappingPublicDto> luckyDipMappings;

  @Override
  public SportPageId sportPageId() {
    return new SportPageId(String.valueOf(sportId), PageType.sport, SportModuleType.LUCKY_DIP);
  }
}
