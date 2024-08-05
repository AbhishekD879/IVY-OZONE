package com.oxygen.publisher.sportsfeatured.model.module;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
import com.oxygen.publisher.model.IdentityAggregator;
import com.oxygen.publisher.model.PageType;
import com.oxygen.publisher.sportsfeatured.model.Identifier;
import com.oxygen.publisher.sportsfeatured.model.ModuleType;
import com.oxygen.publisher.sportsfeatured.model.module.data.AbstractModuleData;
import com.oxygen.publisher.sportsfeatured.visitor.FeaturedModuleVisitor;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.collections4.CollectionUtils;

@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, property = "@type")
@JsonSubTypes({
  @JsonSubTypes.Type(value = EventsModule.class, name = "EventsModule"),
  @JsonSubTypes.Type(value = QuickLinkModule.class, name = "QuickLinkModule"),
  @JsonSubTypes.Type(value = RecentlyPlayedGameModule.class, name = "RecentlyPlayedGameModule"),
  @JsonSubTypes.Type(value = InplayModule.class, name = "InplayModule"),
  @JsonSubTypes.Type(value = SurfaceBetModule.class, name = "SurfaceBetModule"),
  @JsonSubTypes.Type(value = HighlightCarouselModule.class, name = "HighlightCarouselModule"),
  @JsonSubTypes.Type(value = AemBannersModule.class, name = "AemBannersModule"),
  @JsonSubTypes.Type(value = RacingModule.class, name = "RacingModule"),
  @JsonSubTypes.Type(value = RacingEventsModule.class, name = "RacingEventsModule"),
  @JsonSubTypes.Type(value = VirtualRaceModule.class, name = "VirtualRaceModule"),
  @JsonSubTypes.Type(
      value = InternationalToteRaceModule.class,
      name = "InternationalToteRaceModule"),
  @JsonSubTypes.Type(value = TeamBetsModule.class, name = "TeamBetsModule"),
  @JsonSubTypes.Type(value = FanBetsModule.class, name = "FanBetsModule"),
  @JsonSubTypes.Type(value = VirtualEventModule.class, name = "VirtualEventModule"),
  @JsonSubTypes.Type(value = PopularBetModule.class, name = "PopularBetModule"),
  @JsonSubTypes.Type(value = BybWidgetModule.class, name = "BybWidgetModule"),
  @JsonSubTypes.Type(value = LuckyDipModule.class, name = "LuckyDipModule"),
  @JsonSubTypes.Type(value = SuperButtonModule.class, name = "SuperButtonModule"),
  @JsonSubTypes.Type(value = PopularAccaModule.class, name = "PopularAccaModule")
})
@Data
@EqualsAndHashCode
@JsonIgnoreProperties(ignoreUnknown = true)
@Slf4j
public abstract class AbstractFeaturedModule<D extends AbstractModuleData>
    implements Cloneable, IdentityAggregator {

  private static final Map<ModuleType, Identifier> MODULE_IDENTIFIERS = new ConcurrentHashMap<>();

  @JsonProperty("_id")
  private String id;

  private PageType pageType = PageType.sport;
  private Integer sportId = 0; // by agreement Sports Id is equal 0 for the home landing page
  private String title;
  private BigDecimal displayOrder;
  private Boolean showExpanded;
  private List<String> publishedDevices;
  private List<D> data = new ArrayList<>();
  private String errorMessage;
  private List<String> segments;
  private Map<String, SegmentView> moduleSegmentView;
  private boolean segmented;
  private double segmentOrder;
  // BMA-62182: This property helps to holds list of fanzone Segments.
  private List<String> fanzoneSegments;
  // BMA-62182: This property helps to holds the map of Fanzone segment view.
  private Map<String, FanzoneSegmentView> fanzoneModuleSegmentView;

  /**
   * @return a shallow copy of object with empty data field (empty List)
   */
  @SneakyThrows
  public final AbstractFeaturedModule<?> copyWithEmptyData() {
    AbstractFeaturedModule<?> result = (AbstractFeaturedModule<?>) this.clone();
    result.setData(new ArrayList<>());

    return result;
  }

  public boolean hasData() {
    return CollectionUtils.isNotEmpty(getData());
  }

  public Identifier getIdentifier() {
    return MODULE_IDENTIFIERS.computeIfAbsent(getModuleType(), Identifier::new);
  }

  /**
   * Sets the module type for final JSON Works without @JsonProperty and type field for
   * FEATURED_STRUCTURE_CHANGED but not for MODULE_CONTENT_CHANGED Instead of defining method please
   * add private final String type = "FeaturedModuleName"
   *
   * @return FeaturedModule name
   */
  @JsonProperty("@type")
  protected abstract String getType();

  public abstract ModuleType getModuleType();

  public abstract void accept(FeaturedModuleVisitor visitor);

  public void accept(FeaturedModuleVisitor visitor, String segment) {
    log.debug("segment name:: {}", segment);
    accept(visitor);
  }
}
