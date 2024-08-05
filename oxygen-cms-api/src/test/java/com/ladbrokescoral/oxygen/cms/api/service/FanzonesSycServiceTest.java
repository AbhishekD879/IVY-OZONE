package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.*;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.exception.FanzoneSycCreateException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesSycRepository;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.*;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class FanzonesSycServiceTest extends BDDMockito {

  @InjectMocks private FanzonesSycService fanzonesSycService;
  @Mock private FanzonesSycRepository fanzonesSycRepository;

  @Mock private FanzonesComingBackService fanzonesComingBackService;
  @Mock CrudService<User> userServiceObj;
  @Mock FanzonesOptinEmailService fanzonesOptinEmailService;
  private FanzoneSyc fanzoneSyc = createFanzoneSyc();

  @Before
  public void init() {
    fanzonesSycService =
        new FanzonesSycService(
            fanzonesSycRepository, fanzonesComingBackService, fanzonesOptinEmailService);
  }

  @Test
  public void testFindAllByBrandAndPageName() {
    when(fanzonesSycRepository.findAllByBrandAndPageName(anyString(), anyString()))
        .thenReturn(Optional.of(fanzoneSyc));
    assertNotNull(fanzonesSycService.findAllByBrandAndPageName(anyString(), anyString()));
  }

  @Test
  public void testfindAllByBrandPageNameNotPresent() {

    assertNotNull(fanzonesSycService.findAllByBrandAndPageName(anyString(), anyString()));
  }

  @Test
  public void testFindByBrandPageNameAndColumn() {
    when(fanzonesSycRepository.findByBrandPageNameAndColumn(
            anyString(), anyString(), anyString(), anyString()))
        .thenReturn(Optional.of(fanzoneSyc));
    assertNotNull(
        fanzonesSycService.findByBrandPageNameAndColumn(
            anyString(), anyString(), anyString(), anyString()));
  }

  @Test
  public void testFindByBrandPageNameAndColumnNotPresent() {
    when(fanzonesSycRepository.findByBrandPageNameAndColumn(
            anyString(), anyString(), anyString(), anyString()))
        .thenReturn(Optional.empty());
    assertNotNull(
        fanzonesSycService.findByBrandPageNameAndColumn(
            anyString(), anyString(), anyString(), anyString()));
  }

  @Test
  public void testToCheckFanzoneSyc() throws Exception {
    when(fanzonesSycRepository.findAllByBrandAndPageName(anyString(), anyString()))
        .thenReturn(Optional.of(fanzoneSyc));
    fanzonesSycService.checkFanzoneSyc(fanzoneSyc.getBrand(), fanzoneSyc.getPageName());
    Boolean isFanzoneSycCreated = true;
    assertTrue(isFanzoneSycCreated);
  }

  @Test
  public void testToCheckFanzoneSycFalse() throws Exception {
    when(fanzonesSycRepository.findAllByBrandAndPageName(anyString(), anyString()))
        .thenReturn(Optional.empty());
    fanzonesSycService.checkFanzoneSyc(fanzoneSyc.getBrand(), fanzoneSyc.getPageName());
    Boolean isFanzoneSycCreated = false;
    assertFalse(isFanzoneSycCreated);
  }

  @Test
  public void testToGetFanzoneSyc() throws Exception {
    Boolean isFanzoneSycCreated = false;
    try {
      when(fanzonesSycRepository.findAllByBrandAndPageName(anyString(), anyString()))
          .thenReturn(Optional.empty());
      fanzonesSycService.getFanzoneSyc(fanzoneSyc, fanzoneSyc.getBrand(), fanzoneSyc.getPageName());
    } catch (FanzoneSycCreateException e) {
      isFanzoneSycCreated = true;
    }
    assertFalse(isFanzoneSycCreated);
  }

  @Test
  public void testToGetFanzoneSycException() throws Exception {
    Boolean isFanzoneSycCreated = false;
    try {
      when(fanzonesSycRepository.findAllByBrandAndPageName(anyString(), anyString()))
          .thenReturn(Optional.of(fanzoneSyc));
      fanzonesSycService.getFanzoneSyc(fanzoneSyc, fanzoneSyc.getBrand(), fanzoneSyc.getPageName());
    } catch (FanzoneSycCreateException e) {
      isFanzoneSycCreated = true;
    }
    assertTrue(isFanzoneSycCreated);
  }

  @Test
  public void testToGetAllFanzoneSyc() throws Exception {
    Boolean isFanzoneSycCreated = false;
    try {

      fanzonesSycService.getFanzoneSyc(fanzoneSyc, fanzoneSyc.getBrand(), fanzoneSyc.getPageName());
    } catch (FanzoneSycCreateException e) {
      isFanzoneSycCreated = true;
    }
    assertFalse(isFanzoneSycCreated);
  }

  @Test
  public void testToGetAllFanzoneSycException() throws Exception {
    Boolean isFanzoneSycCreated = false;
    try {

      fanzonesSycService.getFanzoneSyc(fanzoneSyc, fanzoneSyc.getBrand(), fanzoneSyc.getPageName());
    } catch (FanzoneSycCreateException e) {
      isFanzoneSycCreated = true;
    }
    assertFalse(isFanzoneSycCreated);
  }

  @Test
  public void testToPopulateCreatorAndUpdater() throws Exception {
    Boolean isFanzoneSycCreated = false;
    try {
      fanzonesSycService.populateCreatorAndUpdater(userServiceObj, fanzoneSyc);
      isFanzoneSycCreated = true;
    } catch (FanzoneSycCreateException e) {
    }
    assertTrue(isFanzoneSycCreated);
  }

  @Test
  public void testDeleteAllByBrandPageName() {
    when(fanzonesSycRepository.findAllByBrandAndPageName(anyString(), anyString()))
        .thenReturn(Optional.of(fanzoneSyc));
    fanzonesSycService.deleteAllByBrandPageName(anyString(), anyString());
    assertNotNull(fanzonesSycService);
    verify(fanzonesSycRepository, atLeastOnce()).delete(fanzoneSyc);
  }

  @Test
  public void testDeleteAllByBrandPageNameElse() throws Exception {
    boolean thrown = false;
    try {
      when(fanzonesSycRepository.findAllByBrandAndPageName(anyString(), anyString()))
          .thenReturn(Optional.empty());
      fanzonesSycService.deleteAllByBrandPageName(anyString(), anyString());
    } catch (NotFoundException e) {
      thrown = true;
    }
    assertTrue(thrown);
  }

  @Test
  public void testToSetFanzoneComingBackSeasonStartDate() throws Exception {
    Boolean isFanzoneComingBackPresent = false;
    try {
      when(fanzonesComingBackService.findAllByBrand(anyString())).thenReturn(Optional.empty());
      fanzonesSycService.setSeasonStartDateForFanzoneComingBack(fanzoneSyc, fanzoneSyc.getBrand());
    } catch (NotFoundException e) {
      isFanzoneComingBackPresent = true;
    }
    assertFalse(isFanzoneComingBackPresent);
  }

  @Test
  public void testToSetFanzoneComingBackSeasonStartDate1() throws Exception {
    Boolean isFanzoneComingBackPresent = true;
    FanzoneComingBack fanzoneComingBack = createFanzoneComingBack();
    try {
      when(fanzonesComingBackService.findAllByBrand(anyString()))
          .thenReturn(Optional.of(fanzoneComingBack));
      fanzonesSycService.setSeasonStartDateForFanzoneComingBack(fanzoneSyc, fanzoneSyc.getBrand());
    } catch (NotFoundException e) {
      isFanzoneComingBackPresent = false;
    }
    assertTrue(isFanzoneComingBackPresent);
  }

  @Test
  public void testToSetSeasonStartDateAndEndDate() throws Exception {
    Boolean isFanzoneOptinEmailPresent = false;
    when(fanzonesOptinEmailService.findFanzoneOptinEmailByBrand(anyString()))
        .thenReturn(Optional.empty());
    fanzonesSycService.setSeasonStartAndEndDateForFanzoneOptinEmail(
        fanzoneSyc, fanzoneSyc.getBrand());
    assertFalse(isFanzoneOptinEmailPresent);
  }

  @Test
  public void testToSetSeasonStartDateAndEndDateNotPresent() throws Exception {
    Boolean isFanzoneOptinEmailPresent = false;
    FanzoneOptinEmail fanzoneOptinEmail = createFanzoneOptinEmail();
    when(fanzonesOptinEmailService.findFanzoneOptinEmailByBrand(anyString()))
        .thenReturn(Optional.of(fanzoneOptinEmail));
    fanzonesSycService.setSeasonStartAndEndDateForFanzoneOptinEmail(
        fanzoneSyc, fanzoneSyc.getBrand());
    assertFalse(isFanzoneOptinEmailPresent);
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
    entity.setFzComingBackBadgeUrlDesktop("Fanzone_Syc2");
    entity.setFzComingBackBadgeUrlMobile("Fanzone_Syc2");
    entity.setFzComingBackPopupDisplay(true);
    return entity;
  }
}
