package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.FirstBetPlaceCFDto;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CloseButton;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.FirstBetPlaceTutorial;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.StepContent;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.FirstBetPlaceTutorialService;
import java.time.Instant;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.modelmapper.ModelMapper;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;

@RunWith(Parameterized.class)
public class FirstBetPlaceAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<FirstBetPlaceTutorial> {

  @InjectMocks private FirstBetPlaceTutorialService service;
  @Getter private FirstBetPlaceAfterSaveListener listener;
  @Getter private FirstBetPlaceTutorial entity = null;
  @Getter private List<FirstBetPlaceTutorial> collection = null;
  ModelMapper mapper = new ModelMapper();

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "first-bet-place"},
          {"connect", "api/connect", "first-bet-place"}
        });
  }

  public FirstBetPlaceCFDto getModelClass() {
    return mapper.map(getEntity(), FirstBetPlaceCFDto.class);
  }

  @Before
  public void init() {
    entity = createEntity();
    service = new FirstBetPlaceTutorialService(null, mapper, null, null, null);
    listener = new FirstBetPlaceAfterSaveListener(service, context);
  }

  @Test
  public void shouldAfterSaveEvent() throws Exception {

    // given
    entity.setBrand(brand);

    // when
    this.getListener().onAfterSave(new AfterSaveEvent<FirstBetPlaceTutorial>(entity, null, "11"));

    then(context).should().upload(brand, path, filename, getModelClass());
  }

  @After
  public void shouldHaveNoMoreInteractions() {
    then(context).shouldHaveNoMoreInteractions();
  }

  private FirstBetPlaceTutorial createEntity() {

    FirstBetPlaceTutorial FirstBetPlaceTutorial = new FirstBetPlaceTutorial();
    CloseButton btx = new CloseButton();
    btx.setDescription("DON'T NEED HELP");
    btx.setTitle("rember you can find your ttrls in my account");
    btx.setLeftButtonDesc("undo");
    btx.setRightButtonDesc("GOT IT");

    StepContent adBetSlip = new StepContent();
    adBetSlip.setDescription("Add the bet to BetSlip");
    adBetSlip.setTitle("Add selection");

    StepContent pickurbet = new StepContent();
    pickurbet.setDescription("pick the bet");
    pickurbet.setTitle("Pick UR Bet");

    FirstBetPlaceTutorial.HomePage homepage = new FirstBetPlaceTutorial.HomePage();
    homepage.setTitle("new to ladbrokes");
    homepage.setDescription("we will guilde you Through your first bet with us");
    homepage.setButton("start tutorial");

    // betdetails
    FirstBetPlaceTutorial.BetDetails betDetails = new FirstBetPlaceTutorial.BetDetails();
    StepContent default_bet_details_content = new StepContent();
    default_bet_details_content.setDescription("betdetails page discription");
    default_bet_details_content.setTitle("Betdetails");

    StepContent cashout_bet_details_content = new StepContent();
    cashout_bet_details_content.setDescription("cashout page discription");
    cashout_bet_details_content.setTitle("BETDETAILS CASHOUT");

    betDetails.setCashOut(cashout_bet_details_content);
    betDetails.setDefaultContent(default_bet_details_content);
    // placeBet
    FirstBetPlaceTutorial.PlaceBet placeBet = new FirstBetPlaceTutorial.PlaceBet();
    StepContent default_place_bet_content = new StepContent();

    default_place_bet_content.setDescription("BetPlaced discription");
    default_place_bet_content.setTitle("Bet placed title");

    StepContent boost_bet_details_content = new StepContent();
    boost_bet_details_content.setDescription("boost page discription");
    boost_bet_details_content.setTitle("PlaceBet Boost");

    placeBet.setBoost(boost_bet_details_content);
    placeBet.setDefaultContent(default_place_bet_content);

    // betSlip
    FirstBetPlaceTutorial.BetSlip betSlip = new FirstBetPlaceTutorial.BetSlip();
    StepContent default_betSlip_content = new StepContent();

    default_betSlip_content.setDescription("bet slip  discription");
    default_betSlip_content.setTitle("BET SLIP");

    StepContent boost_bet_Slip_content = new StepContent();
    boost_bet_Slip_content.setDescription("boost page discription");
    boost_bet_Slip_content.setTitle("PlaceBet Boost");

    betSlip.setBoost(boost_bet_Slip_content);
    betSlip.setDefaultContent(default_betSlip_content);
    // MyBets
    FirstBetPlaceTutorial.MyBets myBets = new FirstBetPlaceTutorial.MyBets();

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

    FirstBetPlaceTutorial.BetPlace betPlace = new FirstBetPlaceTutorial.BetPlace();

    betPlace.setDefaultContent(betPlacedefault_content);
    betPlace.setWinAlert(betPlace_winAlert_content);
    betPlace.setButtonDesc("ok");

    FirstBetPlaceTutorial.setModuleName("FirstBet");
    FirstBetPlaceTutorial.setModuleDiscription("firstBetDetails");
    FirstBetPlaceTutorial.setDisplayFrom(Instant.now());
    FirstBetPlaceTutorial.setDisplayTo(Instant.now());
    FirstBetPlaceTutorial.setBrand(brand);
    FirstBetPlaceTutorial.setIsEnable(true);

    FirstBetPlaceTutorial.setButton(btx);
    FirstBetPlaceTutorial.setHomePage(homepage);
    FirstBetPlaceTutorial.setPickYourBet(pickurbet);
    FirstBetPlaceTutorial.setPlaceYourBet(placeBet);
    FirstBetPlaceTutorial.setBetPlaced(betPlace);
    FirstBetPlaceTutorial.setMyBets(myBets);
    FirstBetPlaceTutorial.setBetDetails(betDetails);
    FirstBetPlaceTutorial.setBetSlip(betSlip);
    FirstBetPlaceTutorial.setAddSelection(adBetSlip);
    return FirstBetPlaceTutorial;
  }
}
