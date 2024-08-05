package com.ladbrokescoral.oxygen.betpackmp.redis;

import static com.ladbrokescoral.oxygen.betpackmp.util.DateUtils.scrub;

import java.util.ArrayList;
import java.util.Objects;
import java.util.Optional;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

/*
 This class is processing active bet pack ids in redis
*/

@Service
public class BetPackRedisService {

  private final BetPackRepository betPackRepository;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  public BetPackRedisService(BetPackRepository betPackRepository) {
    this.betPackRepository = betPackRepository;
  }

  public ActiveBetPacks save(ActiveBetPacks activeBetPacks) {
    betPackRepository.save(activeBetPacks);
    return activeBetPacks;
  }

  public ActiveBetPacks put(ActiveBetPacks activeBetPacks) {
    if (Objects.nonNull(activeBetPacks)
        && !CollectionUtils.isEmpty(activeBetPacks.getActiveBetPacksIds())) {
      betPackRepository.save(activeBetPacks);
    }
    return activeBetPacks;
  }

  public void evict() {
    betPackRepository.deleteAll();
  }

  public ActiveBetPacks getActiveBetPacks(String id) {
    Optional<ActiveBetPacks> activeBetPacks = betPackRepository.findById(id);
    ASYNC_LOGGER.info("get cached data: {}", scrub(activeBetPacks.toString()));
    return activeBetPacks.orElse(new ActiveBetPacks(new ArrayList<>()));
  }
}
