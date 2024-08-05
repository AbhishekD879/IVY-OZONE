package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.AbstractSegmentEntity;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;
import org.springframework.util.CollectionUtils;
import org.springframework.util.ObjectUtils;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "homemodules")
@Data
@EqualsAndHashCode(callSuper = true)
public class HomeModule extends AbstractSegmentEntity {

  private List<HomeModuleData> data;
  @Valid @NotNull private DataSelection dataSelection;
  @Valid @NotNull private EventsSelectionSetting eventsSelectionSettings;
  private FooterLink footerLink;
  private Integer maxRows;
  private String navItem;
  @NotEmpty private List<String> publishToChannels;
  private Map<String, Device> publishedDevices;
  private Boolean showExpanded;
  @NotBlank private String title;
  private Integer totalEvents;
  @Valid @NotNull private Visibility visibility;
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
  private Double displayOrder;
  // Can be used only when module is single brand
  // To handle uploading on akamain we will use getPublishToChannels method instead of getBrand
  // E.x HomeModuleContentAfterSaveListener.onAfterSave
  @Override
  public String getBrand() {
    if (getBrandsCount() == 1) {
      return getPublishToChannels().get(0);
    }
    return null;
  }

  @JsonIgnore
  public boolean isMultiBranded() {
    return PageType.sport.equals(pageType) && AbstractSportEntity.SPORT_HOME_PAGE.equals(pageId);
  }

  public int getBrandsCount() {
    return ObjectUtils.isEmpty(getPublishToChannels()) ? 0 : getPublishToChannels().size();
  }

  public List<HomeModuleData> getData() {
    if (CollectionUtils.isEmpty(data)) {
      return Collections.emptyList();
    }
    return data;
  }
}
