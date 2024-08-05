package com.coral.oxygen.middleware.pojos.model.output.featured;

import java.util.Optional;
import java.util.stream.Stream;
import lombok.AllArgsConstructor;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.ToString;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.math.NumberUtils;
import org.springframework.util.ObjectUtils;

@Slf4j
public class FeaturedRawIndex {

  private static final String EMPTY_PREFIX = "";

  private static final String EVENT_HUB_PREFIX = "h";

  private static final String SPORT_EVENT_HUB_PREFIX = "s";

  private static final String CUSTOMIZED_PREFIX = "c";

  /** no NPE */
  public enum PageType {
    sport(EMPTY_PREFIX, new PageTypeDetector.Number()),
    eventhub(EVENT_HUB_PREFIX, new PageTypeDetector.ByPrefix(EVENT_HUB_PREFIX)),
    sporteventhub(SPORT_EVENT_HUB_PREFIX, new PageTypeDetector.ByPrefix(SPORT_EVENT_HUB_PREFIX)),
    customized(CUSTOMIZED_PREFIX, new PageTypeDetector.ByPrefix(CUSTOMIZED_PREFIX)),
    unknownPage(null, new PageTypeDetector.NpePrefix());

    private String prefix;
    private PageTypeDetector detector;

    PageType(String prefix, PageTypeDetector detector) {
      this.prefix = prefix;
      this.detector = detector;
    }

    public String getPrefix() {
      return prefix;
    }

    public boolean hasPrefix() {
      return !ObjectUtils.isEmpty(prefix);
    }

    public static Optional<PageType> fromPageId(String pageId) {
      return Stream.of(values()).filter(p -> p.detector.detect(pageId)).findAny();
    }

    public interface PageTypeDetector {

      boolean detect(String pageId);

      class Number implements PageTypeDetector {

        @Override
        public boolean detect(String pageId) {
          return NumberUtils.isDigits(pageId);
        }
      }

      class ByPrefix extends Number {
        String prefix;

        private ByPrefix(String prefix) {
          super();
          this.prefix = prefix;
        }

        @Override
        public boolean detect(String pageId) {
          return pageId.startsWith(prefix) && super.detect(pageId.substring(1));
        }
      }

      class NpePrefix implements PageTypeDetector {

        @Override
        public boolean detect(String pageId) {
          return pageId == null;
        }
      }
    }
  }

  @Getter
  @AllArgsConstructor
  @EqualsAndHashCode
  @ToString
  public static class PageKey {
    protected final PageType type;
    protected final String pageId;
  }

  @Getter
  @EqualsAndHashCode(callSuper = true)
  public static class VersionedPageKey extends PageKey {
    public static final String KEY_PATTERN = "%s::%s::%d";

    private final long version;

    public VersionedPageKey(PageType type, String pageId, long version) {
      super(type, pageId);
      this.version = version;
    }

    @Override
    public String toString() {
      return String.format(
          VersionedPageKey.KEY_PATTERN, this.type.toString(), this.getPageId(), this.version);
    }

    public static VersionedPageKey fromPage(FeaturedModel page, long version) {
      return fromPage(page.getPageId(), version);
    }

    public static VersionedPageKey fromPage(String pageId) {
      return fromPage(pageId, -1);
    }

    public static VersionedPageKey fromPage(final String pageId, final long version) {
      PageType type =
          PageType.fromPageId(pageId)
              .orElseGet(
                  () -> {
                    log.error("Unrecognized page type: PageId {}, version {}", pageId, version);
                    return PageType.sport;
                  });
      return new VersionedPageKey(type, pageId, version);
    }
  }

  @Getter
  @AllArgsConstructor
  @EqualsAndHashCode
  public static class ModuleKey {
    public static final String KEY_PATTERN = "%s::%d";

    private final String moduleId;
    private final long version;

    @Override
    public String toString() {
      return String.format(ModuleKey.KEY_PATTERN, moduleId, version);
    }

    public static ModuleKey fromModule(String moduleId, long version) {
      return new ModuleKey(moduleId, version);
    }

    public static ModuleKey fromModule(AbstractFeaturedModule<?> module, long version) {
      return new ModuleKey(module.getId(), version);
    }
  }
}
