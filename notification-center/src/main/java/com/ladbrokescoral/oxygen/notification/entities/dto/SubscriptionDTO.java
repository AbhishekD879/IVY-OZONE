package com.ladbrokescoral.oxygen.notification.entities.dto;

import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.ToString;
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;
import org.springframework.data.redis.core.TimeToLive;
import org.springframework.data.redis.core.index.Indexed;

@Data
@Builder
@ToString
@EqualsAndHashCode(exclude = {"id", "platform", "ownerId", "startTime"})
@NoArgsConstructor
@AllArgsConstructor
@RedisHash("subscriptions")
public class SubscriptionDTO {
  @Id private String id;
  @Indexed private Long eventId;
  private String token;
  private Platform platform;
  @Indexed private String type;
  private String ownerId;
  private String iGameMediaId;
  private String startTime;
  private Integer appVersionInt;
  @TimeToLive private Long expiration;

  /**
   * List of selection names for the non-runner's which were sent for this subscription in order to
   * avoid duplicate messages
   */
  private List<String> sentNonRunners;
}
