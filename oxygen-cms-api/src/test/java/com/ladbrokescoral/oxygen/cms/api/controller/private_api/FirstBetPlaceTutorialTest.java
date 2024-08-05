package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding.FirstBetPlaceTutorialDto;
import com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding.FirstBetPlaceTutorialDto.*;
import com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding.StepContentDto;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.onboarding.FirstBetPlaceTutorials;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CloseButton;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.FirstBetPlaceTutorial;
import com.ladbrokescoral.oxygen.cms.api.repository.FirstBetPlaceTutorialRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.FirstBetPlaceTutorialService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(value = {FirstBetPlaceTutorials.class, FirstBetPlaceTutorialService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
@MockBean(BrandService.class)
public class FirstBetPlaceTutorialTest extends AbstractControllerTest {
  @MockBean ImageService imageService;
  @MockBean FirstBetPlaceTutorialRepository repository;
  FirstBetPlaceTutorial entity;
  FirstBetPlaceTutorialDto firstBetPlaceTutorialDto;

  ModelMapper mapper = new ModelMapper();

  @Before
  public void init() {
    firstBetPlaceTutorialDto = createDto();
    FirstBetPlaceTutorial entity =
        mapper.map(firstBetPlaceTutorialDto, FirstBetPlaceTutorial.class);
    entity.setId("12121212121");
    entity.setCreatedBy("system");
    entity.setUpdatedAt(Instant.now());
    when(repository.save(any())).thenReturn(entity);
    when(repository.findById(any())).thenReturn(Optional.of(entity));
  }

  @Test
  public void testCreateFirstBetTutorial() throws Exception {
    when(repository.existsByBrand(Mockito.anyString())).thenReturn(false);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/first-bet-place-tutorial")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(firstBetPlaceTutorialDto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateFirstBetTutorialWhenActiveRecordPresent() throws Exception {
    when(repository.existsByBrand(Mockito.anyString())).thenReturn(true);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/first-bet-place-tutorial")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(firstBetPlaceTutorialDto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUpdateFirstBetTutorialIdNotFound() throws Exception {
    String id = "11102129130913132";
    when(repository.findById(id)).thenReturn(Optional.ofNullable(null));
    firstBetPlaceTutorialDto.setId(id);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/first-bet-place-tutorial/" + id)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(firstBetPlaceTutorialDto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUpdateFirstBetTutorial() throws Exception {
    when(repository.existsByBrand(Mockito.anyString())).thenReturn(false);
    String id = "1110212913091313";
    firstBetPlaceTutorialDto.setId(id);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/first-bet-place-tutorial/" + id)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(firstBetPlaceTutorialDto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToDeleteById() throws Exception {
    this.mockMvc
        .perform(
            delete("/v1/api/first-bet-place-tutorial/234344546566767")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadByIdNotFound() throws Exception {
    when(repository.findById(any())).thenReturn(Optional.ofNullable(null));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/first-bet-place-tutorial/233")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testReadById() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/first-bet-place-tutorial/233")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadByBrandException() throws Exception {
    when(repository.findByBrand(Mockito.anyString())).thenReturn(null);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/first-bet-place-tutorial/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testReadByBrand() throws Exception {
    FirstBetPlaceTutorial entity = mapper.map(createDto(), FirstBetPlaceTutorial.class);
    List<FirstBetPlaceTutorial> list = new ArrayList<>();
    list.add(entity);
    when(repository.findByBrand(Mockito.anyString())).thenReturn(list);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/first-bet-place-tutorial/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUploadImageSuccess() throws Exception {
    when(imageService.upload(
            anyString(),
            any(MockMultipartFile.class),
            anyString(),
            any(ImageServiceImpl.Size.class)))
        .thenReturn(Optional.of(createFileNames()));
    final MockMultipartFile file =
        new MockMultipartFile("file", "test1.png", "image/png", "file".getBytes());
    this.mockMvc
        .perform(multipart("/v1/api/first-bet-place-tutorial/1/image").file(file))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUploadSVGImageSuccess() throws Exception {
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.of(createSVGFileNames()));
    final MockMultipartFile file =
        new MockMultipartFile("file", "test1.svg", "image/svg", "file".getBytes());
    this.mockMvc
        .perform(multipart("/v1/api/first-bet-place-tutorial/1/image").file(file))
        .andExpect(status().is2xxSuccessful())
        .andDo(result -> result.getResponse())
        .andExpect(result -> result.getResponse());
  }

  @Test
  public void testUploadImageFailsWhenIdNotExists() throws Exception {

    when(repository.findById(anyString())).thenReturn(Optional.empty());
    when(imageService.upload(
            anyString(),
            any(MockMultipartFile.class),
            anyString(),
            any(ImageServiceImpl.Size.class)))
        .thenReturn(Optional.of(createFileNames()));
    final MockMultipartFile file =
        new MockMultipartFile("file", "test1.png", "image/png", "file".getBytes());
    mockMvc
        .perform(multipart("/v1/api/first-bet-place-tutorial/1/image").file(file))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUploadSVGImageFailsWhenIdNotExists() throws Exception {

    when(repository.findById(anyString())).thenReturn(Optional.empty());
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.of(createSVGFileNames()));
    final MockMultipartFile file =
        new MockMultipartFile("file", "test1.svg", "image/svg", "file".getBytes());
    mockMvc
        .perform(multipart("/v1/api/first-bet-place-tutorial/1/image").file(file))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUploadImageFails_FailedToUpdateImage() throws Exception {
    when(imageService.upload(
            anyString(),
            any(MockMultipartFile.class),
            anyString(),
            any(ImageServiceImpl.Size.class)))
        .thenReturn(Optional.empty());
    final MockMultipartFile file =
        new MockMultipartFile("file", "test1.png", "image/png", "file".getBytes());
    mockMvc
        .perform(multipart("/v1/api/first-bet-place-tutorial/1/image").file(file))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUploadSVGImageFails_FailedToUpdateImage() throws Exception {
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.empty());
    final MockMultipartFile file =
        new MockMultipartFile("file", "test1.svg", "image/svg", "file".getBytes());
    mockMvc
        .perform(multipart("/v1/api/first-bet-place-tutorial/1/image").file(file))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testRemoveImageSuccess() throws Exception {
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    mockMvc
        .perform(delete("/v1/api/first-bet-place-tutorial/1/image"))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testRemoveImageIdNotExists() throws Exception {
    when(repository.findById(anyString())).thenReturn(Optional.empty());
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    mockMvc
        .perform(delete("/v1/api/first-bet-place-tutorial/2/image"))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testRemoveImage_FailedtoRemove() throws Exception {
    when(imageService.removeImage(anyString(), anyString())).thenReturn(false);
    mockMvc
        .perform(delete(String.format("/v1/api/first-bet-place-tutorial/2/image")))
        .andExpect(status().is4xxClientError());
  }

  private FirstBetPlaceTutorialDto createDto() {

    FirstBetPlaceTutorialDto firstBetPlaceTutorialDto = new FirstBetPlaceTutorialDto();
    CloseButton btx = new CloseButton();
    btx.setDescription("DON'T NEED HELP");
    btx.setTitle("rember you can find your ttrls in my account");
    btx.setLeftButtonDesc("undo");
    btx.setRightButtonDesc("GOT IT");

    StepContentDto addToBetSlip = new StepContentDto();
    addToBetSlip.setDescription("Add the bet to BetSlip");
    addToBetSlip.setTitle("Add selection");

    StepContentDto pickurbet = new StepContentDto();
    pickurbet.setDescription("pick the bet");
    pickurbet.setTitle("Pick UR Bet");

    HomePageDto homepage = new HomePageDto();
    homepage.setTitle("new to ladbrokes");
    homepage.setDescription("we will guilde you Through your first bet with us");
    homepage.setButton("start tutorial");

    // betdetails
    BetDetailsDto betDetails = new BetDetailsDto();
    StepContentDto default_bet_details_content = new StepContentDto();
    default_bet_details_content.setDescription("betdetails page discription");
    default_bet_details_content.setTitle("Betdetails");

    StepContentDto cashout_bet_details_content = new StepContentDto();
    cashout_bet_details_content.setDescription("cashout page discription");
    cashout_bet_details_content.setTitle("BETDETAILS CASHOUT");

    betDetails.setCashOut(cashout_bet_details_content);
    betDetails.setDefaultContent(default_bet_details_content);
    // placeBet
    PlaceBetDto placeBet = new PlaceBetDto();
    StepContentDto default_place_bet_content = new StepContentDto();

    default_place_bet_content.setDescription("BetPlaced discription");
    default_place_bet_content.setTitle("Bet placed title");

    StepContentDto boost_bet_details_content = new StepContentDto();
    boost_bet_details_content.setDescription("boost page discription");
    boost_bet_details_content.setTitle("PlaceBet Boost");

    placeBet.setBoost(boost_bet_details_content);
    placeBet.setDefaultContent(default_place_bet_content);

    // betSlip
    BetSlipDto betSlip = new BetSlipDto();
    StepContentDto default_betSlip_content = new StepContentDto();

    default_betSlip_content.setDescription("bet slip  discription");
    default_betSlip_content.setTitle("BET SLIP");

    StepContentDto boost_bet_Slip_content = new StepContentDto();
    boost_bet_Slip_content.setDescription("boost page discription");
    boost_bet_Slip_content.setTitle("PlaceBet Boost");

    betSlip.setBoost(boost_bet_Slip_content);
    betSlip.setDefaultContent(default_betSlip_content);
    // MyBets
    MyBetsDto myBets = new MyBetsDto();

    StepContentDto default_myBets_content = new StepContentDto();
    default_myBets_content.setTitle("MYBETS");
    default_myBets_content.setDescription("my bets discription");

    StepContentDto cashout_myBets_content = new StepContentDto();
    cashout_myBets_content.setTitle("CashOut");
    cashout_myBets_content.setDescription("cashout my bets discription");

    myBets.setDefaultContent(default_myBets_content);
    myBets.setCashOut(cashout_myBets_content);
    myBets.setButtonDesc("OK THANKS!");

    StepContentDto betPlace_winAlert_content = new StepContentDto();
    betPlace_winAlert_content.setTitle("CashOut");
    betPlace_winAlert_content.setDescription("cashout my bets discription");

    StepContentDto betPlacedefault_content = new StepContentDto();
    betPlacedefault_content.setTitle("CashOut");
    betPlacedefault_content.setDescription("cashout my bets discription");

    BetPlaceDto betPlaceDto = new BetPlaceDto();

    betPlaceDto.setDefaultContent(betPlacedefault_content);
    betPlaceDto.setWinAlert(betPlace_winAlert_content);
    betPlaceDto.setButtonDesc("ok");

    firstBetPlaceTutorialDto.setModuleName("FirstBet");
    firstBetPlaceTutorialDto.setModuleDiscription("firstBetDetails");
    firstBetPlaceTutorialDto.setDisplayFrom(Instant.now());
    firstBetPlaceTutorialDto.setDisplayTo(Instant.now());
    firstBetPlaceTutorialDto.setBrand("ladbrokes");
    firstBetPlaceTutorialDto.setIsEnable(true);

    firstBetPlaceTutorialDto.setButton(btx);
    firstBetPlaceTutorialDto.setHomePage(homepage);
    firstBetPlaceTutorialDto.setPickYourBet(pickurbet);
    firstBetPlaceTutorialDto.setPlaceYourBet(placeBet);
    firstBetPlaceTutorialDto.setBetPlaced(betPlaceDto);
    firstBetPlaceTutorialDto.setMyBets(myBets);
    firstBetPlaceTutorialDto.setBetDetails(betDetails);
    firstBetPlaceTutorialDto.setBetSlip(betSlip);
    firstBetPlaceTutorialDto.setAddSelection(addToBetSlip);
    firstBetPlaceTutorialDto.setImageUrl("file.svg");
    return firstBetPlaceTutorialDto;
  }

  private static Filename createFileNames() {
    Filename filename = new Filename("name.png");
    filename.setFiletype("png");
    filename.setOriginalname("ogname.png");
    filename.setPath("files/images");
    filename.setSize("2");
    filename.setFullPath("files/image");
    filename.setSvg("svg");
    filename.setSvgId("23");
    return filename;
  }

  private static Filename createSVGFileNames() {
    Filename filename = new Filename("name.svg");
    filename.setFiletype("svg");
    filename.setOriginalname("ogname.svg");
    filename.setPath("files/images");
    filename.setSize("2");
    filename.setFullPath("files/image");
    filename.setSvg("svg");
    filename.setSvgId("23");
    return filename;
  }
}
