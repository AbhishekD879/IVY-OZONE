package com.ladbrokescoral.oxygen.cms.api.service;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNull;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.cms.api.entity.FileType;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.Game;
import com.ladbrokescoral.oxygen.cms.api.entity.GameEvent;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.entity.Team;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.mapping.GameEventMapper;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import java.util.Collections;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.web.multipart.MultipartFile;

@RunWith(MockitoJUnitRunner.class)
public class GameEventServiceTest extends BDDMockito {

  private static final String CORAL_BRAND = "bma";
  @Mock private SiteServerApi siteServerApi;

  @Mock private SiteServeApiProvider siteServeApiProvider;

  @Mock private ImageService imageService;

  @Mock private SvgImageParser svgImageParser;

  @Mock private TeamKitService teamKitService;
  private String teamKitPath = "/test/path/";

  private GameEventService gameEventService;

  @Before
  public void setUp() {
    gameEventService =
        new GameEventService(
            siteServeApiProvider, imageService, svgImageParser, teamKitService, teamKitPath);
    when(siteServeApiProvider.api(CORAL_BRAND)).thenReturn(siteServerApi);
  }

  @Test
  public void findByEventIdIdealNameFormat() {
    String eventId = "11245654";
    Event event = event(eventId);
    event.setName("|Team One| |vs| |Team Another|");

    when(siteServerApi.getEvent(eventId, true)).thenReturn(Optional.of(event));

    IncompleteGameEvent actual = gameEventService.findByEventId(CORAL_BRAND, eventId).get();

    assertThat(actual.getEventId()).isEqualTo(eventId);
    assertThat(actual.getHomeTeamName()).isEqualTo("Team One");
    assertThat(actual.getAwayTeamName()).isEqualTo("Team Another");
    assertThat(actual.getStartTime().toString()).isEqualTo(event.getStartTime());
  }

  @Test
  public void findByEventIdUpperCasedTeamDelimiter() {
    String eventId = "11245654";
    Event event = event(eventId);
    event.setName("|Team One| |Vs| |Team Another|");

    when(siteServerApi.getEvent(eventId, true)).thenReturn(Optional.of(event));

    IncompleteGameEvent actual = gameEventService.findByEventId(CORAL_BRAND, eventId).get();

    assertThat(actual.getEventId()).isEqualTo(eventId);
    assertThat(actual.getHomeTeamName()).isEqualTo("Team One");
    assertThat(actual.getAwayTeamName()).isEqualTo("Team Another");
    assertThat(actual.getStartTime().toString()).isEqualTo(event.getStartTime());
  }

  @Test
  public void findByEventIdUnexpectedEventNameFormat() {
    String eventId = "11245654";
    Event event = event(eventId);
    event.setName("$Team One$ x $Team Another$");

    when(siteServerApi.getEvent(eventId, true)).thenReturn(Optional.of(event));

    IncompleteGameEvent actual = gameEventService.findByEventId(CORAL_BRAND, eventId).get();

    assertThat(actual.getEventId()).isEqualTo(eventId);
    assertThat(actual.getHomeTeamName()).isEqualTo("$Team One$ x $Team Another$");
    assertThat(actual.getAwayTeamName()).isEqualTo("$Team One$ x $Team Another$");
    assertThat(actual.getStartTime().toString()).isEqualTo(event.getStartTime());
  }

  @Test
  public void findByEventIdUnexpectedEventNameDelimiter() {
    String eventId = "11245654";
    Event event = event(eventId);
    event.setName("$Team One$ vs $Team Another$");

    when(siteServerApi.getEvent(eventId, true)).thenReturn(Optional.of(event));

    IncompleteGameEvent actual = gameEventService.findByEventId(CORAL_BRAND, eventId).get();

    assertThat(actual.getEventId()).isEqualTo(eventId);
    assertThat(actual.getHomeTeamName()).isEqualTo("$Team One$");
    assertThat(actual.getAwayTeamName()).isEqualTo("$Team Another$");
    assertThat(actual.getStartTime().toString()).isEqualTo(event.getStartTime());
  }

  @Test
  public void findByEventIdEmptyName() {
    String eventId = "11245654";
    Event event = event(eventId);
    event.setName("");

    when(siteServerApi.getEvent(eventId, true)).thenReturn(Optional.of(event));

    IncompleteGameEvent actual = gameEventService.findByEventId(CORAL_BRAND, eventId).get();

    assertThat(actual.getEventId()).isEqualTo(eventId);
    assertThat(actual.getHomeTeamName()).isEmpty();
    assertThat(actual.getAwayTeamName()).isEmpty();
    assertThat(actual.getStartTime().toString()).isEqualTo(event.getStartTime());
  }

