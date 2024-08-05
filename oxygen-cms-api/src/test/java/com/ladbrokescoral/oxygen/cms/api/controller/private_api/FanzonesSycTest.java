package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesSycRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesComingBackService;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesOptinEmailService;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesSycService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.AdditionalAnswers;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.data.annotation.CreatedBy;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      FanzonesSyc.class,
      FanzonesSycRepository.class,
      FanzonesSycService.class,
      UserService.class,
      User.class,
      CreatedBy.class,
      Util.class,
      ModelMapper.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class FanzonesSycTest extends AbstractControllerTest {
  private FanzoneSyc fanzoneSyc;
  @MockBean FanzonesSycRepository fanzonesSycRepository;
  @MockBean ModelMapper modelMapper;

  @MockBean FanzonesComingBackService fanzonesComingBackService;

  private FanzoneComingBack fanzoneComingBack;
  @Autowired FanzonesSycService fanzonesSycService;

  @MockBean FanzonesOptinEmailService fanzonesOptinEmailService;

  private FanzoneOptinEmail fanzoneOptinEmail;

  @Before
  public void init() {
    fanzonesSycService =
        new FanzonesSycService(
            fanzonesSycRepository, fanzonesComingBackService, fanzonesOptinEmailService);
    fanzoneSyc = createFanzoneSyc();
    fanzoneComingBack = createFanzoneComingBack();
    fanzoneOptinEmail = createFanzoneOptinEmail();
    given(fanzonesSycRepository.save(any(FanzoneSyc.class)))
        .will(AdditionalAnswers.returnsFirstArg());
    given(
            fanzonesSycRepository.findByBrandPageNameAndColumn(
                anyString(), anyString(), anyString(), anyString()))
        .willReturn(Optional.of(fanzoneSyc));
    given(fanzonesSycRepository.findAllByBrandAndPageName(anyString(), anyString()))
        .willReturn(Optional.of(fanzoneSyc));
    given(fanzonesComingBackService.findAllByBrand(anyString()))
        .willReturn(Optional.of(fanzoneComingBack));
    given(fanzonesOptinEmailService.findFanzoneOptinEmailByBrand(anyString()))
        .willReturn(Optional.of(fanzoneOptinEmail));
  }

  @Test
  public void testToCreateFanzoneSyc() throws Exception {
    FanzoneSyc fanzoneSyc = createFanzoneSyc();
    given(modelMapper.map(any(), any())).willReturn(fanzoneSyc);
    given(fanzonesSycRepository.findAllByBrandAndPageName(anyString(), anyString()))
        .willReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/ladbrokes/fanzone-syc")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzoneSyc)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToCreateFanzoneSycException() throws Exception {
    FanzoneSyc fanzoneSyc = createFanzoneSyc();
    given(fanzonesSycRepository.findAllByBrandAndPageName(anyString(), anyString()))
        .willReturn(Optional.of(fanzoneSyc));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/ladbrokes/fanzone-syc")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzoneSyc)))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testToDeleteAllFanzonesSyc() throws Exception {
    given(fanzonesSycRepository.findAllByBrandAndPageName(anyString(), anyString()))
        .willReturn(Optional.of(fanzoneSyc));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/ladbrokes/fanzone-syc")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToReadFanzoneSyc() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/ladbrokes/fanzone-syc")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToUpdateFanzoneSycById() throws Exception {
    given(modelMapper.map(any(), any())).willReturn(fanzoneSyc);
    given(
            fanzonesSycRepository.findByBrandPageNameAndColumn(
                anyString(), anyString(), anyString(), anyString()))
        .willReturn(Optional.of(fanzoneSyc));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/ladbrokes/fanzonesyc/id/123")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzoneSyc)))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testToUpdateFanzoneSycById1() throws Exception {
    FanzoneSyc fanzoneSyc = createFanzoneSyc();
    fanzoneSyc.setId("123");
    given(modelMapper.map(any(), any())).willReturn(fanzoneSyc);
    given(
            fanzonesSycRepository.findByBrandPageNameAndColumn(
                anyString(), anyString(), anyString(), anyString()))
        .willReturn(Optional.of(fanzoneSyc));
    given(fanzonesSycService.findOne(anyString())).willReturn(Optional.of(fanzoneSyc));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/ladbrokes/fanzoneSyc/id/123")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzoneSyc)))
        .andExpect(status().is2xxSuccessful());
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
    entity.setCustomTeamNameDescription("Manchester city");
    entity.setSycConfirmCTA("ok");
    entity.setSycChangeCTA("change team");
    entity.setSycExitCTA("exit");
    entity.setSycCancelCTA("cancel");
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

  private static FanzoneComingBack createFanzoneComingBack() {
    FanzoneComingBack entity = new FanzoneComingBack();
    entity.setId("123");
    entity.setBrand("ladbrokes");
    entity.setFzComingBackHeading("Fanzone Coming Back");
    entity.setFzComingBackDescription("Fanzone Coming Back Pop Up Description");
    entity.setFzComingBackTitle("Fanzone Coming Back Pop Up Title");
    entity.setFzComingBackOKCTA("OK CTA");
    entity.setFzComingBackDisplayFromDays("No of days before season starts");
    entity.setFzComingBackBgImageDesktop("Fanzone_Syc2");
    entity.setFzComingBackBgImageMobile("Fanzone_Syc2");
    entity.setFzComingBackBadgeUrlDesktop("Fanzone_Syc2");
    entity.setFzComingBackBadgeUrlMobile("Fanzone_Syc2");
    entity.setFzComingBackPopupDisplay(true);
    entity.setFzSeasonStartDate(createFanzoneSyc().getSeasonStartDate());
    return entity;
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
}
