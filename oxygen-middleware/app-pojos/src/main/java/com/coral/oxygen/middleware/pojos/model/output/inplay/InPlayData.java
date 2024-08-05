package com.coral.oxygen.middleware.pojos.model.output.inplay;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.cms.VirtualSportEvents;
import java.util.List;
import java.util.stream.Stream;
import lombok.Getter;
import lombok.Setter;

public class InPlayData implements IGenerationEntity {

  private InPlayModel livenow;
  private InPlayModel upcoming;
  private InPlayModel liveStream;
  private InPlayModel upcomingLiveStream;

  private SportsRibbon sportsRibbon;
  private List<VirtualSportEvents> virtualSportEvents;

  @Getter @Setter private long generation = -1;
  @Getter @Setter private long creationTime = System.currentTimeMillis();

  public InPlayData() {
    this(new InPlayModel(), new InPlayModel(), new InPlayModel(), new InPlayModel());
  }

  public InPlayData(
      InPlayModel livenow,
      InPlayModel upcoming,
      InPlayModel liveStream,
      InPlayModel upcomingLiveStream) {
    this.livenow = livenow;
    this.upcoming = upcoming;
    this.liveStream = liveStream;
    this.upcomingLiveStream = upcomingLiveStream;
  }

  @ChangeDetect(compareNestedObject = true)
  public InPlayModel getLivenow() {
    return livenow;
  }

  @ChangeDetect(compareNestedObject = true)
  public InPlayModel getUpcoming() {
    return upcoming;
  }

  @ChangeDetect(compareNestedObject = true)
  public InPlayModel getLiveStream() {
    return liveStream;
  }

  @ChangeDetect(compareNestedObject = true)
  public InPlayModel getUpcomingLiveStream() {
    return upcomingLiveStream;
  }

  public void setLiveStream(InPlayModel liveStream) {
    this.liveStream = liveStream;
  }

  public void setUpcomingLiveStream(InPlayModel upcomingLiveStream) {
    this.upcomingLiveStream = upcomingLiveStream;
  }

  public SportsRibbon getSportsRibbon() {
    return sportsRibbon;
  }

  public void setSportsRibbon(SportsRibbon sportsRibbon) {
    this.sportsRibbon = sportsRibbon;
  }

  @Override
  public long generation() {
    return generation;
  }

  @Override
  public long creationTime() {
    return creationTime;
  }

  @ChangeDetect(compareNestedObject = true, compareList = true)
  public List<VirtualSportEvents> getVirtualSportEvents() {
    return virtualSportEvents;
  }

  public void setVirtualSportEvents(List<VirtualSportEvents> virtualSportEvents) {
    this.virtualSportEvents = virtualSportEvents;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("InPlayData{");
    sb.append("generation=").append(generation);
    sb.append(", creationTime=").append(creationTime);
    sb.append(", livenow=").append(livenow);
    sb.append(", upcoming=").append(upcoming);
    sb.append(", liveStream=").append(liveStream);
    sb.append(", upcomingLiveStream=").append(upcomingLiveStream);
    sb.append(", sportsRibbon=").append(sportsRibbon);
    sb.append('}');
    return sb.toString();
  }

  public static Stream<SportSegment> allSportSegmentsStream(InPlayData data) {
    if (data == null) {
      return Stream.empty();
    }
    return Stream.concat(
        Stream.concat(
            data.getLivenow().getSportEvents().stream(),
            data.getUpcoming().getSportEvents().stream()),
        Stream.concat(
            data.getLiveStream().getSportEvents().stream(),
            data.getUpcomingLiveStream().getSportEvents().stream()));
  }
}
