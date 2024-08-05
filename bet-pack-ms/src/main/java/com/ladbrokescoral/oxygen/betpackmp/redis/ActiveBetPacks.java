package com.ladbrokescoral.oxygen.betpackmp.redis;

import static com.ladbrokescoral.oxygen.betpackmp.constants.BetPackConstants.ACTIVE_BET_PACK_IDS;

import java.io.Serializable;
import java.util.List;
import lombok.Data;
import lombok.NonNull;
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;

/*
  Storing active bet pack ids
*/
@Data
@RedisHash(value = "#{@distributedPrefix}_bpmp")
public class ActiveBetPacks implements Serializable {

  @Id private String id = ACTIVE_BET_PACK_IDS;

  @NonNull private List<String> activeBetPacksIds;
}
