package com.gvc.oxygen.betreceipts.dto;

import java.time.Instant;
import java.util.concurrent.TimeUnit;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;
import org.springframework.data.redis.core.TimeToLive;

@Data
@RedisHash("eventMeta")
public class MetaEvent {

  @Id private String eventId;

  private String typeFlagCodes;

  private Instant startTime;

  private boolean tipAvailable = Boolean.TRUE;

  @TimeToLive(unit = TimeUnit.DAYS)
  private long ttl = 1;
}
