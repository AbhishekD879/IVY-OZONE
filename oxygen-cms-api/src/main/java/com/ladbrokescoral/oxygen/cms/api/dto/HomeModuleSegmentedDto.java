package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.ladbrokescoral.oxygen.cms.api.entity.AbstractSportEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.DataSelection;
import com.ladbrokescoral.oxygen.cms.api.entity.Device;
import com.ladbrokescoral.oxygen.cms.api.entity.EventsSelectionSetting;
import com.ladbrokescoral.oxygen.cms.api.entity.FooterLink;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModuleData;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.Visibility;
import java.util.List;
import java.util.Map;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Field;

@Data
@EqualsAndHashCode(callSuper = true)
public class HomeModuleSegmentedDto extends AbstractSegmentDto {

  private List<HomeModuleData> data;
  private DataSelection dataSelection;
  private EventsSelectionSetting eventsSelectionSettings;
  private FooterLink footerLink;
  private Integer maxRows;
  private String navItem;
  private List<String> publishToChannels;
  private Map<String, Device> publishedDevices;
  private Boolean showExpanded;
  private String title;
  private Integer totalEvents;
  private Visibility visibility;
  private Integer maxSelections;

  @Field("__v")
  @JsonProperty("version")
  private Integer ver;

  private String badge;
  private boolean personalised;
  private String pageId = AbstractSportEntity.SPORT_HOME_PAGE;
  private PageType pageType = PageType.sport;
  // used with featured v2 while grouping by sport
  private boolean groupedBySport = true;
  private boolean hero;
  private Double sortOrder;
}
