package com.oxygen.publisher.sportsfeatured.model;

import com.oxygen.publisher.model.PageType;
import java.util.Optional;
import java.util.stream.Stream;
import lombok.*;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.apache.commons.lang3.math.NumberUtils;

@Getter
@EqualsAndHashCode
@AllArgsConstructor
@Slf4j
public class PageRawIndex {

  public static final String GENERATION_ID_KEY_FORMAT = "%s::%s::%d";
  public static final String KEY_FORMAT = "%s::%s";
  public static final String LEGACY_NAME_SPACE = "socket.io";

  public static final PageRawIndex HOME_PAGE = new PageRawIndex(PageType.sport, 0);
  private PageType pageType;
  private Integer sportId;

  public static PageRawIndex fromModel(FeaturedModel model) {
    return fromPageId(model.getPageId());
  }

  public static PageRawIndex fromPageId(String pageId) {
    Optional<PageRawIndex> optional =
        Stream.of(PageType.values())
            .filter(p -> p.getHandler().detect(pageId))
            .map(type -> new PageRawIndex(type, type.getHandler().getSportId(pageId)))
            .findAny();
    if (!optional.isPresent()) {
      throw new IllegalArgumentException("Invalid pageId :" + pageId);
    }
    return optional.get();
  }

  public static PageRawIndex forSport(int sportId) {
    if (sportId == 0) {
      return HOME_PAGE;
    }
    return new PageRawIndex(PageType.sport, sportId);
  }

  public static PageRawIndex from(int sportId, PageType pageType) {
    if (sportId == 0 && PageType.sport.equals(pageType)) {
      return HOME_PAGE;
    }
    return new PageRawIndex(pageType, sportId);
  }

  public static PageRawIndex forHub(String hubId) {
    return new PageRawIndex(PageType.eventhub, PageType.eventhub.getHandler().getSportId(hubId));
  }

  public static PageRawIndex fromGenerationKey(GenerationKey generationKey) {
    return from(
        generationKey.getType().getHandler().getSportId(generationKey.getPageId()),
        generationKey.getType());
  }

  public static PageRawIndex fromGenerationId(String generationId) {
    if (StringUtils.isBlank(generationId)) {
      log.error("Empty generation Id in PageRawIndex::fromGenerationId.");
      return HOME_PAGE;
    }
    String[] keys = generationId.split("::");
    if (keys.length > 1) {
      PageType pageType = PageType.valueOf(keys[0]);
      return from(pageType.getHandler().getSportId(keys[1]), pageType);
    } else {
      log.error(
          "Unknown format for given generationId -> {} in PageRawIndex::fromGenerationId.",
          generationId);
      return HOME_PAGE;
    }
  }

  @Override
  public String toString() {
    return String.format(KEY_FORMAT, pageType.getTypeName(), sportId);
  }

  @Getter
  @AllArgsConstructor
  @NoArgsConstructor
  @Data
  @EqualsAndHashCode
  public static class GenerationKey {

    public static final String KEY_PATTERN = "%s::%s::%d";

    private PageType type;
    private String pageId;
    @EqualsAndHashCode.Exclude private long version;

    @Override
    public String toString() {
      return String.format(
          GenerationKey.KEY_PATTERN, this.type.toString(), this.pageId, this.version);
    }

    public static GenerationKey fromString(String generationId) {
      String[] fields = generationId.split("::");
      return new GenerationKey(PageType.valueOf(fields[0]), fields[1], Long.parseLong(fields[2]));
    }

    public static GenerationKey fromPage(String pageId, long version) {
      PageType type = PageType.sport;
      if (!NumberUtils.isDigits(pageId)) {
        type = PageType.eventhub;
      }
      return new GenerationKey(type, pageId, version);
    }
  }
}
