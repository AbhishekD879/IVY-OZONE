package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.junit.Assert.assertEquals;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.repository.GameRepository;
import com.ladbrokescoral.oxygen.cms.api.service.*;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import java.time.Duration;
import java.time.Instant;
import java.util.Arrays;
import java.util.Collections;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.AdditionalAnswers;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      Games.class,
      GameService.class,
      GameEventService.class,
    })
@AutoConfigureMockMvc(addFilters = false)
@MockBean({TeamKitService.class, GameScoreService.class})
public class GameServiceTest extends AbstractControllerTest {

  private static final String CORAL_BRAND = "bma";

  @MockBean private GameRepository repository;
  @MockBean private BrandService brandService;
  @MockBean private SiteServerApi siteServerApi;
  @MockBean private SiteServeApiProvider siteServeApiProvider;
  @MockBean private ImageService imageService;
  @MockBean private SvgImageParser svgImageParser;
  @MockBean private GamificationService gamificationService;

  @Autowired private ObjectMapper mapper;

  @Before
  public void init() {

    given(repository.findById(anyString())).willReturn(Optional.of(createGame(-1, 2)));
    given(repository.save(any(Game.class))).will(AdditionalAnswers.returnsFirstArg());

    given(brandService.findByBrandCode(anyString())).willReturn(Optional.empty());
    given(brandService.findByBrandCode(CORAL_BRAND)).willReturn(Optional.of(new Brand()));

    Event event = new Event();
    event.setStartTime("2018-10-23T10:12:35Z");

    given(siteServerApi.getEvent(anyString(), anyBoolean())).willReturn(Optional.of(event));
    given(siteServerApi.getEvent(eq("keinEvent"), anyBoolean()))
        .willReturn(Optional.ofNullable(null));

    given(siteServeApiProvider.api(CORAL_BRAND)).willReturn(siteServerApi);

    given(svgImageParser.parse(any())).willReturn(Optional.of(new Svg()));
    given(imageService.upload(eq(CORAL_BRAND), any(), any(), any(), any()))
        .willReturn(Optional.of(getFileName("test")));
    given(imageService.removeImage(eq(CORAL_BRAND), any())).willReturn(true);
  }

  @Test
  public void getGames() throws Exception {
    this.mockMvc
        .perform(get("/v1/api/game/brand/bma").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void testCreateGame() throws Exception {
    Game dto = createGame(-2, 1);
    this.mockMvc
        .perform(
            post("/v1/api/game")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().isCreated());
  }

  @Test
  public void testCreateGameError() throws Exception {
    Game dto = new Game();
    this.mockMvc
        .perform(
            post("/v1/api/game")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().isBadRequest());
  }

  @Test
  public void testCreateGameAlreadyExists() throws Exception {

    Game game = createGame(0, 5);
    game.setEnabled(true);

    when(repository.findByDisplayFromIsBeforeAndDisplayToIsAfterAndBrandIsAndEnabledIsTrueAndIdNot(
            any(), any(), eq(CORAL_BRAND), eq(null)))
        .thenReturn(Collections.singletonList(new Game()));

    this.mockMvc
        .perform(
            post("/v1/api/game")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(game)))
        .andExpect(status().isBadRequest());
  }

  @Test
  public void testUpdateGame() throws Exception {
    Game dto = createGame(-2, 1);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/game/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().isOk());
  }

