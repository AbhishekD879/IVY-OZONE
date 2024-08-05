package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import lombok.Data;

@Data
public class VirtualNextEventDto implements SportPageModuleDataItem {

  private String id;

  private Integer sportId;

  private String title;

  private int limit;

  private String typeIds;

  private boolean disabled;

  private String classIds;

  private String mobileImageId;

  private String desktopImageId;

  private String buttonText;

  private String redirectionUrl;

  @Override
  public SportPageId sportPageId() {
    return new SportPageId(
        String.valueOf(sportId), PageType.sport, SportModuleType.VIRTUAL_NEXT_EVENTS);
  }
}
