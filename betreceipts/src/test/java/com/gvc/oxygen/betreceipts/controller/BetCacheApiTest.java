package com.gvc.oxygen.betreceipts.controller;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.coral.bpp.api.model.bet.api.response.UserDataResponse;
import com.coral.bpp.api.service.BppApiAsync;
import com.egalacoral.spark.siteserver.api.ExistsFilter;
import com.egalacoral.spark.siteserver.api.LimitToFilter;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Category;
import com.egalacoral.spark.siteserver.model.Event;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.gson.Gson;
import com.gvc.oxygen.betreceipts.config.NextRacesConfig;
import com.gvc.oxygen.betreceipts.dto.BetDTO;
import com.gvc.oxygen.betreceipts.dto.HorseDTO;
import com.gvc.oxygen.betreceipts.dto.MetaEvent;
import com.gvc.oxygen.betreceipts.dto.RaceDTO;
import com.gvc.oxygen.betreceipts.dto.TipDTO;
import com.gvc.oxygen.betreceipts.entity.Bet;
import com.gvc.oxygen.betreceipts.entity.NextRace;
import com.gvc.oxygen.betreceipts.entity.NextRaceMap;
import com.gvc.oxygen.betreceipts.mapping.BetMapper;
import com.gvc.oxygen.betreceipts.mapping.NextRaceMapper;
import com.gvc.oxygen.betreceipts.repository.BetRepository;
import com.gvc.oxygen.betreceipts.repository.EventRepository;
import com.gvc.oxygen.betreceipts.repository.MetaEventRepository;
import com.gvc.oxygen.betreceipts.service.BetService;
import com.gvc.oxygen.betreceipts.service.EventService;
import com.gvc.oxygen.betreceipts.service.NextRacesPublicService;
import com.gvc.oxygen.betreceipts.service.siteserve.SiteServeService;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.TreeSet;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import reactor.core.publisher.Mono;

@WebMvcTest(
    value = {
      BetCacheApi.class,
      BetMapper.class,
      BetService.class,
      NextRacesPublicService.class,
      EventService.class,
      NextRaceMapper.class,
      SiteServeService.class
    })
@Import(NextRacesConfig.class)
public class BetCacheApiTest extends AbstractControllerTest {

  @Autowired private ObjectMapper mapper;
  @MockBean private BetRepository repository;
  @MockBean private BppApiAsync bppApiAsync;
  @MockBean private SiteServerApi siteServerApi;
  @MockBean private EventRepository eventRepository;
  @MockBean private MetaEventRepository metaEventRepository;

  @BeforeEach
  public void init() {
    UserDataResponse userDataResponse = new UserDataResponse();
    userDataResponse.setSportBookUserName("");
    when(repository.saveAll(anyList())).thenReturn(Arrays.asList(getBet("user1"), getBet("user2")));
    when(siteServerApi.getClasses(Mockito.any(SimpleFilter.class), Mockito.any(ExistsFilter.class)))
        .thenReturn(Optional.empty());
    when(bppApiAsync.getUserData(anyString())).thenReturn(Mono.just(userDataResponse));
  }

