package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertNotNull;

import com.ladbrokescoral.oxygen.cms.api.entity.ContestPrize;
import com.ladbrokescoral.oxygen.cms.api.repository.ContestPrizeRepository;
import java.io.IOException;
import java.net.URISyntaxException;
import java.util.ArrayList;
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
@SpringBootTest(classes = {ContestPrizeService.class})
class ContestPrizeServiceTest {

  @MockBean private ContestPrizeRepository contestPrizesRepository;
  @MockBean private ImageService imageService;
  @InjectMocks private ContestPrizeService contestPrizeService;
  @MockBean private SvgImageParser svgImageParser;

  @BeforeEach
  public void init() throws IOException, URISyntaxException {
    MockitoAnnotations.openMocks(this);
  }

  @Test
  void testGetByContestId_FreebetPrize() {
    Mockito.when(contestPrizesRepository.findByContestId(Mockito.any()))
        .thenReturn(getContestFreebetPrize());
    assertNotNull(contestPrizeService.getByContestId("12345"));
  }

  @Test
  void testGetByContestId_TicketPrize() {
    Mockito.when(contestPrizesRepository.findByContestId(Mockito.any()))
        .thenReturn(getContestTicketPrize());
    assertNotNull(contestPrizeService.getByContestId("12345"));
  }

  @Test
  void testGetByContestId_CashPrize() {
    Mockito.when(contestPrizesRepository.findByContestId(Mockito.any()))
        .thenReturn(getContestCashPrize());
    assertNotNull(contestPrizeService.getByContestId("12345"));
  }

  @Test
  void testGetByContestId_VocherPrize() {
    Mockito.when(contestPrizesRepository.findByContestId(Mockito.any()))
        .thenReturn(getContestVocherPrize());
    assertNotNull(contestPrizeService.getByContestId("12345"));
  }

  private List<ContestPrize> getContestFreebetPrize() {
    List<ContestPrize> contestPrizes = new ArrayList<>();
    ContestPrize contestPrize = new ContestPrize();
    contestPrize.setBrand("ladbrokes");
    contestPrize.setType("Freebet");
    contestPrize.setId("12345");
    contestPrizes.add(contestPrize);
    ContestPrize contestPrize1 = new ContestPrize();
    contestPrize1.setBrand("ladbrokes");
    contestPrize1.setType("Freebet");
    contestPrize1.setId("12345");
    contestPrize1.setFreebetOfferId("28216");
    contestPrizes.add(contestPrize);
    contestPrizes.add(contestPrize1);
    return contestPrizes;
  }

  private List<ContestPrize> getContestTicketPrize() {
    List<ContestPrize> contestPrizes = new ArrayList<>();
    ContestPrize contestPrize = new ContestPrize();
    contestPrize.setBrand("ladbrokes");
    contestPrize.setType("Ticket");
    contestPrize.setId("12345");
    ContestPrize contestPrize1 = new ContestPrize();
    contestPrize1.setBrand("ladbrokes");
    contestPrize1.setType("Ticket");
    contestPrize1.setId("12345");
    contestPrize1.setFreebetOfferId("28216");
    contestPrizes.add(contestPrize);
    contestPrizes.add(contestPrize1);
    return contestPrizes;
  }

  private List<ContestPrize> getContestCashPrize() {
    List<ContestPrize> contestPrizes = new ArrayList<>();
    ContestPrize contestPrize = new ContestPrize();
    contestPrize.setBrand("ladbrokes");
    contestPrize.setType("Cash");
    contestPrize.setId("12345");
    contestPrize.setFreebetOfferId("28216");
    contestPrizes.add(contestPrize);
    return contestPrizes;
  }

  private List<ContestPrize> getContestVocherPrize() {
    List<ContestPrize> contestPrizes = new ArrayList<>();
    ContestPrize contestPrize = new ContestPrize();
    contestPrize.setBrand("ladbrokes");
    contestPrize.setType("Vocher");
    contestPrize.setId("12345");
    contestPrize.setFreebetOfferId("28216");
    contestPrizes.add(contestPrize);
    return contestPrizes;
  }
}