  @Test
  public void findByEventIdNullName() {
    String eventId = "11245654";
    Event event = event(eventId);
    event.setName(null);

    when(siteServerApi.getEvent(eventId, true)).thenReturn(Optional.of(event));

    IncompleteGameEvent actual = gameEventService.findByEventId(CORAL_BRAND, eventId).get();

    assertThat(actual.getEventId()).isEqualTo(eventId);
    assertThat(actual.getHomeTeamName()).isNull();
    assertThat(actual.getAwayTeamName()).isNull();
    assertThat(actual.getStartTime().toString()).isEqualTo(event.getStartTime());
  }

  @Test
  public void findByEventIdNotFound() {
    String eventId = "11245654";

    when(siteServerApi.getEvent(eventId, true)).thenReturn(Optional.empty());

    IncompleteGameEvent gameEvent =
        gameEventService.findByEventId(CORAL_BRAND, eventId).orElse(null);
    assertThat(gameEvent).isNull();
  }

  @Test
  public void getGameEventById() {
    GameEvent gameEvent = gameEventService.getGameEventById(getMockGame("123"), "123");
    assertEquals("123", gameEvent.getEventId());
  }

  @Test(expected = NotFoundException.class)
  public void getGameEventByIdNotFound() {
    gameEventService.getGameEventById(getMockGame("123"), "567");
  }

  @Test
  public void uploadGameEventTeamImageSVGWithoutName() {
    GameEvent gameEvent = getMockGame("123").getEvents().get(0);
    Filename filename = getFileName("test.svg");
    MultipartFile file = new MockMultipartFile("test.svg", "test.svg", "", new byte[0]);
    when(svgImageParser.parse(file)).thenReturn(Optional.of(new Svg()));
    when(imageService.upload(CORAL_BRAND, file, "/test/path/bma", "test", null))
        .thenReturn(Optional.of(filename));

    gameEventService.uploadGameEventTeamImage(
        gameEvent, "home", file, FileType.SVG, "", CORAL_BRAND);

    assertEquals("123", gameEvent.getEventId());
  }

  @Test
  public void uploadGameEventTeamImageSVGWithName() {
    GameEvent gameEvent = getMockGame("123").getEvents().get(0);
    Filename filename = getFileName("manchester.svg");
    MultipartFile file = new MockMultipartFile("test.svg", "test.svg", "", new byte[0]);
    when(svgImageParser.parse(file)).thenReturn(Optional.of(new Svg()));
    when(imageService.upload(CORAL_BRAND, file, "/test/path/bma", "manchester", null))
        .thenReturn(Optional.of(filename));
    gameEventService.uploadGameEventTeamImage(
        gameEvent, "home", file, FileType.SVG, "manchester", CORAL_BRAND);

    assertEquals("123", gameEvent.getEventId());
  }

  @Test
  public void uploadGameEventTeamImagePNGWithName() {
    GameEvent gameEvent = getMockGame("123").getEvents().get(0);
    Filename filename = getFileName("manchester.png");
    MultipartFile file = new MockMultipartFile("test.png", "test.png", "", new byte[0]);
    when(imageService.upload(CORAL_BRAND, file, "/test/path/bma", "manchester", null))
        .thenReturn(Optional.of(filename));
    gameEventService.uploadGameEventTeamImage(
        gameEvent, "home", file, null, "manchester", CORAL_BRAND);

    assertEquals("123", gameEvent.getEventId());
  }

  @Test(expected = IllegalStateException.class)
  public void uploadGameEventTeamImageError() {
    GameEvent gameEvent = getMockGame("123").getEvents().get(0);
    MultipartFile file = new MockMultipartFile("test.png", "test.png", "", new byte[0]);
    when(imageService.upload(CORAL_BRAND, file, "/test/path/bma", "manchester", null))
        .thenReturn(Optional.empty());
    gameEventService.uploadGameEventTeamImage(
        gameEvent, "home", file, null, "manchester", CORAL_BRAND);
  }

  @Test
  public void removeImage() {
    GameEvent gameEvent = getMockGame("123").getEvents().get(0);
    gameEvent.getHome().setTeamKitIcon("/test/path/test.png");

    gameEventService.removeImage(gameEvent, "home");

    assertNull(gameEvent.getHome().getTeamKitIcon());
  }

  private Game getMockGame(String id) {
    Game game = new Game();
    GameEvent event = new GameEvent();
    event.setEventId(id);
    Team home = new Team();
    home.setName("TestHomeTeam");
    event.setHome(home);
    game.setBrand(CORAL_BRAND);
    game.setTitle("TestGame");
    game.setEvents(Collections.singletonList(event));
    return game;
  }

  private Filename getFileName(String name) {
    Filename filename = new Filename();
    filename.setPath("/test/path/bma");
    filename.setFilename(name);
    filename.setOriginalname("test.svg");
    return filename;
  }

  private Event event(String eventId) {
    Event event = new Event();
    event.setId(eventId);
    event.setStartTime("2018-12-25T14:00:00Z");
    return event;
  }

  @Test
  public void testMapperDeclaration() {
    GameEventMapper teamMapper = GameEventMapper.getInstance();
    assertNotNull(teamMapper);
  }
}
