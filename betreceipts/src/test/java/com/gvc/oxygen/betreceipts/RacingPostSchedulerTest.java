package com.gvc.oxygen.betreceipts;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.gvc.oxygen.betreceipts.config.NextRaceProps;
import com.gvc.oxygen.betreceipts.dto.HorseDTO;
import com.gvc.oxygen.betreceipts.dto.MetaEvent;
import com.gvc.oxygen.betreceipts.dto.RaceDTO;
import com.gvc.oxygen.betreceipts.entity.Bet;
import com.gvc.oxygen.betreceipts.entity.NextRace;
import com.gvc.oxygen.betreceipts.exceptions.JsonSerializeDeserializeException;
import com.gvc.oxygen.betreceipts.mapping.NextRaceMapper;
import com.gvc.oxygen.betreceipts.scheduler.RacingPostScheduler;
import com.gvc.oxygen.betreceipts.service.BetService;
import com.gvc.oxygen.betreceipts.service.EventService;
import com.gvc.oxygen.betreceipts.service.NextEventsService;
import com.gvc.oxygen.betreceipts.service.df.DFService;
import com.ladbrokescoral.lib.masterslave.executor.MasterSlaveExecutor;
import java.io.IOException;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.*;
import org.junit.Assert;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.Spy;
import org.mockito.junit.jupiter.MockitoExtension;
import org.modelmapper.ModelMapper;
import org.modelmapper.convention.MatchingStrategies;
import org.springframework.util.ReflectionUtils;
import reactor.core.publisher.Flux;

@ExtendWith(MockitoExtension.class)
class RacingPostSchedulerTest {

  private ModelMapper modelMapper = getModelMapper();

  @Mock private MasterSlaveExecutor masterSlaveExecutor;

  @Mock private NextRaceProps nextRaceProps;

  @Mock private DFService dfService;

  @Mock private LiveServService liveServService;

  @Spy private NextRaceMapper nextRaceMapper = new NextRaceMapper(modelMapper);

  @Mock private EventService eventService;

  @Mock private NextEventsService nextEventsService;

  @Mock private BetService betService;

  @Mock ObjectMapper objectMapper;

  @InjectMocks private RacingPostScheduler racingPostScheduler;

  @Test
  void evictSiteServCacheTest() {
    Assertions.assertDoesNotThrow(() -> racingPostScheduler.saveSiteservEvents());
  }

  @Test
  void testUpdateUserHistory() {
    Assertions.assertDoesNotThrow(() -> racingPostScheduler.updateUserHistory());
  }

  @Test
  void testDfSaveAllForEmptyClasses() {
    mockNextEvents("chevlton", 10, 2);
    Method method = ReflectionUtils.findMethod(RacingPostScheduler.class, "saveNextRaces");
    method.setAccessible(true);
    Assertions.assertDoesNotThrow(() -> method.invoke(racingPostScheduler));
  }

  @Test
  void testDfSaveAllForEvents() throws IllegalAccessException, IOException {
    mockNextEvents("chevlton", 10, 2);
    mockDataFabric();

    Method method = ReflectionUtils.findMethod(RacingPostScheduler.class, "saveNextRaces");
    Field field = ReflectionUtils.findField(RacingPostScheduler.class, "objectMapper");
    field.setAccessible(true);
    field.set(racingPostScheduler, objectMapper);

    method.setAccessible(true);

    Assertions.assertDoesNotThrow(() -> method.invoke(racingPostScheduler));
  }

  @Test
  void testDfSaveAllForException() throws IllegalAccessException, IOException {
    mockNextEvents("chevlton", 10, 2);
    Mockito.when(dfService.getNextRaces(Mockito.anyInt(), Mockito.anyCollection()))
        .thenThrow(IOException.class);
    Method method = ReflectionUtils.findMethod(RacingPostScheduler.class, "saveNextRaces");
    Field field = ReflectionUtils.findField(RacingPostScheduler.class, "objectMapper");
    field.setAccessible(true);
    field.set(racingPostScheduler, objectMapper);

    method.setAccessible(true);
    Assertions.assertDoesNotThrow(() -> method.invoke(racingPostScheduler));
  }

  @Test
  void testSlaveAction() {
    Method method = ReflectionUtils.findMethod(RacingPostScheduler.class, "slaveAction");
    method.setAccessible(true);

    Assertions.assertDoesNotThrow(() -> method.invoke(racingPostScheduler));
  }

  @Test
  void testDfSaveAllForEmptyEvents() throws IllegalAccessException {
    Mockito.when(nextEventsService.getNextEvents())
        .thenReturn(Flux.fromIterable(Collections.emptyList()));
    Method method = ReflectionUtils.findMethod(RacingPostScheduler.class, "saveNextRaces");
    Field field = ReflectionUtils.findField(RacingPostScheduler.class, "objectMapper");
    field.setAccessible(true);
    field.set(racingPostScheduler, objectMapper);

    method.setAccessible(true);
    Assertions.assertDoesNotThrow(() -> method.invoke(racingPostScheduler));
  }

