package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import com.coral.oxygen.middleware.pojos.model.output.AbstractModuleData;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.PageType;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
import com.google.gson.annotations.SerializedName;
import java.beans.Transient;
import java.io.Serializable;
import java.math.BigDecimal;
import java.util.*;
import lombok.*;
import org.apache.commons.collections4.CollectionUtils;

@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, property = "@type")
@JsonSubTypes({
  @JsonSubTypes.Type(value = EventsModule.class, name = "EventsModule"),
  @JsonSubTypes.Type(value = QuickLinkModule.class, name = "QuickLinkModule"),
  @JsonSubTypes.Type(value = HighlightCarouselModule.class, name = "HighlightCarouselModule"),
  @JsonSubTypes.Type(value = InplayModule.class, name = "InplayModule"),
  @JsonSubTypes.Type(value = RecentlyPlayedGameModule.class, name = "RecentlyPlayedGameModule"),
  @JsonSubTypes.Type(value = SurfaceBetModule.class, name = "SurfaceBetModule"),
  @JsonSubTypes.Type(value = AemBannersModule.class, name = "AemBannersModule"),
  @JsonSubTypes.Type(value = RacingModule.class, name = "RacingModule"),
  @JsonSubTypes.Type(value = RacingEventsModule.class, name = "RacingEventsModule"),
  @JsonSubTypes.Type(value = VirtualRaceModule.class, name = "VirtualRaceModule"),
  @JsonSubTypes.Type(value = VirtualEventModule.class, name = "VirtualEventModule"),
  @JsonSubTypes.Type(value = PopularBetModule.class, name = "PopularBetModule"),
  @JsonSubTypes.Type(
      value = InternationalToteRaceModule.class,
      name = "InternationalToteRaceModule"),
  @JsonSubTypes.Type(value = TeamBetsModule.class, name = "TeamBetsModule"),
  @JsonSubTypes.Type(value = FanBetsModule.class, name = "FanBetsModule"),
  @JsonSubTypes.Type(value = BybWidgetModule.class, name = "BybWidgetModule"),
  @JsonSubTypes.Type(value = SuperButtonModule.class, name = "SuperButtonModule"),
  @JsonSubTypes.Type(value = LuckyDipModule.class, name = "LuckyDipModule"),
  @JsonSubTypes.Type(value = PopularAccaModule.class, name = "PopularAccaModule")
})
@EqualsAndHashCode
@AllArgsConstructor
@NoArgsConstructor
@Data
public abstract class AbstractFeaturedModule<D extends AbstractModuleData>
    implements Serializable, Cloneable {

  @SerializedName("_id")
  @JsonProperty("_id")
  protected String id;

  protected PageType pageType;
  protected Integer sportId;
  protected String title; // "Test Sports",
  protected BigDecimal displayOrder; // 0,
  protected double sortOrder;

  /**
   * secondaryDisplayOrder is needed to preserve CMS order of Featured/HighlightCarousel modules,
   * where 1 CMS module can be mapped to multiple AbstractFeaturedModule. In that case displayOrder
   * should be equal to CMS module sortOrder and secondaryDisplayOrder should be equal to the
   * display order of CMS module items
   */
  protected BigDecimal secondaryDisplayOrder; // 0,

  private List<String> publishedDevices =
      Collections.emptyList(); // ": ["desktop", "tablet", "mobile"],
  private List<D> data = new ArrayList<>(); // [],
  protected Boolean showExpanded; // false,
  private String errorMessage;
  private boolean segmented;
  private double segmentOrder;
  private List<String> segments;

  protected AbstractFeaturedModule(SportModule cmsModule) {
    this.id = cmsModule.getId();
    this.sportId = cmsModule.getSportId();
    this.title = cmsModule.getTitle();
    this.publishedDevices = cmsModule.getPublishedDevices();
    this.displayOrder =
        BigDecimal.valueOf(Optional.ofNullable(cmsModule.getSortOrder()).orElse(0.0));
    this.showExpanded = true;
    this.pageType = cmsModule.getPageType();
  }

  @Transient
  public boolean hasStaticContent() {
    return getModuleType().isStatic();
  }

  public abstract ModuleType getModuleType();

  @JsonProperty("_id")
  public String getId() {
    return id;
  }

  public void setId(String id) {
    this.id = id;
  }

  @ChangeDetect
  public String getTitle() {
    return title;
  }

  public void setTitle(String title) {
    this.title = title;
  }

  public BigDecimal getDisplayOrder() {
    return displayOrder;
  }

  public void setDisplayOrder(BigDecimal displayOrder) {
    this.displayOrder = displayOrder;
  }

  public BigDecimal getSecondaryDisplayOrder() {
    return secondaryDisplayOrder;
  }

  public void setSecondaryDisplayOrder(BigDecimal secondaryDisplayOrder) {
    this.secondaryDisplayOrder = secondaryDisplayOrder;
  }

  public List<String> getPublishedDevices() {
    return publishedDevices;
  }

  public void setPublishedDevices(List<String> publishedDevices) {
    this.publishedDevices = publishedDevices;
  }

  @ChangeDetect(compareCollection = true)
  public List<D> getData() {
    return data;
  }

  public void setData(List<D> data) {
    this.data = data;
  }

  public Boolean getShowExpanded() {
    return showExpanded;
  }

  public void setShowExpanded(Boolean showExpanded) {
    this.showExpanded = showExpanded;
  }

  public String getErrorMessage() {
    return errorMessage;
  }

  public void setErrorMessage(String errorMessage) {
    this.errorMessage = errorMessage;
  }

  @JsonIgnore
  public Boolean isErrorEmpty() {
    return this.errorMessage == null || errorMessage.isEmpty();
  }

  public Integer getSportId() {
    return sportId;
  }

  public void setSportId(Integer sportId) {
    this.sportId = sportId;
  }

  public PageType getPageType() {
    return pageType;
  }

  public void setPageType(PageType pageType) {
    this.pageType = pageType;
  }

  public double getSortOrder() {
    return sortOrder;
  }

  public void setSortOrder(double sortOrder) {
    this.sortOrder = sortOrder;
  }

  public boolean isSegmented() {
    return segmented;
  }

  public void setSegmented(boolean segmented) {
    this.segmented = segmented;
  }

  @Override
  public String toString() {
    return "AbstractFeaturedModule{"
        + "id='"
        + id
        + '\''
        + ", sportId="
        + sportId
        + ", title='"
        + title
        + '\''
        + ", @type='"
        + this.getModuleType().toString()
        + '\''
        + '}';
  }

  @JsonIgnore
  public boolean isValid() {
    return CollectionUtils.isNotEmpty(getData());
  }

  public boolean hasStructureChanges(AbstractFeaturedModule<D> previous) {
    return previous == null
        || !Objects.equals(getPublishedDevices(), previous.getPublishedDevices())
        || !Objects.equals(getTitle(), previous.getTitle());
  }

  @SneakyThrows
  public final AbstractFeaturedModule<D> copyWithEmptyData() {
    AbstractFeaturedModule<D> result = (AbstractFeaturedModule<D>) this.clone();
    result.setData(new ArrayList<>());

    return result;
  }
}
