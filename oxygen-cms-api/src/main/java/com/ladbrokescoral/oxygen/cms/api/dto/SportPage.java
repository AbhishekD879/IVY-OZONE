package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import java.util.List;
import lombok.Data;

@Data
public class SportPage {
  private final String sportId;
  private final List<SportPageModule> sportPageModules;
  private final PageType pageType;
  private final String pageId;
  private final boolean featureStructureChanged;
  private final boolean segmented;
}
