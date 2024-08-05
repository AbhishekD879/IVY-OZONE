package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CloseButton;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.FirstBetPlaceTutorial;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.FirstBetPlaceTutorial.*;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.StepContent;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.FirstBetPlaceTutorialService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.time.Instant;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(value = {FirstBetPlaceTutorialPublicApi.class, FirstBetPlaceTutorialService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
public class FirstBetPlaceTutorialPublicApiTest extends AbstractControllerTest {

  FirstBetPlaceTutorial entity;
  @MockBean FirstBetPlaceTutorialService service;
  ModelMapper mapper = new ModelMapper();

  @Before
  public void init() {
    entity = createEntity();
    entity.setId("12121212121");
    entity.setCreatedBy("system");
    entity.setUpdatedAt(Instant.now());
  }

  @Test
  public void testFindByBrand() throws Exception {

    given(service.readByBrand(Mockito.anyString())).willReturn(Optional.of(entity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/first-bet-place-tutorial/brand/bma")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  private FirstBetPlaceTutorial createEntity() {

    FirstBetPlaceTutorial firstBetPlaceTutorial = new FirstBetPlaceTutorial();
    CloseButton btx = new CloseButton();
    btx.setDescription("DON'T NEED HELP");
    btx.setTitle("rember you can find your ttrls in my account");
    btx.setLeftButtonDesc("undo");
    btx.setRightButtonDesc("GOT IT");

    StepContent addToBetSlip = new StepContent();
    addToBetSlip.setDescription("Add the bet to BetSlip");
    addToBetSlip.setTitle("Add selection");

    StepContent pickurbet = new StepContent();
    pickurbet.setDescription("pick the bet");
    pickurbet.setTitle("Pick UR Bet");

    FirstBetPlaceTutorial.HomePage homepage = new HomePage();
    homepage.setTitle("new to ladbrokes");
    homepage.setDescription("we will guilde you Through your first bet with us");
    homepage.setButton("start tutorial");

    // betdetails
    BetDetails betDetails = new BetDetails();
    StepContent default_bet_details_content = new StepContent();
    default_bet_details_content.setDescription("betdetails page discription");
    default_bet_details_content.setTitle("Betdetails");

    StepContent cashout_bet_details_content = new StepContent();
    cashout_bet_details_content.setDescription("cashout page discription");
    cashout_bet_details_content.setTitle("BETDETAILS CASHOUT");

    betDetails.setCashOut(cashout_bet_details_content);
    betDetails.setDefaultContent(default_bet_details_content);
    // placeBet
    PlaceBet placeBet = new PlaceBet();
    StepContent default_place_bet_content = new StepContent();

    default_place_bet_content.setDescription("BetPlaced discription");
    default_place_bet_content.setTitle("Bet placed title");

    StepContent boost_bet_details_content = new StepContent();
    boost_bet_details_content.setDescription("boost page discription");
    boost_bet_details_content.setTitle("PlaceBet Boost");

    placeBet.setBoost(boost_bet_details_content);
    placeBet.setDefaultContent(default_place_bet_content);

    // betSlip
    BetSlip betSlip = new BetSlip();
    StepContent default_betSlip_content = new StepContent();

    default_betSlip_content.setDescription("bet slip  discription");
    default_betSlip_content.setTitle("BET SLIP");

    StepContent boost_bet_Slip_content = new StepContent();
    boost_bet_Slip_content.setDescription("boost page discription");
    boost_bet_Slip_content.setTitle("PlaceBet Boost");

    betSlip.setBoost(boost_bet_Slip_content);
    betSlip.setDefaultContent(default_betSlip_content);
    // MyBets
    MyBets myBets = new MyBets();

    StepContent default_myBets_content = new StepContent();
    default_myBets_content.setTitle("MYBETS");
    default_myBets_content.setDescription("my bets discription");

    StepContent cashout_myBets_content = new StepContent();
    cashout_myBets_content.setTitle("CashOut");
    cashout_myBets_content.setDescription("cashout my bets discription");

    myBets.setDefaultContent(default_myBets_content);
    myBets.setCashOut(cashout_myBets_content);
    myBets.setButtonDesc("OK THANKS!");

    StepContent betPlace_winAlert_content = new StepContent();
    betPlace_winAlert_content.setTitle("CashOut");
    betPlace_winAlert_content.setDescription("cashout my bets discription");

    StepContent betPlacedefault_content = new StepContent();
    betPlacedefault_content.setTitle("CashOut");
    betPlacedefault_content.setDescription("cashout my bets discription");

    BetPlace betPlace = new BetPlace();

    betPlace.setDefaultContent(betPlacedefault_content);
    betPlace.setWinAlert(betPlace_winAlert_content);
    betPlace.setButtonDesc("ok");

    firstBetPlaceTutorial.setModuleName("FirstBet");
    firstBetPlaceTutorial.setModuleDiscription("firstBetDetails");
    firstBetPlaceTutorial.setDisplayFrom(Instant.now());
    firstBetPlaceTutorial.setDisplayTo(Instant.now());
    firstBetPlaceTutorial.setBrand("ladbrokes");
    firstBetPlaceTutorial.setIsEnable(true);

    firstBetPlaceTutorial.setButton(btx);
    firstBetPlaceTutorial.setHomePage(homepage);
    firstBetPlaceTutorial.setPickYourBet(pickurbet);
    firstBetPlaceTutorial.setPlaceYourBet(placeBet);
    firstBetPlaceTutorial.setBetPlaced(betPlace);
    firstBetPlaceTutorial.setMyBets(myBets);
    firstBetPlaceTutorial.setBetDetails(betDetails);
    firstBetPlaceTutorial.setBetSlip(betSlip);
    firstBetPlaceTutorial.setAddSelection(addToBetSlip);
    return firstBetPlaceTutorial;
  }
}
