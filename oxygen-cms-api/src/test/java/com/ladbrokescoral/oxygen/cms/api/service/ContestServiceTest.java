package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNull;

import com.ladbrokescoral.oxygen.cms.api.dto.ContestRequest;
import com.ladbrokescoral.oxygen.cms.api.entity.Contest;
import com.ladbrokescoral.oxygen.cms.api.entity.ContestPrize;
import com.ladbrokescoral.oxygen.cms.api.repository.ContestRepository;
import com.ladbrokescoral.oxygen.cms.api.service.showdown.ShowdownService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import java.io.IOException;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
@SpringBootTest(classes = {ContestService.class})
class ContestServiceTest {

  @MockBean private ContestRepository contestsRepository;
  @MockBean private ImageService imageService;
  @MockBean private SvgImageParser svgImageParser;
  @MockBean private SiteServeService siteServeService;
  @MockBean private ShowdownService showdownService;
  @InjectMocks private ContestService contestService;
  @MockBean private ContestPrizeService contestPrizesService;

  @BeforeEach
  public void setup() throws IOException, URISyntaxException {
    MockitoAnnotations.openMocks(this);
  }

  @Test
  void testSetContestWithOfferIds() {
    Contest contest = new Contest();
    contest.setId("12345");
    assertNotNull(contestService.setContestWithOfferIds(contest));
  }

  @Test
  void testGenerateContestUrl() {

    Contest contest = new Contest();
    contest.setId("12345");
    ContestService service =
        new ContestService(
            contestsRepository,
            "",
            "",
            imageService,
            svgImageParser,
            showdownService,
            null,
            null,
            contestPrizesService);
    service.generateContestUrl(contest);
    assertNotNull(contest);
    assertNull(contest.getContestURL());
  }

  @Test
  void testGenerateContestUrlWithInvitational() {

    Contest contest = new Contest();
    contest.setId("12345");
    contest.setInvitationalContest(true);
    ContestService service =
        new ContestService(
            contestsRepository,
            "",
            "",
            imageService,
            svgImageParser,
            showdownService,
            null,
            null,
            contestPrizesService);
    service.generateContestUrl(contest);
    assertNotNull(contest);
    assertNotNull(contest.getContestURL());
  }

  @Test
  void testpopulateContestPrizes() {
    ContestRequest request = new ContestRequest();
    request.setIntialContestId("12345");
    Contest contest = new Contest();
    contest.setId("12345");
    ContestPrize contestPrize = new ContestPrize();
    contestPrize.setId("238287");
    List<ContestPrize> contestPrizes = new ArrayList<ContestPrize>();
    contestPrizes.add(contestPrize);
    Mockito.when(contestPrizesService.getByContestId(Mockito.anyString()))
        .thenReturn(contestPrizes);
    contestService.populateContestPrizes(request, contest);
    Mockito.verify(contestPrizesService).getByContestId(Mockito.anyString());
  }

  @Test
  void testpopulateContestPrizesWithEmptyPrizes() {
    ContestRequest request = new ContestRequest();
    request.setIntialContestId("12345");
    Contest contest = new Contest();
    contest.setId("12345");
    Mockito.when(contestPrizesService.getByContestId(Mockito.anyString()))
        .thenReturn(Collections.emptyList());
    contestService.populateContestPrizes(request, contest);
    Mockito.verify(contestPrizesService).getByContestId(Mockito.anyString());
  }

  @Test
  void testPrepareModelBeforeSave_error() {
    try {
      contestService.prepareModelBeforeSave(null);
    } catch (Exception e) {
      assertNotNull(e);
    }
  }
}
