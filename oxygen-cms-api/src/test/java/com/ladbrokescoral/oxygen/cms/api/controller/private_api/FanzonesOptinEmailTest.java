package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.mapping.FanzoneOptinEmailMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesOptinEmailRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesSycRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesOptinEmailService;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Arrays;
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
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      FanzonesOptinEmail.class,
      FanzonesOptinEmailService.class,
      FanzoneOptinEmailMapper.class,
      FanzonesOptinEmailRepository.class,
      FanzonesSycRepository.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class FanzonesOptinEmailTest extends AbstractControllerTest {
  private FanzoneOptinEmail fanzoneOptinEmail;
  private FanzoneSyc fanzoneSyc;

  @MockBean private FanzonesOptinEmailRepository fanzonesOptinEmailRepository;
  @MockBean private FanzoneOptinEmailMapper fanzoneOptinEmailMapper;
  @Autowired private FanzonesOptinEmailService fanzonesOptinEmailService;

  @MockBean private FanzonesSycRepository fanzonesSycRepository;

  @Before
  public void init() {
    fanzoneOptinEmail = createFanzoneOptinEmail();
    fanzoneSyc = createFanzoneSyc();
    given(fanzonesOptinEmailRepository.save(any(FanzoneOptinEmail.class)))
        .will(AdditionalAnswers.returnsFirstArg());
    given(fanzonesOptinEmailRepository.findFanzoneOptinEmailByBrand(anyString()))
        .willReturn(Optional.of(fanzoneOptinEmail));
    given(fanzonesSycRepository.findByBrand(anyString())).willReturn(Arrays.asList(fanzoneSyc));
  }

  @Test
  public void testToCreateFanzoneOptinEmail() throws Exception {
    given(fanzoneOptinEmailMapper.toEntity(any())).willReturn(fanzoneOptinEmail);
    given(fanzonesOptinEmailRepository.findFanzoneOptinEmailByBrand(anyString()))
        .willReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/ladbrokes/fanzones/fanzone-optin-email")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzoneOptinEmail)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToReadFanzoneOptinEmail() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/ladbrokes/fanzones/fanzone-optin-email")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToUpdateFanzoneOptinEmail() throws Exception {
    FanzoneOptinEmail fanzoneOptinEmail1 = createFanzoneOptinEmail();
    fanzoneOptinEmail1.setId("123");
    String id = "123";
    given(fanzoneOptinEmailMapper.toEntity(any())).willReturn(fanzoneOptinEmail1);
    given(fanzonesOptinEmailRepository.findFanzoneOptinEmailByBrand(anyString()))
        .willReturn(Optional.of(fanzoneOptinEmail1));
    given(fanzonesOptinEmailService.findOne(id)).willReturn(Optional.of(fanzoneOptinEmail1));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/ladbrokes/fanzones/fanzone-optin-email/123")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzoneOptinEmail1)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToDeleteFanzoneOptinEmail() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/ladbrokes/fanzones/fanzone-optin-email/123")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private static FanzoneOptinEmail createFanzoneOptinEmail() {
    FanzoneOptinEmail entity = new FanzoneOptinEmail();
    entity.setId("123");
    entity.setBrand("ladbrokes");
    entity.setFanzoneEmailPopupDescription("Abc");
    entity.setFanzoneEmailPopupDontShowThisAgain("abc");
    entity.setFanzoneEmailPopupOptIn("abc");
    entity.setFanzoneEmailPopupRemindMeLater("abc");
    entity.setFanzoneEmailPopupTitle("abc");
    return entity;
  }

  private static FanzoneSyc createFanzoneSyc() {
    FanzoneSyc entity = new FanzoneSyc();
    entity.setId("123");
    entity.setBrand("ladbrokes");
    entity.setPageName("fanzoneSyc");
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
