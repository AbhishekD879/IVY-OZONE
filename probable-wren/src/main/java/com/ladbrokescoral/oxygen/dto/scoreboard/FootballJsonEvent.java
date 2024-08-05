package com.ladbrokescoral.oxygen.dto.scoreboard;

import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;

@Data
@RedisHash(value = "#{@distributedPrefix}")
public class FootballJsonEvent {
  @Id private String obEventId;
  private String data;
}
