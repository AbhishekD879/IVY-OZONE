package com.ladbrokescoral.oxygen.notification.entities.dto;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.ToString;
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;
import org.springframework.data.redis.core.TimeToLive;
import org.springframework.data.redis.core.index.Indexed;

@Data
@ToString
@EqualsAndHashCode(exclude = {"id", "expiration"})
@RedisHash("channels")
public class ChannelDTO {
  @Id private String id;
  @Indexed private String name;
  private String ownerId;
  @TimeToLive private Long expiration;
}
