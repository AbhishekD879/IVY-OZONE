package com.ladbrokescoral.oxygen.betpackmp.redis;

import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;

@Data
@RedisHash(value = "#{@distributedPrefix}_paf_bpmp", timeToLive = 86400)
public class PafBetPack {

  @Id private String id;
}
