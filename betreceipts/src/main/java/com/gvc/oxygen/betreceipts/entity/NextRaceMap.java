package com.gvc.oxygen.betreceipts.entity;

import java.util.concurrent.TimeUnit;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;
import org.springframework.data.redis.core.TimeToLive;

@RedisHash("events")
@Data
@AllArgsConstructor
public class NextRaceMap {

  @Id private String id;
  private String nextRace;

  @TimeToLive(unit = TimeUnit.DAYS)
  private long ttl;
}
