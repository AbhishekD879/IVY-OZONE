package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public enum RelationType {
  sport(PageType.sport),
  eventhub(PageType.eventhub),
  edp(PageType.edp);

  private PageType pageType;
}
