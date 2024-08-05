package com.coral.oxygen.middleware.featured.service;

import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPage;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.PageType;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class SportPageFilter {

  private List<PageType> supportedTypes;

  public SportPageFilter(@Value("${featured.sport.types}") List<PageType> supportedPageTypes) {
    super();
    this.supportedTypes = supportedPageTypes;
  }

  public boolean isSupportedPage(SportPage page) {
    Optional<PageType> pageType = PageType.fromPageId(page.getSportId());
    return pageType.isPresent() && supportedTypes.contains(pageType.get());
  }
}
