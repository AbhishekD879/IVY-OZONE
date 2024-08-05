package com.ladbrokescoral.oxygen.notification.entities.sportsbook;

import com.google.gson.annotations.SerializedName;
import com.ladbrokescoral.oxygen.notification.entities.Outcome;
import java.util.List;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.ToString;
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;

@EqualsAndHashCode(callSuper = true)
@Data
@ToString
// todo move "timeToLive" to properties
@RedisHash(value = "events", timeToLive = 5400)
@Builder
public class Event extends SportsBookEntity {
  @Id private String id;
  private String name;

  @SerializedName("eventKey")
  private Long eventId;

  private String categoryId;
  private String period;
  private String homeTeamName;
  private String awayTeamName;
  private int homeTeamScore;
  private int awayTeamScore;
  private int homeTeamPenalties;
  private int awayTeamPenalties;
  private boolean isLive;
  private String startTime;
  private String sportUri;
  private List<Outcome> outcomes;
  private boolean isEventStarted;
  private boolean isEventResulted;
  private boolean isGoingDown;
  private boolean isStreamStarted;
}
