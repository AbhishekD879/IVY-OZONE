package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class SportGroupKey {

  private String pageId;

  private PageType pageType;

  public String getGroupKey() {
    return pageType.getPrefix() + "" + pageId;
  }
}
