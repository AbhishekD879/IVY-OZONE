package com.oxygen.publisher.model;

import java.util.Optional;
import java.util.stream.Stream;
import lombok.Getter;
import org.apache.commons.lang3.math.NumberUtils;
import org.springframework.util.ObjectUtils;

public enum PageType {
  sport(Constants.EMPTY_PREFIX, new PageTypeHandler.Number()),
  eventhub(Constants.EVENT_HUB_PREFIX, new PageTypeHandler.ByPrefix(Constants.EVENT_HUB_PREFIX)),
  sporteventhub(
      Constants.SPORT_EVENT_HUB_PREFIX,
      new PageTypeHandler.ByPrefix(Constants.SPORT_EVENT_HUB_PREFIX)),
  customized(
      Constants.CUSTOMIZED_PREFIX, new PageTypeHandler.ByPrefix(Constants.CUSTOMIZED_PREFIX));

  @Getter private String prefix;

  @Getter private PageTypeHandler handler;

  private PageType(String prefix, PageTypeHandler detector) {
    this.prefix = prefix;
    this.handler = detector;
  }

  public boolean hasPrefix() {
    return !ObjectUtils.isEmpty(prefix);
  }

  public static Optional<PageType> fromPageId(String pageId) {
    return Stream.of(values()).filter(p -> p.handler.detect(pageId)).findAny();
  }

  public String getTypeName() {
    return this.name().toLowerCase();
  }

  public interface PageTypeHandler {

    boolean detect(String pageId);

    Integer getSportId(String pageId);

    public class Number implements PageTypeHandler {

      @Override
      public boolean detect(String pageId) {
        return NumberUtils.isDigits(pageId);
      }

      @Override
      public Integer getSportId(String pageId) {
        return Integer.valueOf(pageId);
      }
    }

    public class ByPrefix implements PageTypeHandler {
      String prefix;

      private ByPrefix(String prefix) {
        super();
        this.prefix = prefix;
      }

      @Override
      public boolean detect(String pageId) {
        return pageId.startsWith(prefix);
      }

      @Override
      public Integer getSportId(String pageId) {
        return Integer.valueOf(pageId.substring(prefix.length()));
      }
    }
  }
}
