package com.coral.oxygen.middleware.ms.liveserv.model;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;

@RedisHash(value = "#{@distributedPrefix}", timeToLive = 10800) // 3 hours
@NoArgsConstructor
@Data
@EqualsAndHashCode
public class CachedChannel {

  @Id String channel;

  public CachedChannel(String channel) {
    this.channel = channel;
  }
}
