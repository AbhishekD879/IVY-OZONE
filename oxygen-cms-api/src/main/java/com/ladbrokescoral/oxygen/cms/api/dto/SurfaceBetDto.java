package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.RelationType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import com.ladbrokescoral.oxygen.cms.api.mapping.SurfaceBetMapper;
import java.math.BigInteger;
import java.time.Instant;
import java.util.Optional;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = false)
public class SurfaceBetDto extends AbstractSegmentDto
    implements SportPageModuleDataItem, Copyable<SurfaceBetDto> {

  private String id;
  private String title;
  private Instant displayFrom;
  private Instant displayTo;
  private String svgId;
  private String svg;
  private String content;
  private Boolean disabled;
  private Boolean edpOn;
  private Boolean highlightsTabOn;
  private RelationDto reference;
  private BigInteger selectionId;
  private SiteServeCompleteEventDto selectionEvent;
  private PriceDto price;
  private Integer displayOrder;
  private String svgBgId;
  private String pageId;
  private PageType pageType = PageType.sport;
  private String svgBgImgPath;
  private String contentHeader;
  private Boolean displayOnDesktop;
  private boolean isReactionsEnabled;

  @JsonProperty("isReactionsEnabled")
  public boolean isReactionsEnabled() {
    return isReactionsEnabled;
  }

  public Boolean getEventIsLive() {
    return Optional.ofNullable(selectionEvent)
        .map(SiteServeCompleteEventDto::getEventIsLive)
        .orElse(null);
  }

  public String getEventStartTime() {
    return Optional.ofNullable(selectionEvent)
        .map(SiteServeCompleteEventDto::getStartTime)
        .orElse(null);
  }

  public String getPageId() {
    return reference.getRefId();
  }

  public PageType getPageType() {
    return Optional.ofNullable(reference.getRelationType())
        .map(RelationType::valueOf)
        .map(RelationType::getPageType)
        .orElse(this.pageType);
  }

  @Override
  public SportPageId sportPageId() {
    return new SportPageId(getPageId(), getPageType(), SportModuleType.SURFACE_BET);
  }

  @Override
  public SurfaceBetDto copy(PageType pageType, String marker) {
    SurfaceBetDto copy = SurfaceBetMapper.getInstance().copy(this);
    copy.setId(marker + copy.id);
    copy.setPageType(pageType);
    return copy;
  }
}
