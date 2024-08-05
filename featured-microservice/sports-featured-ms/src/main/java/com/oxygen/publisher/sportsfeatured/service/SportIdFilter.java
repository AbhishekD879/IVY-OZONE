package com.oxygen.publisher.sportsfeatured.service;

import com.oxygen.publisher.model.PageType;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class SportIdFilter {
  private List<PageType> supportedTypes;

  public SportIdFilter(@Value("${socket.sport.types:}") List<PageType> supportedPageTypes) {
    super();
    this.supportedTypes = supportedPageTypes;
  }

  public boolean isSupportedPageType(String pageId) {
    Optional<PageType> pageType = PageType.fromPageId(pageId);
    return pageType.isPresent() && supportedTypes.contains(pageType.get());
  }
}
