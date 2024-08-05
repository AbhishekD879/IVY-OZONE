package com.ladbrokescoral.oxygen.trendingbets.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import java.util.List;
import java.util.stream.Stream;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class TrendingEvent {

  private String id;
  private String name;
  private String categoryId;
  private String categoryCode;
  private String categoryName;
  private String className;
  private String typeId;
  private String typeName;
  private Boolean eventIsLive;
  private Boolean displayed;
  private String eventStatusCode;
  private Boolean isActive;
  private Boolean isDisplayed;
  private String drilldownTagNames;
  private String liveServChannels;
  private String liveServChildrenChannels;
  private String startTime;
  private List<OutputMarket> markets;

  @EqualsAndHashCode.Include private String selectionId;
  private Boolean isSuspended;
  private boolean hideEventName;

  @JsonIgnore
  public Stream<String> getStreamChannels() {
    OutputMarket outputMarket = markets.get(0);
    return Stream.of(
        liveServChannels,
        outputMarket.getLiveServChannels(),
        outputMarket.getOutcomes().get(0).getLiveServChannels());
  }
}
