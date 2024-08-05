package com.ladbrokescoral.oxygen.notification.entities.dto;

import java.io.Serializable;
import java.util.List;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.ToString;
import org.springframework.data.redis.core.RedisHash;

@Data
@ToString
@Builder
@EqualsAndHashCode(of = {"eventId", "token", "platform"})
@RedisHash("racing_subscriptions")
public class RacingDTO implements Serializable {
  private Long eventId;
  private String token;
  private String platform;
  private List<String> types;
}