  @Test
  void testDeleteUserExpiredHistory() {
    Mockito.when(eventService.getMetaEvents()).thenReturn(Flux.fromIterable(getMetaEvents()));
    Mockito.when(betService.findAllBets())
        .thenReturn(Flux.fromIterable(Arrays.asList(createBet("test-gvc"), createBet("jan-gvc"))));
    Method method =
        ReflectionUtils.findMethod(RacingPostScheduler.class, "deleteUserExpiredHistory");
    method.setAccessible(true);
    Assertions.assertDoesNotThrow(() -> method.invoke(racingPostScheduler));
  }

  @Test
  void testEventToNextRaceMap()
      throws JsonProcessingException, NoSuchMethodException, IllegalAccessException {
    NextRace nextRaceMock = Mockito.mock(NextRace.class);
    Mockito.doThrow(new JsonProcessingException("error in processing") {})
        .when(objectMapper)
        .writeValueAsString(nextRaceMock);
    try {
      Method method =
          racingPostScheduler.getClass().getDeclaredMethod("eventToNextRaceMap", NextRace.class);
      method.setAccessible(true);
      method.invoke(racingPostScheduler, nextRaceMock);
    } catch (InvocationTargetException exception) {
      Assert.assertTrue(
          exception.getTargetException() instanceof JsonSerializeDeserializeException);
    }
  }

  private void mockNextEvents(String s, int minutes, int days) {
    ArrayList<Event> value = new ArrayList<>();
    value.add(buildEvent("1", s, getStartDate(minutes + 2, days)));
    value.add(buildEvent("2", s, getStartDate(minutes + 5, days)));
    value.add(buildEvent("3", s, getStartDate(minutes + 10, days)));
    value.add(buildEvent("5", s, getStartDate(minutes + 10, days)));
    value.add(buildEvent("4", s, getStartDate(minutes + 13, days)));
    setOutcome(value.get(1), "horse1", "sSEL898766889");
    setOutcome(value.get(2), "horse2", "hi");
    setOutcome(value.get(4), "horse1", "");
    if (minutes >= 60) value.add(buildEvent("5", s, getStartDate(minutes + 23, days)));
    Mockito.when(nextEventsService.getNextEvents()).thenReturn(Flux.fromIterable(value));
  }

  private List<MetaEvent> getMetaEvents() {
    MetaEvent metaEvent = new MetaEvent();
    metaEvent.setEventId("223344");
    return Arrays.asList(metaEvent);
  }

  private Bet createBet(String username) {
    Bet bet = new Bet();
    bet.setUsername(username);
    bet.setEventIds(new HashSet<>(Arrays.asList("12222,23333,222233")));
    return bet;
  }

  private Event buildEvent(String id, String typeFlagCodes, String startTime) {
    Event event = new Event();
    event.setId(id);
    event.setName("name" + id);
    event.setTypeFlagCodes(typeFlagCodes);
    event.setStartTime(startTime);
    event.setLiveServChannels("sEVent878889898");
    return event;
  }

  private void setOutcome(Event event, String name, String outcome) {
    event.setChildren(Arrays.asList(getChildren(name, outcome)));
  }

  private Children getChildren(String name, String outcome) {
    Children children = new Children();
    children.setMarket(getMarkets(name, outcome));
    children.setOutcome(getOutcome(name, outcome));
    return children;
  }

  private Market getMarkets(String name, String outcome) {
    Market market = new Market();
    market.setChildren(getOutcomes(name, outcome));
    return market;
  }

  private List<Children> getOutcomes(String name, String outcome) {
    Children children = new Children();
    children.setOutcome(getOutcome(name, outcome));
    return Arrays.asList(children);
  }

  private Outcome getOutcome(String name, String channel) {
    Outcome outcome = new Outcome();
    outcome.setName(name);
    outcome.setLiveServChannels(channel);
    return outcome;
  }

  private String getStartDate(int minutes, int days) {
    return Instant.now().plus(days, ChronoUnit.DAYS).plus(minutes, ChronoUnit.MINUTES).toString();
  }

  private void mockDataFabric() throws IOException {
    Map<Long, RaceDTO> races = new HashMap<>();
    races.put(1L, buildRaceEvent(false));
    races.put(2L, buildRaceEvent(true));
    races.put(3L, buildRaceEvent(true));
    races.put(5L, buildRaceEvent(true));
    Mockito.when(dfService.getNextRaces(Mockito.anyInt(), Mockito.anyCollection()))
        .thenReturn(Optional.of(races));
  }

  private RaceDTO buildRaceEvent(boolean setHorses) {
    RaceDTO raceEvent = new RaceDTO();
    raceEvent.setDistance("123");
    if (setHorses) raceEvent.setHorses(Arrays.asList(getHorse(true), getHorse(false)));
    return raceEvent;
  }

  private ModelMapper getModelMapper() {
    ModelMapper modelMapper = new ModelMapper();
    modelMapper.getConfiguration().setMatchingStrategy(MatchingStrategies.STRICT);
    return modelMapper;
  }

  private HorseDTO getHorse(boolean isMostTipped) {
    HorseDTO horse = new HorseDTO();
    horse.setIsMostTipped(isMostTipped);
    horse.setTrainer("K Dalgleish");
    horse.setJockey("B Garritty");
    horse.setHorseName("horse1");
    return horse;
  }
}
