package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.Contest;
import com.ladbrokescoral.oxygen.cms.api.entity.ContestPrize;
import com.ladbrokescoral.oxygen.cms.api.entity.PrizePool;
import com.ladbrokescoral.oxygen.cms.api.repository.ContestPrizeRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.ContestRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ContestPrizeService;
import com.ladbrokescoral.oxygen.cms.api.service.ContestService;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.api.service.SvgImageParser;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.ContestPrizePublicService;
import com.ladbrokescoral.oxygen.cms.api.service.showdown.ShowdownService;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(
    value = {
      ContestPrizeApi.class,
      ContestPrizePublicService.class,
      ContestPrizeService.class,
      ContestService.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class ContestPrizeApiTest extends AbstractControllerTest {

  @MockBean private ContestPrizeRepository repository;
  @MockBean private ImageService imageService;
  @MockBean private ShowdownService showdownService;
  @MockBean private ContestRepository contestRepository;
  @MockBean private SvgImageParser svgImageParser;

  private Contest contest;

  private List<ContestPrize> contestPrizes;

  @Before
  public void init() {
    contestPrizes = getContestPrizesForScenario1();
    contest = getContestInfo();
    given(repository.findByContestId(anyString())).willReturn(contestPrizes);
    given(contestRepository.findById(anyString())).willReturn(Optional.of(contest));
  }

  @Test
  public void testGetByContestId() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/contestprize/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(contestPrizes)))
        .andExpect(status().is2xxSuccessful());
  }

  private static List<ContestPrize> getContestPrizesForScenario1() {
    List<ContestPrize> contestPrizes = new ArrayList<>();
    ContestPrize prize = new ContestPrize();
    prize.setType("Cash");
    prize.setId("89");
    prize.setBrand("coral");
    prize.setContestId("1");
    prize.setNumberOfEntries("1");
    ContestPrize prize1 = new ContestPrize();
    prize1.setType("Cash");
    prize1.setId("2");
    prize1.setBrand("Bma");
    prize1.setContestId("1");
    prize1.setNumberOfEntries("2");
    ContestPrize prize2 = new ContestPrize();
    prize2.setType("Freebet");
    prize2.setContestId("1");
    prize2.setNumberOfEntries("1-100");
    contestPrizes.add(prize);
    contestPrizes.add(prize1);
    return contestPrizes;
  }

  private Contest getContestInfo() {
    Contest contest = new Contest();
    PrizePool prizePool = new PrizePool();
    prizePool.setCash("1000");
    contest.setPrizePool(prizePool);
    return contest;
  }
}
