package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.cms.ModuleDataSelection;
import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import lombok.EqualsAndHashCode;
import lombok.Setter;
import lombok.ToString;
import org.apache.commons.lang3.StringUtils;

@Setter
@EqualsAndHashCode(callSuper = true)
@ToString
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "_id")
public class HighlightCarouselModule extends EventsModule {
  private String svgId;
  private Integer limit;
  private Boolean inPlay;
  private Integer typeId;
  // Fanzone BMA-62182 : this property will be hold multiple typeIds
  private List<String> typeIds;
  private List<String> marketIds = new ArrayList<>();
  private List<Long> eventIds = new ArrayList<>();
  private String displayMarketType;
  private Boolean displayOnDesktop;

  public HighlightCarouselModule() {
    this.showExpanded = true;
    ModuleDataSelection dataSelection = new ModuleDataSelection();
    dataSelection.setSelectionId(StringUtils.EMPTY);
    dataSelection.setSelectionType(StringUtils.EMPTY);

    setDataSelection(dataSelection);
  }

  @ChangeDetect
  public String getSvgId() {
    return svgId;
  }

  @ChangeDetect
  public Integer getLimit() {
    return limit;
  }

  @ChangeDetect
  public Boolean getInPlay() {
    return inPlay;
  }

  @ChangeDetect
  public Integer getTypeId() {
    return typeId;
  }
  // This property used to get TypeIds.
  @ChangeDetect
  public List<String> getTypeIds() {
    return typeIds;
  }

  @ChangeDetect
  public List<Long> getEventIds() {
    return eventIds;
  }

  public List<String> getMarketIds() {
    return marketIds;
  }

  @Override
  public ModuleType getModuleType() {
    return ModuleType.HIGHLIGHTS_CAROUSEL;
  }

  @ChangeDetect
  public String getDisplayMarketType() {
    return displayMarketType;
  }

  @ChangeDetect
  public Boolean isDisplayOnDesktop() {
    return displayOnDesktop;
  }

  @Override
  public boolean hasStructureChanges(AbstractFeaturedModule previous) {
    HighlightCarouselModule module = (HighlightCarouselModule) previous;
    return previous == null
        || !Objects.equals(isDisplayOnDesktop(), module.isDisplayOnDesktop())
        || hasAnyModuleChangeDueTo2UpEventsLive(module, this)
        || super.hasStructureChanges(previous);
  }

  /**
   * If there is a change in Display Market Type or When Event goes live, HC replaces the 2Up
   * markets with Primary markets. In this case, FE should receive the fresh content as the 2Up
   * market gets suspended once the Event is Live.
   *
   * @param previous
   * @param current
   * @return true / false
   */
  private boolean hasAnyModuleChangeDueTo2UpEventsLive(
      HighlightCarouselModule previous, HighlightCarouselModule current) {
    return !Objects.equals(previous.getDisplayMarketType(), current.getDisplayMarketType())
        || ("2UpMarket".equals(current.getDisplayMarketType())
            && !current.getMarketIds().equals(previous.getMarketIds()));
  }
}
