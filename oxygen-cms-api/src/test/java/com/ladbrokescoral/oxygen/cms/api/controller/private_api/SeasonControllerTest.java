package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.Game;
import com.ladbrokescoral.oxygen.cms.api.entity.Gamification;
import com.ladbrokescoral.oxygen.cms.api.entity.Season;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.BrandRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.GameRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.GamificationRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SeasonRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.SeasonService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
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

@WebMvcTest({SeasonController.class, SeasonService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
class SeasonControllerTest extends AbstractControllerTest {

  @MockBean SeasonRepository seasonRepository;
  @MockBean GamificationRepository gamificationRepository;
  @MockBean GameRepository gameRepository;
  @MockBean BrandService brandService;
  @MockBean BrandRepository brandRepository;

  private List<Season> seasonList;

  private Season entity;
  private Season updateSeasonEntity;

  public static final String API_BASE_URL = "/v1/api/season";
  public static final String SEASON_ID = "1";
  public static final String BRAND = "ladbrokes";

  @BeforeEach
  public void setUp() throws IOException {
    entity =
        TestUtil.deserializeWithJackson("controller/private_api/createSeason.json", Season.class);
    updateSeasonEntity =
        TestUtil.deserializeWithJackson("controller/private_api/updateSeason.json", Season.class);

    given(seasonRepository.save(any(Season.class))).will(AdditionalAnswers.returnsFirstArg());
    doReturn(Optional.of(entity)).when(seasonRepository).findById(any(String.class));
    seasonList = new ArrayList<>();
    seasonList.add(entity);
  }

  @Test
  void createSeasonTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void seasonAlreadyExist() throws Exception {
    seasonList.add(updateSeasonEntity);
    given(
            seasonRepository.findByBrandAndDisplayToIsGreaterThanEqualAndDisplayFromIsLessThan(
                any(), any(), any()))
        .willReturn(seasonList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is5xxServerError());
  }

  @Test
  void updateSeasonTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + SEASON_ID + "/" + false)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(updateSeasonEntity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void updateSeasonWhenSeasonDateIsChangedAndSeasonNotExistAlreadyTest() throws Exception {
    given(
            seasonRepository.findByBrandAndDisplayToIsGreaterThanEqualAndDisplayFromIsLessThan(
                any(), any(), any()))
        .willReturn(new ArrayList<>());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + SEASON_ID + "/" + true)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(updateSeasonEntity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void updateSeasonWhenSeasonDateChangeButSeasonAlreadyExistTest() throws Exception {
    seasonList = new ArrayList<>();
    seasonList.add(updateSeasonEntity);
    Season season2 = new Season();
    season2.setId("61f27536008b6f5f2aa2213c");
    seasonList.add(season2);
    given(
            seasonRepository.findByBrandAndDisplayToIsGreaterThanEqualAndDisplayFromIsLessThan(
                any(), any(), any()))
        .willReturn(seasonList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + SEASON_ID + "/" + true)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(updateSeasonEntity)))
        .andExpect(status().is5xxServerError());
  }

  @Test
  void getSeasonTest() throws Exception {
    Game game = new Game();
    game.setSeasonId(SEASON_ID);
    game.setTitle("Game 1");
    Gamification gamification = new Gamification();
    gamification.setSeasonId(SEASON_ID);
    given(gameRepository.findBySeasonId(any())).willReturn(Arrays.asList(game));
    given(gamificationRepository.findBySeasonId(any())).willReturn(Optional.of(gamification));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/" + SEASON_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void getSeasonWithoutGameTest() throws Exception {
    Gamification gamification = new Gamification();
    gamification.setSeasonId(SEASON_ID);
    given(gamificationRepository.findBySeasonId(any())).willReturn(Optional.of(gamification));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/" + SEASON_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void getSeasonWithoutGamificationTest() throws Exception {
    Game game = new Game();
    game.setSeasonId(SEASON_ID);
    game.setTitle("Game 1");
    given(gameRepository.findBySeasonId(any())).willReturn(Arrays.asList(game));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/" + SEASON_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void getSeasonNotFoundExceptionTest() throws Exception {
    when(seasonRepository.findById(any())).thenReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/" + SEASON_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  void deleteSeasonTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(API_BASE_URL + "/" + SEASON_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void getSeasonsByBrandWithGamificationLinkedTest() throws Exception {
    seasonList = new ArrayList<>();
    entity.setId("1");
    seasonList.add(entity);
    Gamification gamification = new Gamification();
    gamification.setSeasonId(entity.getId());
    Game game = new Game();
    game.setTitle("Game1");
    game.setBrand("ladbrokes");
    game.setSeasonId(entity.getId());
    given(seasonRepository.findByBrand(any(), any())).willReturn(seasonList);
    given(gamificationRepository.findByBrand(any())).willReturn(Arrays.asList(gamification));
    given(gameRepository.findByBrand(any())).willReturn(Arrays.asList(game));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/brand/" + BRAND + "?sort=updatedAt,asc")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void getSeasonsByBrandWithGamificationLinkedAndGameNotLinkedTest() throws Exception {
    seasonList = new ArrayList<>();
    entity.setId("1");
    seasonList.add(entity);
    Gamification gamification = new Gamification();
    gamification.setSeasonId(entity.getId());
    given(seasonRepository.findByBrand(any(), any())).willReturn(seasonList);
    given(gamificationRepository.findByBrand(any())).willReturn(Arrays.asList(gamification));
    given(gameRepository.findByBrand(any())).willReturn(new ArrayList<>());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/brand/" + BRAND + "?sort=updatedAt,asc")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void getSeasonsByBrandWithGamificationNotLinkedTest() throws Exception {
    Gamification gamification = new Gamification();
    gamification.setSeasonId("2");
    given(gamificationRepository.findByBrand(any())).willReturn(Arrays.asList(gamification));
    entity.setId("1");
    seasonList = new ArrayList<>();
    seasonList.add(entity);
    given(seasonRepository.findByBrand(any(), any())).willReturn(seasonList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/brand/" + BRAND + "?sort=updatedAt,asc")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void getSeasonByIdNotFoundExceptionTest() throws NotFoundException {
    try {
      SeasonService seasonService =
          Mockito.spy(
              new SeasonService(seasonRepository, gamificationRepository, gameRepository, null));
      seasonService.getSeasonById(Optional.empty(), "1");
    } catch (Exception ex) {
      Assertions.assertEquals(NotFoundException.class, ex.getClass());
    }
  }

  @Test
  void getActiveSeasonTest() {
    SeasonService seasonService =
        Mockito.spy(
            new SeasonService(seasonRepository, gamificationRepository, gameRepository, null));
    List<Season> seasonList = seasonService.getActiveSeason("BMA");
    Assertions.assertNotNull(seasonList);
  }

  @Test
  void getCurrentFutureSeasonsWithOnlyFutureSeasonTest() {
    SeasonService seasonService =
        Mockito.spy(
            new SeasonService(seasonRepository, gamificationRepository, gameRepository, null));
    Mockito.when(
            seasonRepository.findByBrandAndDisplayFromIsLessThanEqualAndDisplayToGreaterThanEqual(
                any(), any(), any()))
        .thenReturn(new ArrayList<>());
    List<Season> seasonList = seasonService.getCurrentFutureSeasons("BMA");
    Assertions.assertNotNull(seasonList);
  }

  @Test
  void getCurrentFutureSeasonsWithActiveSeasonTest() {
    SeasonService seasonService =
        Mockito.spy(
            new SeasonService(seasonRepository, gamificationRepository, gameRepository, null));
    Mockito.when(
            seasonRepository.findByBrandAndDisplayFromIsLessThanEqualAndDisplayToGreaterThanEqual(
                any(), any(), any()))
        .thenReturn(seasonList);
    List<Season> seasonList = seasonService.getCurrentFutureSeasons("BMA");
    Assertions.assertNotNull(seasonList);
  }
}
