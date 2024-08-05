package com.ladbrokescoral.oxygen.betpackmp.redis;

import static com.ladbrokescoral.oxygen.betpackmp.constants.BetPackConstants.ACTIVE_BET_PACK_IDS;
import static org.mockito.Mockito.*;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Optional;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class BetPackRedisServiceTest implements WithAssertions {

  private final String betPackId = ACTIVE_BET_PACK_IDS;

  @Mock private BetPackRepository repository;

  @InjectMocks private BetPackRedisService service;

  @Test
  void putWithEmptyBetPackIdsTest() {
    ActiveBetPacks activeBetPacks = new ActiveBetPacks(new ArrayList<>());
    ActiveBetPacks betPacks = service.put(activeBetPacks);
    Assertions.assertEquals(0, betPacks.getActiveBetPacksIds().size());
  }

  @Test
  void putWithValidBetPackIdsTest() {
    ActiveBetPacks activeBetPacks = new ActiveBetPacks(Arrays.asList("778", "434", "5454"));
    ActiveBetPacks betPacks = service.put(activeBetPacks);
    Assertions.assertEquals(3, betPacks.getActiveBetPacksIds().size());
  }

  @Test
  void putWithNullBetPackTest() {
    Assertions.assertNull(service.put(null));
  }

  @Test
  void saveTest() {
    ActiveBetPacks activeBetPacks = new ActiveBetPacks(new ArrayList<>());
    ActiveBetPacks betPacks = service.save(activeBetPacks);
    Assertions.assertNotNull(betPacks);
  }

  @Test
  void evictTest() {
    service.evict();
    verify(repository, times(1)).deleteAll();
  }

  @Test
  void getActiveBetPacksSuccess() {
    when(repository.findById(betPackId))
        .thenReturn(Optional.of(new ActiveBetPacks(Arrays.asList("56", "989"))));
    ActiveBetPacks activeBetPacks = service.getActiveBetPacks(betPackId);
    Assertions.assertNotNull(activeBetPacks);
  }

  @Test
  void getActiveBetPacksFailure() {
    ActiveBetPacks betPacks = new ActiveBetPacks(new ArrayList<>());
    when(repository.findById(betPackId)).thenReturn(Optional.empty());
    ActiveBetPacks activeBetPacks = service.getActiveBetPacks(betPackId);
    Assertions.assertEquals(betPacks.getId(), activeBetPacks.getId());
    Assertions.assertEquals(betPacks.getActiveBetPacksIds(), activeBetPacks.getActiveBetPacksIds());
  }
}