  @Test
  public void testUpdateGameWhenSeasonNotPresent() throws Exception {
    Game dto = createGame(-2, 1);
    dto.setSeasonId(null);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/game/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().isOk());
  }

  @Test
  public void testUpdateGameWithSortedEvents() throws Exception {
    Game game = createGame(-2, 1);
    GameEvent first = createGameEvent("first", Instant.ofEpochMilli(1234567871));
    GameEvent third = createGameEvent("third", Instant.ofEpochMilli(1234567893));
    GameEvent second = createGameEvent("second", Instant.ofEpochMilli(1234567882));
    game.setEvents(Arrays.asList(second, createGameEvent("test", null), third, first, null));

    String responseContent =
        this.mockMvc
            .perform(
                MockMvcRequestBuilders.put("/v1/api/game/1")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(TestUtil.convertObjectToJsonBytes(game)))
            .andReturn()
            .getResponse()
            .getContentAsString();

    Game returnedGame = mapper.readValue(responseContent, Game.class);
    assertEquals(4, returnedGame.getEvents().size());
    assertEquals(returnedGame.getEvents().get(0).getStartTime(), Instant.ofEpochMilli(1234567871));
    assertEquals(returnedGame.getEvents().get(1).getStartTime(), Instant.ofEpochMilli(1234567882));
    assertEquals(returnedGame.getEvents().get(2).getStartTime(), Instant.ofEpochMilli(1234567893));
  }

  @Test
  public void testGetGames() throws Exception {
    this.mockMvc
        .perform(get("/v1/api/game").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetByBrand() throws Exception {
    this.mockMvc
        .perform(get("/v1/api/game/brand/bma").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void testGetById() throws Exception {
    this.mockMvc
        .perform(get("/v1/api/game/1").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void testGetByIdError() throws Exception {
    given(repository.findById(anyString())).willReturn(Optional.empty());
    this.mockMvc
        .perform(get("/v1/api/game/1").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testDelete() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/game/1").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNoContent());
  }

  @Test
  public void testGetEventById() throws Exception {
    this.mockMvc
        .perform(get("/v1/api/game/brand/bma/event-id/112").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void testGetEventByIdNotPresent() throws Exception {
    this.mockMvc
        .perform(
            get("/v1/api/game/brand/bma/event-id/keinEvent")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNoContent());
  }

  @Test
  public void testUploadImage() throws Exception {
    final MockMultipartFile file = new MockMultipartFile("file", "test.svg", "", new byte[0]);
    this.mockMvc
        .perform(
            multipart("/v1/api/game/123456/image/event/678/team/home")
                .file(file)
                .param("fileType", "svg"))
        .andExpect(status().isOk());
  }

  @Test
  public void testUploadImageValidationError() throws Exception {
    doReturn(Optional.empty()).when(svgImageParser).parse(any());
    final MockMultipartFile file = new MockMultipartFile("file", "test.svg", "", new byte[0]);
    this.mockMvc
        .perform(
            multipart("/v1/api/game/123456/image/event/678/team/home")
                .file(file)
                .param("fileType", "svg"))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testRemoveImage() throws Exception {
    mockMvc
        .perform(delete("/v1/api/game/123456/image/event/678/team/home"))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testRemoveImageNotFound() throws Exception {
    mockMvc
        .perform(delete("/v1/api/game/123456/image/event/6789/team/home"))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testSetScores() throws Exception {
    EventScore dto = createEventScore("54321", 1);
    this.mockMvc
        .perform(
            post("/v1/api/game/123456/score")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().isOk());
  }

  @Test
  public void testGetScores() throws Exception {
    this.mockMvc
        .perform(
            get("/v1/api/game/123456/score")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(Arrays.asList(1, 1))))
        .andExpect(status().isOk());
  }

  private static GameEvent createGameEvent(String name, Instant startTime) {
    GameEvent gameEvent = new GameEvent();
    Team away = new Team();
    away.setTeamKitIcon(name);
    away.setDisplayName(name);
    away.setName(name);
    Team home = new Team();
    home.setTeamKitIcon(name);
    home.setDisplayName(name);
    home.setName(name);
    gameEvent.setAway(away);
    gameEvent.setHome(home);
    gameEvent.setEventId(name);
    gameEvent.setStartTime(startTime);
    return gameEvent;
  }

  private static Game createGame(int displayFromAddDays, int displayToAddDays) {
    Game dto = new Game();
    dto.setBrand(CORAL_BRAND);
    dto.setTitle("testGameId");
    dto.setDisplayFrom(Instant.now().plus(Duration.ofDays(displayFromAddDays)));
    dto.setDisplayTo(Instant.now().plus(Duration.ofDays(displayToAddDays - displayFromAddDays)));
    GameEvent gameEvent = new GameEvent();
    gameEvent.setEventId("678");
    Team home = new Team();
    home.setName("TestHomeTeam");
    home.setTeamKitIcon("");
    gameEvent.setHome(home);
    dto.setEvents(Collections.singletonList(gameEvent));
    dto.setSeasonId("1");
    return dto;
  }

  private static EventScore createEventScore(String eventId, Integer eventPosition) {
    EventScore eventScore = new EventScore();
    eventScore.setEventId(eventId);
    eventScore.setEventPosition(eventPosition);
    eventScore.setActualScores(new Integer[] {1, 2});
    return eventScore;
  }

  private static Filename getFileName(String name) {
    Filename filename = new Filename();
    filename.setPath("/test/path");
    filename.setFilename(name);
    filename.setOriginalname("test.svg");
    return filename;
  }
}
