package com.entain.oxygen.betbuilder_middleware.scheduler;

import static org.mockito.Mockito.*;

import com.egalacoral.spark.siteserver.model.Event;
import com.entain.oxygen.betbuilder_middleware.exception.EmptySiteserveDataException;
import com.entain.oxygen.betbuilder_middleware.exception.ZookeeperException;
import com.entain.oxygen.betbuilder_middleware.redis.dto.CombinationCache;
import com.entain.oxygen.betbuilder_middleware.repository.RedissonCombinationRepository;
import com.entain.oxygen.betbuilder_middleware.repository.RedissonEventIdRepository;
import com.entain.oxygen.betbuilder_middleware.service.SiteServeService;
import com.ladbrokescoral.lib.leader.LeaderStatus;
import java.util.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import reactor.core.publisher.Mono;

class EventsSchedulerTest {

  @Mock private SiteServeService siteServeService;

  @Mock private RedissonCombinationRepository redissonCombinationRepository;

  @Mock private RedissonEventIdRepository redissonEventIdRepository;
  @Mock private LeaderStatus leaderStatus;

  @InjectMocks private EventsScheduler eventsScheduler;

  @BeforeEach
  void setUp() {
    MockitoAnnotations.openMocks(this);
  }

  @Test()
  void executeTask_EmptySiteserveData() {
    List<Event> eventList = new ArrayList<>();
    when(leaderStatus.isLeaderNode()).thenReturn(true);

    when(redissonEventIdRepository.readEvents())
        .thenReturn(Mono.just(Collections.singletonMap("14692328", "beId1")));
    when(siteServeService.getFinishedEvents()).thenReturn(Mono.just(eventList));

    try {
      eventsScheduler.executeTask();
    } catch (EmptySiteserveDataException e) {
      throw new EmptySiteserveDataException("Null or empty data received from Siteserve.");
    }
    verify(siteServeService, atLeastOnce()).getFinishedEvents();
  }

  @Test
  void executeTask_SuccessfulExecution() {
    when(leaderStatus.isLeaderNode()).thenReturn(true);
    Map<String, String> redisEventIds = Map.of("14666972", "beId1", "14667004", "beId2");
    when(redissonEventIdRepository.readEvents()).thenReturn(Mono.just(redisEventIds));

    List<Event> events = new ArrayList<>();
    Event event1 = new Event();
    event1.setId("14666972");
    Event event2 = new Event();
    event2.setId("14667004");
    events.add(event1);
    events.add(event2);
    when(siteServeService.getFinishedEvents()).thenReturn(Mono.just(events));

    CombinationCache combination1 = new CombinationCache();
    combination1.setOEId("14666972");
    CombinationCache combination2 = new CombinationCache();
    combination2.setOEId("14667004");

    when(redissonCombinationRepository.getCombinationsByOeId(Mockito.any()))
        .thenReturn(Mono.just(Arrays.asList("abc", "def")));
    doNothing()
        .when(redissonCombinationRepository)
        .deleteCombinations(Mockito.any(), Mockito.any());
    when(redissonEventIdRepository.delete(Mockito.anyString())).thenReturn(Mono.just(true));
    eventsScheduler.executeTask();
    verify(redissonCombinationRepository, atLeastOnce())
        .deleteCombinations(Mockito.any(), Mockito.any());
  }

  @Test()
  void executeTask_ErrorFromSS() {
    when(leaderStatus.isLeaderNode()).thenReturn(true);
    when(redissonEventIdRepository.readEvents())
        .thenReturn(Mono.just(Collections.singletonMap("14692328", "beId1")));
    when(siteServeService.getFinishedEvents())
        .thenReturn(Mono.error(new EmptySiteserveDataException("SS error")));
    eventsScheduler.executeTask();
    verify(siteServeService, atLeastOnce()).getFinishedEvents();
  }

  @Test
  void testSlave() {
    when(leaderStatus.isLeaderNode()).thenReturn(false);
    eventsScheduler.executeTask();
    verify(siteServeService, never()).getFinishedEvents();
  }

  @Test
  void testZookeeperExc() {
    when(leaderStatus.isLeaderNode()).thenThrow(new ZookeeperException("Zookeeper exc"));
    eventsScheduler.executeTask();
    verify(siteServeService, never()).getFinishedEvents();
  }
}
