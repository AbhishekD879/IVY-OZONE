package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneComingBack;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneSyc;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesComingBackRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesSycRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesComingBackService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Arrays;
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
      FanzonesComingBackController.class,
      FanzonesComingBackRepository.class,
      FanzonesComingBackService.class,
      UserService.class,
      User.class,
      CreatedBy.class,
      Util.class,
      ModelMapper.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class FanzonesComingBackTest extends AbstractControllerTest {

  private FanzoneComingBack fanzoneComingBack;
  private FanzoneSyc fanzoneSyc;

  @MockBean FanzonesComingBackRepository fanzonesComingBackRepository;
  @MockBean ModelMapper modelMapper;
  @Autowired FanzonesComingBackService fanzonesComingBackService;

  @MockBean private FanzonesSycRepository fanzonesSycRepository;

  @Before
  public void init() {
    fanzoneComingBack = createFanzoneComingBack();
    fanzoneSyc = createFanzoneSyc();

    given(fanzonesComingBackRepository.save(any(FanzoneComingBack.class)))
        .will(AdditionalAnswers.returnsFirstArg());
    given(fanzonesComingBackRepository.findAllByBrand(anyString()))
        .willReturn(Optional.of(fanzoneComingBack));
    given(fanzonesComingBackRepository.findAllByBrandAndId(anyString(), anyString()))
        .willReturn(Optional.of(fanzoneComingBack));
    given(fanzonesSycRepository.findByBrand(anyString())).willReturn(Arrays.asList(fanzoneSyc));
  }

  @Test
  public void testToCreateFanzoneComingBack() throws Exception {
    FanzoneComingBack fanzoneComingBack = createFanzoneComingBack();
    given(modelMapper.map(any(), any())).willReturn(fanzoneComingBack);
    given(fanzonesComingBackRepository.findAllByBrand(anyString())).willReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/ladbrokes/fanzone-coming-back")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzoneComingBack)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToCreateFanzoneComingBackException() throws Exception {
    FanzoneComingBack fanzoneComingBack = createFanzoneComingBack();
    given(fanzonesComingBackRepository.findAllByBrand(anyString()))
        .willReturn(Optional.of(fanzoneComingBack));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/ladbrokes/fanzone-coming-back")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzoneComingBack)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testToDeleteAllFanzoneComingBack() throws Exception {
    given(fanzonesComingBackRepository.findAllByBrand(anyString()))
        .willReturn(Optional.of(fanzoneComingBack));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/ladbrokes/fanzone-coming-back")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToReadFanzoneComingBack() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/ladbrokes/fanzone-coming-back")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToUpdateFanzoneComingBackById() throws Exception {
    given(modelMapper.map(any(), any())).willReturn(fanzoneComingBack);
    given(fanzonesComingBackRepository.findAllByBrandAndId(anyString(), anyString()))
        .willReturn(Optional.of(fanzoneComingBack));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/ladbrokes/fanzone-coming-back/id/123")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzoneComingBack)))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testToUpdateFanzoneComingBackById1() throws Exception {
    FanzoneComingBack fanzoneComingBack = createFanzoneComingBack();
    fanzoneComingBack.setId("123");
    given(modelMapper.map(any(), any())).willReturn(fanzoneComingBack);
    given(fanzonesComingBackRepository.findAllByBrandAndId(anyString(), anyString()))
        .willReturn(Optional.of(fanzoneComingBack));
    given(fanzonesComingBackService.findOne(anyString()))
        .willReturn(Optional.of(fanzoneComingBack));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/ladbrokes/fanzone-coming-back/id/123")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzoneComingBack)))
        .andExpect(status().is2xxSuccessful());
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
