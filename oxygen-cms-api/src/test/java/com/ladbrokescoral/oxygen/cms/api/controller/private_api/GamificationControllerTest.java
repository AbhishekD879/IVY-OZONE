package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.exception.GameCreationException;
import com.ladbrokescoral.oxygen.cms.api.repository.AssetManagementRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.BrandRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.GamificationRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.GamificationService;
import com.ladbrokescoral.oxygen.cms.api.service.SeasonService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.io.IOException;
import java.time.Instant;
import java.util.*;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.AdditionalAnswers;
import org.mockito.Mockito;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({GamificationController.class, GamificationService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
class GamificationControllerTest extends AbstractControllerTest {

  @MockBean GamificationRepository gamificationRepository;
  @MockBean AssetManagementRepository assetManagementRepository;
  @MockBean BrandService brandService;
  @MockBean BrandRepository brandRepository;
  @MockBean SeasonService seasonService;

  private Gamification entity;
  private Gamification updateGamification;

  public static final String API_BASE_URL = "/v1/api/gamification";
  public static final String GAMIFICATION_ID = "1";
  public static final String BRAND = "ladbrokes";

  @BeforeEach
  public void setUp() throws IOException {
    entity =
        TestUtil.deserializeWithJackson(
            "controller/private_api/createGamification.json", Gamification.class);
    updateGamification =
        TestUtil.deserializeWithJackson(
            "controller/private_api/updateGamification.json", Gamification.class);
    given(gamificationRepository.save(any(Gamification.class)))
        .will(AdditionalAnswers.returnsFirstArg());
    doReturn(Optional.of(entity)).when(gamificationRepository).findById(any(String.class));
  }

  @Test
  void createGamificationTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void getGamificationTest() throws Exception {
    when(assetManagementRepository.findByIdIn(any())).thenReturn(setAssetManagement());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/" + GAMIFICATION_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void getGamificationWithNoTeamsLinkedTest() throws Exception {
    when(assetManagementRepository.findByIdIn(any()))
        .thenReturn(Arrays.asList(new AssetManagement()));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/" + GAMIFICATION_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void updateGamificationTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + GAMIFICATION_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(updateGamification)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void deleteGamificationTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(API_BASE_URL + "/" + GAMIFICATION_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void findGamificationByBrandTest() throws Exception {
    List<Gamification> gamificationList = new ArrayList<>();
    gamificationList.add(entity);
    when(gamificationRepository.findByBrand(any())).thenReturn(gamificationList);
    Season season = new Season();
    season.setId("1");
    season.setSeasonName("Season1");
    season.setDisplayFrom(Instant.now());
    season.setDisplayTo(Instant.now());
    when(seasonService.findByBrand(any())).thenReturn(Collections.singletonList(season));
    when(assetManagementRepository.findByIdIn(any())).thenReturn(setAssetManagement());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void findGamificationByBrandWhenSeasonIdNotEqualTest() throws Exception {
    List<Gamification> gamificationList = new ArrayList<>();
    gamificationList.add(entity);
    when(gamificationRepository.findByBrand(any())).thenReturn(gamificationList);
    Season season = new Season();
    season.setId("2");
    season.setSeasonName("Season2");
    when(seasonService.findByBrand(any())).thenReturn(Collections.singletonList(season));
    when(assetManagementRepository.findByIdIn(any()))
        .thenReturn(Arrays.asList(new AssetManagement()));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void findGamificationByBrandNullTest() throws Exception {
    when(gamificationRepository.findByBrand(any())).thenReturn(new ArrayList<>());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(new Gamification())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void findGamificationBySeasonIdTest() {
    GamificationService gamificationService =
        Mockito.spy(
            new GamificationService(
                gamificationRepository, assetManagementRepository, null, seasonService));
    Optional<Gamification> gamificationList = gamificationService.findGamificationBySeasonId("1");
    Assertions.assertNotNull(gamificationList);
  }

  @Test
  void findAllGamificationBySeasonIdTest() {
    GamificationService gamificationService =
        Mockito.spy(
            new GamificationService(
                gamificationRepository, assetManagementRepository, null, seasonService));
    List<Optional<Gamification>> gamificationList =
        gamificationService.findAllGamificationBySeasonId(Collections.singletonList("1"));
    Assertions.assertNotNull(gamificationList);
  }

  @Test
  void testValidateGameTeamNameWithSeasonTeamNameHappyPath() {
    GamificationService gamificationService =
        Mockito.spy(
            new GamificationService(
                gamificationRepository, assetManagementRepository, null, seasonService));
    when(gamificationRepository.findBySeasonId(any())).thenReturn(Optional.of(entity));
    when(assetManagementRepository.findAllById(any())).thenReturn(setAssetManagement());
    entity.setId("GM1");
    Game game = createGame();
    game.getEvents().get(0).getAway().setDisplayName("Newcastle");
    gamificationService.validateGameTeamNameWithSeasonTeamName(game);
    Assertions.assertEquals("1", entity.getSeasonId());
  }

  @Test
  void testValidateGameTeamNameWithSeasonTeamNameWithException() throws GameCreationException {
    try {
      GamificationService gamificationService =
          Mockito.spy(
              new GamificationService(
                  gamificationRepository, assetManagementRepository, null, seasonService));
      when(gamificationRepository.findBySeasonId(any())).thenReturn(Optional.of(entity));
      when(assetManagementRepository.findAllById(any())).thenReturn(setAssetManagement());
      entity.setId("GM1");
      gamificationService.validateGameTeamNameWithSeasonTeamName(createGame());
    } catch (Exception ex) {
      Assertions.assertEquals(GameCreationException.class, ex.getClass());
    }
  }

  @Test
  void testValidateGameTeamNameWithSeasonTeamNameWhenTeamNotPresent() throws GameCreationException {
    try {
      GamificationService gamificationService =
          Mockito.spy(
              new GamificationService(
                  gamificationRepository, assetManagementRepository, null, seasonService));
      when(gamificationRepository.findBySeasonId(any())).thenReturn(Optional.empty());
      gamificationService.validateGameTeamNameWithSeasonTeamName(createGame());
    } catch (Exception ex) {
      Assertions.assertEquals(GameCreationException.class, ex.getClass());
    }
  }

  @Test
  void testValidateGameTeamNameWithSeasonTeamNameWhenHomeTeamIsNotPLTeam()
      throws GameCreationException {
    try {
      GamificationService gamificationService =
          Mockito.spy(
              new GamificationService(
                  gamificationRepository, assetManagementRepository, null, seasonService));
      when(gamificationRepository.findBySeasonId(any())).thenReturn(Optional.of(entity));
      Game game = createGame();
      game.getEvents().get(0).getHome().setIsNonPLTeam(null);
      gamificationService.validateGameTeamNameWithSeasonTeamName(game);
    } catch (Exception ex) {
      Assertions.assertEquals(GameCreationException.class, ex.getClass());
      Assertions.assertEquals("isNonPLTeam field is null", ex.getMessage());
    }
  }

  @Test
  void testValidateGameTeamNameWithSeasonTeamNameWhenAwayTeamIsNotPLTeam()
      throws GameCreationException {
    try {
      GamificationService gamificationService =
          Mockito.spy(
              new GamificationService(
                  gamificationRepository, assetManagementRepository, null, seasonService));
      when(gamificationRepository.findBySeasonId(any())).thenReturn(Optional.of(entity));
      Game game = createGame();
      game.getEvents().get(0).getAway().setIsNonPLTeam(null);
      gamificationService.validateGameTeamNameWithSeasonTeamName(game);
    } catch (Exception ex) {
      Assertions.assertEquals(GameCreationException.class, ex.getClass());
      Assertions.assertEquals("isNonPLTeam field is null", ex.getMessage());
    }
  }

  @Test
  void testValidateGameTeamNameWithSeasonTeamNameSetIsNonPLTeamTrue() {
    GamificationService gamificationService =
        Mockito.spy(
            new GamificationService(
                gamificationRepository, assetManagementRepository, null, seasonService));
    when(gamificationRepository.findBySeasonId(any())).thenReturn(Optional.of(entity));
    when(assetManagementRepository.findAllById(any())).thenReturn(setAssetManagement());
    entity.setId("GM1");
    Game game = createGame();
    game.getEvents().get(0).getAway().setIsNonPLTeam(true);
    game.getEvents().get(0).getHome().setIsNonPLTeam(true);
    gamificationService.validateGameTeamNameWithSeasonTeamName(game);
    Assertions.assertEquals("1", entity.getSeasonId());
  }

  private List<AssetManagement> setAssetManagement() {
    AssetManagement assetManagement1 = new AssetManagement();
    assetManagement1.setId("5784d7ee01b346ab3471d09a");
    assetManagement1.setTeamName("Arsenal");
    AssetManagement assetManagement2 = new AssetManagement();
    assetManagement2.setId("5784d7ee01b346ab3471c09b");
    assetManagement2.setTeamName("Newcastle");
    Filename filename = new Filename();
    filename.setSvg("Arsenal.svg");
    assetManagement2.setTeamsImage(filename);
    return Arrays.asList(assetManagement1, assetManagement2);
  }

  private static Game createGame() {
    Game dto = new Game();
    dto.setId("G1");
    dto.setBrand(BRAND);
    dto.setTitle("testGameId");
    GameEvent gameEvent = new GameEvent();
    gameEvent.setEventId("678");
    Team home = new Team();
    home.setDisplayName("Arsenal");
    home.setIsNonPLTeam(false);
    gameEvent.setHome(home);
    Team away = new Team();
    away.setDisplayName("Liverpool");
    away.setIsNonPLTeam(false);
    gameEvent.setAway(away);
    dto.setEvents(Collections.singletonList(gameEvent));
    dto.setSeasonId("1");
    return dto;
  }
}
