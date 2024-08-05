package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import com.ladbrokescoral.oxygen.cms.api.mapping.HighlightCarouselMapper;
import java.time.Instant;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = false)
public class HighlightCarouselDto extends AbstractSegmentDto
    implements SportPageModuleDataItem, Copyable<HighlightCarouselDto> {

  private Integer sportId;
  private String title;
  private Instant displayFrom;
  private Instant displayTo;
  private String svg;
  private String svgId;
  private Integer limit;
  private Boolean inPlay;
  private Integer typeId;
  private List<String> typeIds;
  private List<String> events;
  private String id;
  private Integer displayOrder;
  private Boolean displayOnDesktop;
  private String displayMarketType;

  private String pageId;
  private PageType pageType = PageType.sport;

  @Override
  public SportPageId sportPageId() {
    return new SportPageId(getPageId(), getPageType(), SportModuleType.HIGHLIGHTS_CAROUSEL);
  }

  @Override
  public HighlightCarouselDto copy(PageType pageType, String marker) {
    HighlightCarouselDto copy = HighlightCarouselMapper.getInstance().copy(this);
    copy.setId(marker + copy.id);
    copy.setPageType(pageType);
    return copy;
  }
}
