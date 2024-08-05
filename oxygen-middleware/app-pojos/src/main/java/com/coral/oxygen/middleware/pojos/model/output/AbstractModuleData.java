package com.coral.oxygen.middleware.pojos.model.output;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.IdHolder;
import com.coral.oxygen.middleware.pojos.model.output.featured.*;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.PageType;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
import java.io.Serializable;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.SneakyThrows;

@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, property = "@type")
@JsonSubTypes({
  @JsonSubTypes.Type(value = SurfaceBetModuleData.class, name = "SurfaceBetModuleData"),
  @JsonSubTypes.Type(value = EventsModuleData.class, name = "EventsModuleData"),
  @JsonSubTypes.Type(value = QuickLinkData.class, name = "QuickLinkData"),
  @JsonSubTypes.Type(value = RpgConfig.class, name = "RpgConfig"),
  @JsonSubTypes.Type(value = SportSegment.class, name = "SportSegment"),
  @JsonSubTypes.Type(value = AemBannersImg.class, name = "AemBannersImg"),
  @JsonSubTypes.Type(value = RacingModuleConfig.class, name = "RacingModuleConfig"),
  @JsonSubTypes.Type(value = RacingEventData.class, name = "RacingEventsModuleData"),
  @JsonSubTypes.Type(value = VirtualRaceModuleData.class, name = "VirtualRaceModuleData"),
  @JsonSubTypes.Type(value = InternationalToteRaceData.class, name = "InternationalToteRaceData"),
  @JsonSubTypes.Type(value = TeamBetsConfig.class, name = "TeamBetsConfig"),
  @JsonSubTypes.Type(value = FanBetsConfig.class, name = "FanBetsConfig"),
  @JsonSubTypes.Type(value = PopularBetModuleData.class, name = "PopularBetModuleData"),
  @JsonSubTypes.Type(value = BybWidgetModuleData.class, name = "BybWidgetData"),
  @JsonSubTypes.Type(value = LuckyDipCategoryData.class, name = "LuckyDipData"),
  @JsonSubTypes.Type(value = SuperButtonConfig.class, name = "SuperButtonConfig"),
  @JsonSubTypes.Type(value = PopularAccaModuleData.class, name = "PopularAccaModuleData")
})
@NoArgsConstructor
@EqualsAndHashCode
@Data
public abstract class AbstractModuleData implements IdHolder, Serializable, Cloneable {

  private String guid;
  protected PageType pageType;

  private double segmentOrder;

  @ChangeDetect
  public List<String> getSegments() {
    return segments;
  }

  private List<String> segments;

  public String getGuid() {
    return guid;
  }

  public void setGuid(String guid) {
    this.guid = guid;
  }

  @Override
  public String idForChangeDetection() {
    return guid;
  }

  protected AbstractModuleData(String guid, PageType pageType) {
    super();
    this.guid = guid;
    this.pageType = pageType;
  }

  @SneakyThrows
  public final AbstractModuleData copyWithEmptySegmentedData() {
    AbstractModuleData result = (AbstractModuleData) this.clone();
    result.setSegments(null);
    return result;
  }
}
