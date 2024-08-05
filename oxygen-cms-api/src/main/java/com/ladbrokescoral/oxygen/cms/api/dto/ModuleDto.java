package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import java.util.ArrayList;
import java.util.List;
import lombok.Builder;
import lombok.Data;

@Data
@Builder(toBuilder = true)
public class ModuleDto extends AbstractSegmentDto {
  @JsonProperty("_id")
  private String id;

  private String title;
  private Double displayOrder;
  private Boolean showExpanded;
  private String navItem;
  private Integer maxRows;
  private Integer maxSelections;
  private Integer totalEvents;
  @Builder.Default private List<String> publishedDevices = new ArrayList<>();
  private @JsonProperty("__v") Integer version;
  private List<ModuleDataDto> data;
  private ModuleDataSelectionDto dataSelection;
  private ModuleFooterLinkDto footerLink;
  private List<String> publishToChannels;
  private String badge;
  private ModuleEventsSelectionSettingsDto eventsSelectionSettings;
  private String category;
  private String pageId;
  @Builder.Default private PageType pageType = PageType.sport;
  private boolean personalised;
  private boolean groupedBySport;
  private boolean hero;
}
