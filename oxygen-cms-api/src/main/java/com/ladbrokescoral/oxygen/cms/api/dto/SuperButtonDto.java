package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.util.ObjectUtils;

@Data
@AllArgsConstructor
public class SuperButtonDto implements SportPageModuleDataItem {
  private Integer sportId;

  @Override
  public SportPageId sportPageId() {
    String id = ObjectUtils.isEmpty(sportId) ? null : String.valueOf(sportId);
    return new SportPageId(id, PageType.sport, SportModuleType.SUPER_BUTTON);
  }
}
