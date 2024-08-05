package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import java.util.List;
import java.util.Map;
import lombok.Data;

@Data
public class HomeModuleDto extends AbstractHomeModuleSegmentDto {
  String id;
  private DataSelectionDto dataSelection;
  private String title;
  private List<String> publishToChannels;
  private Map<String, DeviceDto> publishedDevices;
  private VisibilityDto visibility;
  private Integer displayOrder;
  private EventsSelectionSettingDto eventsSelectionSettings;
  private Long showEventsForDays;
  private boolean personalised;
  private String pageId;
  private PageType pageType;
  private String message;
}
