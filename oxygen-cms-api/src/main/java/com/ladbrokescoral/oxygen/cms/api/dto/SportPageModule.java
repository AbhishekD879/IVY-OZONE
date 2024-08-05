package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;

@Data
public class SportPageModule {
  private final SportModuleDto sportModule;
  private final List<SportPageModuleDataItem> pageData;
}
