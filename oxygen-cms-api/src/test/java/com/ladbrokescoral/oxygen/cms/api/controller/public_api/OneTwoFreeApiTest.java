package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.Users;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.exception.ActiveGameNotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.GameRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.QualificationRuleRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.StaticTextOtfRepository;
import com.ladbrokescoral.oxygen.cms.api.service.AuthenticationService;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.GameService;
import com.ladbrokescoral.oxygen.cms.api.service.StaticTextOtfService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.GamePublicService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.OtfIosAppTogglePublicService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.QualificationRulePublicService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.StaticTextOtfPublicService;
import java.io.IOException;
import java.time.Duration;
import java.time.Instant;
import java.util.*;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.data.domain.Sort;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      Users.class,
      AuthenticationService.class,
      GamePublicService.class,
      GameService.class,
      StaticTextOtfService.class,
      StaticTextOtfPublicService.class,
      OneTwoFreeApi.class,
      BrandService.class,
      QualificationRulePublicService.class,
      GameRepository.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class OneTwoFreeApiTest {

  @MockBean private GameRepository repository;
  @MockBean private StaticTextOtfRepository staticTextRepository;
  @MockBean private BrandService brandService;
  @MockBean private UserService userServiceMock;
  @MockBean private QualificationRuleRepository qualificationRuleRepository;
  @MockBean private OtfIosAppTogglePublicService otfIosAppTogglePublicService;
  @Autowired private MockMvc mockMvc;
  private Game createOneTwoFreeApi;

  @Before
  public void init() throws IOException {
    final ObjectMapper jsonMapper = new ObjectMapper();
    jsonMapper.configure(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS, false);
    jsonMapper.registerModule(new JavaTimeModule());
    createOneTwoFreeApi =
        jsonMapper.readValue(
            TestUtil.class.getResourceAsStream(
                "controller/public_api/one-two-free-api/createOneTwoFreeApi.json"),
            new TypeReference<Game>() {});

    given(brandService.findByBrandCode(anyString())).willReturn(Optional.empty());
    given(staticTextRepository.findByBrand(eq("bma"), any(Sort.class)))
        .willReturn(Collections.singletonList(createStaticText()));
    given(
            repository.findByDisplayFromIsBeforeAndDisplayToIsAfterAndBrandIsAndEnabledIsTrue(
                any(), any(), eq("ladbrokes")))
        .willReturn(Arrays.asList(createOneTwoFreeApi));
    given(repository.findById(any())).willReturn(Optional.of(createOneTwoFreeApi));

    given(
            repository.findByDisplayFromIsBeforeAndDisplayToIsAfterAndBrandIsAndEnabledIsTrue(
                any(), any(), eq("bma")))
        .willThrow(new ActiveGameNotFoundException());
    given(repository.findLastBeforeActive("bma")).willReturn(Arrays.asList(createOneTwoFreeApi));
    given(repository.findLastBeforeActive("bma")).willThrow(new ActiveGameNotFoundException());
  }

  @Test
  public void getActiveGame() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/one-two-free/game")
                .contentType(MediaType.APPLICATION_JSON)
                .param("gameState", "ACTIVE"))
        .andExpect(status().isOk());
  }

  @Test
  public void getGameById() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/one-two-free/game")
                .contentType(MediaType.APPLICATION_JSON)
                .param("gameId", "5e305c78c9e77c0001788672"))
        .andExpect(status().isOk());
  }

  @Test
  public void getActiveGameNoActive() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/one-two-free/game")
                .contentType(MediaType.APPLICATION_JSON)
                .param("gameState", "ACTIVE"))
        .andExpect(status().isNotFound());
  }

  @Test
  public void getActiveGameWrongRequestParams() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/one-two-free/game")
                .contentType(MediaType.APPLICATION_JSON)
                .param("gameState", "WRONG_STATE"))
        .andExpect(status().isBadRequest());
  }

  @Test
  public void getActiveGameNoRequestParams() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/one-two-free/game")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isBadRequest());
  }

  @Test
  public void getActiveMoreThanOneExists() throws Exception {
    when(repository.findByDisplayFromIsBeforeAndDisplayToIsAfterAndBrandIsAndEnabledIsTrue(
            any(), any(), eq("bma")))
        .thenReturn(Arrays.asList(createOneTwoFreeApi));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/one-two-free/game")
                .contentType(MediaType.APPLICATION_JSON)
                .param("gameState", "ACTIVE"))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void getPreviousGame() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/one-two-free/game")
                .contentType(MediaType.APPLICATION_JSON)
                .param("gameState", "BEFORE_ACTIVE"))
        .andExpect(status().isOk());
  }

  @Test
  public void getPreviousGameNoPrevious() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/one-two-free/game")
                .contentType(MediaType.APPLICATION_JSON)
                .param("gameState", "BEFORE_ACTIVE"))
        .andExpect(status().isNotFound());
  }

  @Test
  public void getPreviousGameWhenGameListEmpty() throws Exception {
    given(repository.findLastBeforeActive("ladbrokes")).willReturn(new ArrayList<>());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/one-two-free/game")
                .contentType(MediaType.APPLICATION_JSON)
                .param("gameState", "BEFORE_ACTIVE"))
        .andExpect(status().isOk());
  }

  @Test
  public void getActiveStaticTexts() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/one-two-free/static-texts")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void getGamesByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/one-two-free/games")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void getQualificationRule() throws Exception {
    QualificationRule qualificationRule =
        new QualificationRule().setBrand("ladbrokes").setEnabled(true).setMessage("Test Message");

    when(qualificationRuleRepository.findOneByBrandAndEnabledIsTrue("ladbrokes"))
        .thenReturn(Optional.ofNullable(qualificationRule));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/one-two-free/qualification-rule")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void testfindPreviousCurrentAndFutureGameByBrandTrue() throws Exception {
    given(repository.findLastBeforeActive(anyString()))
        .willReturn(Arrays.asList(createOneTwoFreeApi));
    given(
            repository.findByDisplayFromIsBeforeAndDisplayToIsAfterAndBrandIsAndEnabledIsTrue(
                any(), any(), any()))
        .willReturn(Arrays.asList(createOneTwoFreeApi));
    given(repository.findByDisplayFromIsGreaterThanEqualAndBrandIsAndEnabledIsTrue(any(), any()))
        .willReturn(Arrays.asList(createGameForFutureGame(-1, 4)));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/one-two-free/previous-current-future-game")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testfindCurrentAndFutureGameByBrand() throws Exception {
    given(repository.findLastBeforeActive(anyString()))
        .willReturn(Arrays.asList(createOneTwoFreeApi));
    given(
            repository.findByDisplayFromIsBeforeAndDisplayToIsAfterAndBrandIsAndEnabledIsTrue(
                any(), any(), any()))
        .willReturn(Arrays.asList(createOneTwoFreeApi));
    given(repository.findByDisplayFromIsGreaterThanEqualAndBrandIsAndEnabledIsTrue(any(), any()))
        .willReturn(Arrays.asList(createGameForFutureGame(-1, 4)));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/one-two-free/current-future-game")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void findPreviousCurrentAndFutureGameByBrandbothfalse() throws Exception {
    given(repository.findLastBeforeActive(anyString()))
        .willReturn(Arrays.asList(createOneTwoFreeApi));
    given(
            repository.findByDisplayFromIsBeforeAndDisplayToIsAfterAndBrandIsAndEnabledIsTrue(
                any(), any(), any()))
        .willReturn(Collections.emptyList());
    given(repository.findByDisplayFromIsGreaterThanEqualAndBrandIsAndEnabledIsTrue(any(), any()))
        .willReturn(Arrays.asList(createOneTwoFreeApi));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/one-two-free/previous-current-future-game")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void findPreviousCurrentAndFutureGameByBrandTF() throws Exception {
    List<Game> game = new ArrayList<>();
    game.add(createOneTwoFreeApi);
    given(repository.findLastBeforeActive(anyString()))
        .willReturn(Arrays.asList(createOneTwoFreeApi));
    given(
            repository.findByDisplayFromIsBeforeAndDisplayToIsAfterAndBrandIsAndEnabledIsTrue(
                any(), any(), any()))
        .willReturn((Arrays.asList(createOneTwoFreeApi)));
    given(repository.findByDisplayFromIsGreaterThanEqualAndBrandIsAndEnabledIsTrue(any(), any()))
        .willReturn(game);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/one-two-free/previous-current-future-game")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void findPreviousCurrentAndFutureGameByBrandIdnull() throws Exception {
    Game dto1 = createOneTwoFreeApi;
    dto1.setId(null);
    given(repository.findLastBeforeActive(anyString())).willReturn(Arrays.asList(dto1));
    given(
            repository.findByDisplayFromIsBeforeAndDisplayToIsAfterAndBrandIsAndEnabledIsTrue(
                any(), any(), any()))
        .willReturn(Arrays.asList(createOneTwoFreeApi));
    given(repository.findByDisplayFromIsGreaterThanEqualAndBrandIsAndEnabledIsTrue(any(), any()))
        .willReturn(Arrays.asList(createGameForFutureGame(-1, 4)));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/one-two-free/previous-current-future-game")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private StaticTextOtf createStaticText() {
    StaticTextOtf dto = new StaticTextOtf();
    dto.setBrand("bma");
    dto.setEnabled(true);
    dto.setCtaText1("CtaText1");
    dto.setCtaText2("CtaText2");
    dto.setPageName("PageName1");
    dto.setPageText1("PageText1");
    dto.setPageText2("PageText2");
    dto.setPageText1("PageText3");
    dto.setPageText2("PageText4");
    dto.setPageText2("PageText5");
    dto.setId("privateCmsId");
    return dto;
  }

  private Game createGameForFutureGame(int displayFromAddDays, int displayToAddDays) {
    Game dto = new Game();
    dto.setBrand("bma");
    dto.setTitle("testGameID");
    dto.setId("1234");
    dto.setDisplayFrom(Instant.now().plus(Duration.ofDays(displayFromAddDays)));
    dto.setDisplayTo(Instant.now().plus(Duration.ofDays(displayToAddDays - displayFromAddDays)));
    return dto;
  }
}
