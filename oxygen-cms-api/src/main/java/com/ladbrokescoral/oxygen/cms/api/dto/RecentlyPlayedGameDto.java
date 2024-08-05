package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.RpgConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import lombok.Data;
import lombok.experimental.Accessors;
import org.springframework.util.ObjectUtils;

@Accessors(chain = true)
@Data
public class RecentlyPlayedGameDto implements SportPageModuleDataItem {
  private RpgConfig rpgConfig;
  private Integer sportId;

  @Override
  public SportPageId sportPageId() {
    String id = ObjectUtils.isEmpty(sportId) ? null : String.valueOf(sportId);
    return new SportPageId(id, PageType.sport, SportModuleType.RECENTLY_PLAYED_GAMES);
  }
}
