package com.coral.oxygen.middleware.pojos.model.cms.featured;

import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.PageType;
import java.util.List;
import lombok.Data;

@Data
public class SportPage {
  private final String
      sportId; // don't be longer then 7 symbols. spot -> 0..N ; eventhub -> 'h' + 0..N)
  private final List<SportPageModule> sportPageModules;
  private String pageId = "0";
  private PageType pageType = PageType.sport;
  private boolean featureStructureChanged;
  private boolean segmented = true;
}
