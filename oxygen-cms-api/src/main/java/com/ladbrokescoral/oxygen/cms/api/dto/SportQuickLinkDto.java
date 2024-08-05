package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import com.ladbrokescoral.oxygen.cms.api.mapping.SportQuickLinkMapper;
import java.time.Instant;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
@EqualsAndHashCode(callSuper = false)
public class SportQuickLinkDto extends AbstractSegmentDto
    implements SportPageModuleDataItem, Copyable<SportQuickLinkDto> {

  private String id;
  private String destination;
  private Boolean disabled;
  private Integer sportId;
  private String title;
  private Instant validityPeriodEnd;
  private Instant validityPeriodStart;
  private String svg;
  private String svgId;
  private Integer displayOrder;

  private String pageId;
  private PageType pageType = PageType.sport;

  @Override
  public SportPageId sportPageId() {
    return new SportPageId(getPageId(), getPageType(), SportModuleType.QUICK_LINK);
  }

  @Override
  public SportQuickLinkDto copy(PageType pageType, String marker) {
    SportQuickLinkDto copy = SportQuickLinkMapper.INSTANCE.copy(this);
    copy.setId(marker + copy.id);
    copy.setPageType(pageType);
    return copy;
  }
}
