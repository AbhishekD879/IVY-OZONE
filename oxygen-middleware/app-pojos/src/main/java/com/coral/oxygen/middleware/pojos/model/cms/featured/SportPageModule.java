package com.coral.oxygen.middleware.pojos.model.cms.featured;

import java.util.List;
import lombok.Data;

@Data
public class SportPageModule {
  private final SportModule sportModule;
  private final List<SportPageModuleDataItem> pageData;
}
