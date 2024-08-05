package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneSyc;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesSycRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesComingBackService;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesOptinEmailService;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesSycService;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(value = {FanzonesSycService.class, FanzonesSycApi.class})
@AutoConfigureMockMvc(addFilters = false)
public class FanzonesSycApiTest extends AbstractControllerTest {

  private FanzoneSyc fanzoneSyc;

  @MockBean FanzonesSycRepository fanzonesSycRepository;
  @Autowired FanzonesSycService fanzonesSycService;
  @MockBean FanzonesComingBackService fanzonesComingBackService;
  @MockBean FanzonesOptinEmailService fanzonesOptinEmailService;

  @Before
  public void init() {
    fanzoneSyc = createFanzoneSyc();
    fanzonesSycService =
        new FanzonesSycService(
            fanzonesSycRepository, fanzonesComingBackService, fanzonesOptinEmailService);
    given(fanzonesSycRepository.findAllByBrandAndPageName(anyString(), anyString()))
        .willReturn(Optional.of(fanzoneSyc));
  }

  @Test
  public void testToReadFanzoneSyc() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/fanzone-syc")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private static FanzoneSyc createFanzoneSyc() {
    FanzoneSyc entity = new FanzoneSyc();
    entity.setId("61a07854cf77d75281e83733");
    entity.setBrand("ladbrokes");
    entity.setPageName("fanzone-syc");
    entity.setSycTitle("abc");
    entity.setSycPopUpTitle("welcome to fanzonesyc");
    entity.setSycDescription("show your colors");
    entity.setSycPopUpDescription("select your team");
    entity.setSycImage("www.assest.com");
    entity.setOkCTA("12");
    entity.setRemindLater("YES");
    entity.setRemindLaterHideDays("25");
    entity.setDontShowAgain("yes");
    entity.setSeasonStartDate(Instant.now().plus(5, ChronoUnit.DAYS));
    entity.setSeasonEndDate(Instant.now().plus(6, ChronoUnit.DAYS));
    entity.setCustomTeamNameText("Manchester");
    entity.setSycConfirmCTA("ok");
    entity.setSycChangeCTA("change team");
    entity.setSycExitCTA("exit");
    entity.setThankYouMsg("thankyou message");
    entity.setChangeTeamTimePeriodMsg("can change team time period");
    entity.setDaysToChangeTeam(15);
    entity.setSycLoginCTA("LOGIN");
    entity.setSycConfirmTitle("TEAM CONFIRMATION");
    entity.setSycThankYouTitle("THANK YOU");
    entity.setRelegatedSycTitle("Welcome to fanzone");
    entity.setRelegatedSycDescription("Relegated teams description");
    entity.setSycPreLoginTeamSelectionMsg(
        "You need to be logged in to proceed. Please LOG IN via the button below to proceed with choosing your favourite team.");
    entity.setSycPreLoginNoTeamSelectionMsg(
        "You need to be logged in to proceed. Please LOG IN via the button below to proceed with telling us who is your favourite team.");
    entity.setSycConfirmMsgMobile(
        "By CONFIRMING that you are a supporter of ${team} you will not be able to change your team for another ${days} days. On the next screen you can tell us which FANZONE notifications you want to receive");
    entity.setSycConfirmMsgDesktop(
        "Are you sure? By CONFIRMING that you are a supporter of ${team}  you will not be able to change your team for another ${days} days. FANZONE notifications are unavailable on desktop; head over to our app to receive notifications of offers, team news and live updates.");
    entity.setSycNoTeamSelectionTitle("I DON’T SUPPORT ANY OF THESE TEAMS");
    return entity;
  }
}
