package com.oxygen.publisher.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import java.util.List;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class InPlayData implements IGenerationEntity {

  private InPlayModel livenow;
  private InPlayModel upcoming;
  private InPlayModel liveStream;
  private InPlayModel upcomingLiveStream;
  private SportsRibbon sportsRibbon;

  private List<VirtualSportEvents> virtualSportList;

  private long generation;
  private long creationTime;

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

  @JsonIgnore
  public InPlayData getShallowCopyWithoutStreamEvents() {
    InPlayData result = new InPlayData(livenow, upcoming, null, null);
    result.setGeneration(generation);
    result.setCreationTime(creationTime);
    // there are only two additional fields (boolean and int) related to liveStream, so no need to
    // clean up them
    result.setSportsRibbon(sportsRibbon);
    return result;
  }

  @Override
  public long generation() {
    return generation;
  }

  @Override
  public long creationTime() {
    return creationTime;
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
}
