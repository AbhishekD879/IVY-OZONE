package com.oxygen.publisher.sportsfeatured.model.module.data;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
import com.oxygen.publisher.sportsfeatured.model.module.LuckyDipCategoryData;
import com.oxygen.publisher.sportsfeatured.model.module.data.inplay.SportSegment;
import java.util.List;
import lombok.Data;
import lombok.SneakyThrows;

@Data
@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, property = "@type")
@JsonSubTypes({
  @JsonSubTypes.Type(value = EventsModuleData.class, name = "EventsModuleData"),
  @JsonSubTypes.Type(value = QuickLinkData.class, name = "QuickLinkData"),
  @JsonSubTypes.Type(value = SurfaceBetModuleData.class, name = "SurfaceBetModuleData"),
  @JsonSubTypes.Type(value = RpgConfig.class, name = "RpgConfig"),
  @JsonSubTypes.Type(value = SportSegment.class, name = "SportSegment"),
  @JsonSubTypes.Type(value = AemBannersImg.class, name = "AemBannersImg"),
  @JsonSubTypes.Type(value = RacingModuleConfig.class, name = "RacingModuleConfig"),
  @JsonSubTypes.Type(value = RacingEventsModuleData.class, name = "RacingEventsModuleData"),
  @JsonSubTypes.Type(value = VirtualRaceCarouselData.class, name = "VirtualRaceModuleData"),
  @JsonSubTypes.Type(value = InternationalToteRaceData.class, name = "InternationalToteRaceData"),
  @JsonSubTypes.Type(value = TeamBetsConfig.class, name = "TeamBetsConfig"),
  @JsonSubTypes.Type(value = FanBetsConfig.class, name = "FanBetsConfig"),
  @JsonSubTypes.Type(value = PopularBetModuleData.class, name = "PopularBetModuleData"),
  @JsonSubTypes.Type(value = BybWidgetModuleData.class, name = "BybWidgetData"),
  @JsonSubTypes.Type(value = LuckyDipCategoryData.class, name = "LuckyDipData"),
  @JsonSubTypes.Type(value = SuperButtonConfig.class, name = "SuperButtonConfig"),
  @JsonSubTypes.Type(value = PopularAccaModuleData.class, name = "PopularAccaModuleData")
})
@JsonIgnoreProperties(ignoreUnknown = true)
public abstract class AbstractModuleData implements Cloneable {
  private String guid;
  private String id;
  private double segmentOrder;
  private List<String> segments;
  // BMA-62182: This property helps to holds list of fanzone Segments.
  private List<String> fanzoneSegments;

  @SneakyThrows
  public final AbstractModuleData copyWithEmptySegmentedData() {
    AbstractModuleData result = (AbstractModuleData) this.clone();
    result.setSegments(null);
    return result;
  }
}
