package com.ladbrokescoral.oxygen.notification.entities.dto;

import lombok.*;
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;
import org.springframework.data.redis.core.TimeToLive;

@Data
@ToString
@EqualsAndHashCode(exclude = {"id"})
@RequiredArgsConstructor(staticName = "of")
@RedisHash("owners")
public class OwnerDTO {
  @Id private final String id;
  @TimeToLive private Long expiration;
}
