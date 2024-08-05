package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.PageType;

public interface Copyable<T extends SportPageModuleDataItem> {

  T copy(PageType pageType, String marker);
}