  @Test
  void testSaveBetDTOSWithMetEvents() throws Exception {
    when(metaEventRepository.findAll()).thenReturn(getUKAndInternationalRaces());
    when(eventRepository.findAllById(anyList())).thenReturn(getNextRaceMap());
    List<BetDTO> betDTOS = getBetDtos();
    TipDTO tipDTO = new TipDTO();
    tipDTO.setBets(betDTOS);
    tipDTO.setTipEnabled(true);
    mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bets")
                .contentType(MediaType.APPLICATION_JSON)
                .header("token", "$uch$ecretVerySafe")
                .content(mapper.writeValueAsString(tipDTO)))
        .andExpect(status().is2xxSuccessful());
    // .andExpect(MockMvcResultMatchers.jsonPath("$.isNextRace",Matchers.is(false)));

  }

  @Test
  void testSaveBetDTOSWithMetEventsForAll15Min() throws Exception {
    when(metaEventRepository.findAll()).thenReturn(getUKAndInternationalRacesWithIn15Min());
    when(eventRepository.findAllById(anyList())).thenReturn(getNextRaceMap());
    List<BetDTO> betDTOS = getBetDtos();
    TipDTO tipDTO = new TipDTO();
    tipDTO.setBets(betDTOS);
    tipDTO.setTipEnabled(true);
    mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bets")
                .contentType(MediaType.APPLICATION_JSON)
                .header("token", "$uch$ecretVerySafe")
                .content(mapper.writeValueAsString(tipDTO)))
        .andExpect(status().is2xxSuccessful());
    // .andExpect(MockMvcResultMatchers.jsonPath("$.isNextRace",Matchers.is(false)));

  }

  @Test
  void testSaveBetDTOSWithMetEventsForInternationalRaces() throws Exception {
    when(metaEventRepository.findAll()).thenReturn(getInternationalRaces());
    when(eventRepository.findAllById(anyList())).thenReturn(getNextRaceMap());
    List<BetDTO> betDTOS = getBetDtos();
    TipDTO tipDTO = new TipDTO();
    tipDTO.setBets(betDTOS);
    tipDTO.setTipEnabled(true);
    mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bets")
                .contentType(MediaType.APPLICATION_JSON)
                .header("token", "$uch$ecretVerySafe")
                .content(mapper.writeValueAsString(tipDTO)))
        .andExpect(status().is2xxSuccessful());
    // .andExpect(MockMvcResultMatchers.jsonPath("$.isNextRace",Matchers.is(false)));

  }

  @Test
  void testSaveBetsForException() throws Exception {
    when(metaEventRepository.findAll()).thenReturn(getInternationalRaces());
    when(metaEventRepository.findAll()).thenThrow(new RuntimeException());
    List<BetDTO> betDTOS = getBetDtos();
    TipDTO tipDTO = new TipDTO();
    tipDTO.setBets(betDTOS);
    tipDTO.setTipEnabled(true);
    mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bets")
                .contentType(MediaType.APPLICATION_JSON)
                .header("token", "$uch$ecretVerySafe")
                .content(mapper.writeValueAsString(tipDTO)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void testSaveBetsForExceptionAtEvent() throws Exception {
    when(eventRepository.findAllById(anyList())).thenThrow(new RuntimeException());
    List<BetDTO> betDTOS = getBetDtos();
    TipDTO tipDTO = new TipDTO();
    tipDTO.setBets(betDTOS);
    tipDTO.setTipEnabled(true);
    mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bets")
                .contentType(MediaType.APPLICATION_JSON)
                .header("token", "$uch$ecretVerySafe")
                .content(mapper.writeValueAsString(tipDTO)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void testSaveBetDTOSWithNoFutureMetEvents() throws Exception {
    when(metaEventRepository.findAll()).thenReturn(getUKAndInternationalRaces());
    when(eventRepository.findAllById(anyList())).thenReturn(getNextRaceMap());
    List<BetDTO> betDTOS = getBetDtos();
    TipDTO tipDTO = new TipDTO();
    tipDTO.setBets(betDTOS);
    tipDTO.setTipEnabled(true);
    mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bets")
                .contentType(MediaType.APPLICATION_JSON)
                .header("token", "$uch$ecretVerySafe")
                .content(mapper.writeValueAsString(tipDTO)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void testSaveBetDTOSWithMetEventsTipEnabledFalse() throws Exception {
    when(metaEventRepository.findAll()).thenReturn(getUKAndInternationalRaces());
    when(eventRepository.findAllById(anyList())).thenReturn(getNextRaceMap());
    List<BetDTO> betDTOS = getBetDtos();
    TipDTO tipDTO = new TipDTO();
    tipDTO.setBets(betDTOS);
    tipDTO.setTipEnabled(true);
    mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bets")
                .contentType(MediaType.APPLICATION_JSON)
                .header("token", "$uch$ecretVerySafe")
                .content(mapper.writeValueAsString(tipDTO)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void testSaveBetDTOS() throws Exception {
    List<BetDTO> betDTOS = getBetDtos();
    TipDTO tipDTO = new TipDTO();
    tipDTO.setBets(betDTOS);
    tipDTO.setTipEnabled(true);
    mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bets")
                .contentType(MediaType.APPLICATION_JSON)
                .header("token", "$uch$ecretVerySafe")
                .content(mapper.writeValueAsString(tipDTO)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void testSaveBetDTOSWithException() throws Exception {
    when(metaEventRepository.findAll()).thenThrow(new RuntimeException());
    List<BetDTO> betDTOS = getBetDtos();
    TipDTO tipDTO = new TipDTO();
    tipDTO.setBets(betDTOS);
    tipDTO.setTipEnabled(true);
    mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bets")
                .contentType(MediaType.APPLICATION_JSON)
                .header("token", "$uch$ecretVerySafe")
                .content(mapper.writeValueAsString(tipDTO)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void testSaveBetDTOSForException() throws Exception {
    List<BetDTO> betDTOS = getBetDtos();
    TipDTO tipDTO = new TipDTO();
    tipDTO.setBets(betDTOS);
    tipDTO.setTipEnabled(true);
    Mockito.when(repository.saveAll(anyList())).thenThrow(new RuntimeException());
    mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bets")
                .contentType(MediaType.APPLICATION_JSON)
                .header("token", "$uch$ecretVerySafe")
                .content(mapper.writeValueAsString(tipDTO)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void testSaveBetDTOSForControllerException() throws Exception {
    when(metaEventRepository.findAll()).thenReturn(getUKAndInternationalRaces());
    when(eventRepository.findAllById(anyList())).thenReturn(getNextRaceMap());
    List<BetDTO> betDTOS = getBetDtos();
    TipDTO tipDTO = new TipDTO();
    tipDTO.setBets(null);
    tipDTO.setTipEnabled(true);
    // Mockito.when(betService.saveBets(anyList(),any())).thenThrow(new RuntimeException());
    mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bets")
                .contentType(MediaType.APPLICATION_JSON)
                .header("token", "$uch$ecretVerySafe")
                .content(mapper.writeValueAsString(tipDTO)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void testSaveBetForDfEmpty() throws Exception {
    mockSiteServer("UK,IE", 3, 0);
    List<BetDTO> betDTOS = getBetDtos();
    TipDTO tipDTO = new TipDTO();
    tipDTO.setBets(betDTOS);
    tipDTO.setTipEnabled(true);
    mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bets")
                .contentType(MediaType.APPLICATION_JSON)
                .header("token", "$uch$ecretVerySafe")
                .content(mapper.writeValueAsString(tipDTO)))
        .andExpect(status().is2xxSuccessful());
    // .andExpect(MockMvcResultMatchers.jsonPath("$.races", Matchers.hasSize(3)));
  }

  @Test
  void testSaveBetForTimeLimitWithDfEmpty() throws Exception {
    mockSiteServer("UK,IE", 0, 0);
    List<BetDTO> betDTOS = getBetDtos();
    TipDTO tipDTO = new TipDTO();
    tipDTO.setBets(betDTOS);
    tipDTO.setTipEnabled(true);
    mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bets")
                .contentType(MediaType.APPLICATION_JSON)
                .header("token", "$uch$ecretVerySafe")
                .content(mapper.writeValueAsString(tipDTO)))
        .andExpect(status().is2xxSuccessful());
    // .andExpect(MockMvcResultMatchers.jsonPath("$.races", Matchers.hasSize(3)));
  }

  @Test
  void testSaveBetWithDf() throws Exception {
    mockSiteServer("UK,IE", 3, 0);
    List<BetDTO> betDTOS = getBetDtos();
    TipDTO tipDTO = new TipDTO();
    tipDTO.setBets(betDTOS);
    tipDTO.setTipEnabled(true);
    mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bets")
                .contentType(MediaType.APPLICATION_JSON)
                .header("token", "$uch$ecretVerySafe")
                .content(mapper.writeValueAsString(tipDTO)))
        .andExpect(status().is2xxSuccessful());
    // .andExpect(MockMvcResultMatchers.jsonPath("$.races", Matchers.hasSize(3)));
  }

  @Test
  void testSaveBetWithDfWithTipDisabled() throws Exception {
    mockSiteServer("UK,IE", 3, 0);
    List<BetDTO> betDTOS = getBetDtos();
    TipDTO tipDTO = new TipDTO();
    tipDTO.setBets(betDTOS);
    tipDTO.setTipEnabled(false);
    mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bets")
                .contentType(MediaType.APPLICATION_JSON)
                .header("token", "$uch$ecretVerySafe")
                .content(mapper.writeValueAsString(tipDTO)))
        .andExpect(status().is2xxSuccessful());
    // .andExpect(MockMvcResultMatchers.jsonPath("$.races", Matchers.hasSize(3)));
  }

  @Test
  void testSaveBetWithDfwithException() throws Exception {
    mockSiteServer("UK,IE", 3, 0);
    List<BetDTO> betDTOS = getBetDtos();
    TipDTO tipDTO = new TipDTO();
    tipDTO.setBets(betDTOS);
    tipDTO.setTipEnabled(true);
    mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bets")
                .contentType(MediaType.APPLICATION_JSON)
                .header("token", "$uch$ecretVerySafe")
                .content(mapper.writeValueAsString(tipDTO)))
        .andExpect(status().is2xxSuccessful());
    // .andExpect(MockMvcResultMatchers.jsonPath("$.races", Matchers.hasSize(3)));
  }

  @Test
  void testSaveBetWithDfWithBetHistory() throws Exception {
    mockSiteServer("UK,IE", 3, 0);
    when(repository.findById(anyString())).thenReturn(Optional.of(getFullBetHistory()));
    List<BetDTO> betDTOS = getBetDtos();
    TipDTO tipDTO = new TipDTO();
    tipDTO.setBets(betDTOS);
    tipDTO.setTipEnabled(true);
    mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bets")
                .contentType(MediaType.APPLICATION_JSON)
                .header("token", "$uch$ecretVerySafe")
                .content(mapper.writeValueAsString(tipDTO)))
        .andExpect(status().is2xxSuccessful());
    // .andExpect(MockMvcResultMatchers.jsonPath("$.races", Matchers.hasSize(3)));
  }

  private BetDTO getBetDTO(String user) {
    BetDTO betDTO = new BetDTO();
    betDTO.setUsername(user);
    betDTO.setEventId("17162092");
    betDTO.setStartTime(Instant.now());
    return betDTO;
  }

  private Bet getBet(String user) {
    Bet bet = new Bet();
    bet.setUsername(user);
    bet.setEventIds(new TreeSet<>(Arrays.asList("1")));
    // bet.setStartTime(Instant.now());
    return bet;
  }

  private List<BetDTO> getBetDtos() {
    return Arrays.asList(getBetDTO("user1"), getBetDTO("user2"));
  }

  private Event buildEvent(String id, String typeFlagCodes, String startTime) {
    Event event = new Event();
    event.setId(id);
    event.setName("name" + id);
    event.setTypeFlagCodes(typeFlagCodes);
    event.setStartTime(startTime);
    return event;
  }

  private String getStartDate(int minutes, int days) {
    return Instant.now().plus(days, ChronoUnit.DAYS).plus(minutes, ChronoUnit.MINUTES).toString();
  }

  private void mockSiteServer(String s, int minutes, int days) {
    ArrayList<Event> value = new ArrayList<>();
    value.add(buildEvent("1", s, getStartDate(minutes + 2, days)));
    value.add(buildEvent("2", s, getStartDate(minutes + 5, days)));
    value.add(buildEvent("3", s, getStartDate(minutes + 10, days)));
    value.add(buildEvent("4", s, getStartDate(minutes + 13, days)));
    if (minutes >= 60) value.add(buildEvent("5", s, getStartDate(minutes + 23, days)));
    when(siteServerApi.getClasses(Mockito.any(SimpleFilter.class), Mockito.any(ExistsFilter.class)))
        .thenReturn(Optional.of(Arrays.asList(getCategory(221), getCategory(222))));
    when(siteServerApi.getEventToOutcomeForClass(
            anyList(), any(SimpleFilter.class), any(LimitToFilter.class), any(ExistsFilter.class)))
        .thenReturn(Optional.of(value));
  }

  private Category getCategory(int categoryId) {
    Category category = new Category();
    category.setCategoryId(categoryId);
    return category;
  }

  private RaceDTO buildRaceEvent(String id) {
    RaceDTO raceDTO = new RaceDTO();
    raceDTO.setId(id);
    raceDTO.setDistance("123");
    raceDTO.setHorses(Arrays.asList(getHorse(true), getHorse(false)));
    return raceDTO;
  }

  private HorseDTO getHorse(boolean isMostTipped) {
    HorseDTO horse = new HorseDTO();
    horse.setIsMostTipped(isMostTipped);
    horse.setTrainer("K Dalgleish");
    horse.setJockey("B Garritty");
    return horse;
  }

  private RaceDTO buildRaceEventWithOutHorses(String id) {
    RaceDTO raceDTO = new RaceDTO();
    raceDTO.setDistance("123");
    raceDTO.setId(id);
    return raceDTO;
  }

  private List<Bet> getBetHistory() {
    return Arrays.asList(getBet("1"), getBet("2"));
  }

  private Bet getFullBetHistory() {
    return getBet("1");
  }

  private List<MetaEvent> getUKAndInternationalRaces() {
    List<MetaEvent> eventList = new ArrayList<>();

    eventList.add(getMetaEvent(true, 5, "UK,IE"));
    eventList.add(getMetaEvent(false, 2, "INT"));
    eventList.add(getMetaEvent(true, 1, "UK"));
    eventList.add(getMetaEvent(true, 17, "UK"));
    eventList.add(getMetaEvent(true, 19, "INT"));
    return eventList;
  }

  private List<MetaEvent> getUKAndInternationalRacesWithIn15Min() {
    List<MetaEvent> eventList = new ArrayList<>();

    eventList.add(getMetaEvent(true, 5, "UK,IE"));
    eventList.add(getMetaEvent(false, 2, "INT"));
    eventList.add(getMetaEvent(true, 1, "UK"));
    eventList.add(getMetaEvent(true, 13, "INT"));
    return eventList;
  }

  private List<MetaEvent> getInternationalRaces() {
    List<MetaEvent> eventList = new ArrayList<>();

    eventList.add(getMetaEvent(true, 35, "INT"));
    eventList.add(getMetaEvent(false, 22, "INT"));
    eventList.add(getMetaEvent(true, 21, "INT"));
    eventList.add(getMetaEvent(true, 17, "INT"));
    eventList.add(getMetaEvent(true, 19, "INT"));
    return eventList;
  }

  private MetaEvent getMetaEvent(boolean isTipAvail, long minToAdd, String typeFlagCodes) {
    MetaEvent event = new MetaEvent();
    event.setEventId("1");
    event.setStartTime(Instant.now().plus(minToAdd, ChronoUnit.MINUTES));
    event.setTipAvailable(isTipAvail);
    event.setTypeFlagCodes(typeFlagCodes);
    return event;
  }

  private Iterable<NextRaceMap> getNextRaceMap() {
    Gson gson = new Gson();
    List<NextRaceMap> nextRaces = new ArrayList<>();
    NextRace race = new NextRace();
    race.setId("2121");
    race.setIsActive(true);
    race.setName("race");
    race.setRaceNo(131);
    race.setRaceName("raceName");
    nextRaces.add(new NextRaceMap("21212", gson.toJson(race), 5));
    return nextRaces;
  }
}
