package com.gvc.oxygen.betreceipts.service;

import com.gvc.oxygen.betreceipts.entity.Bet;
import com.gvc.oxygen.betreceipts.repository.BetRepository;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class BetServiceTest implements WithAssertions {

  @Mock private BetRepository betRepository;

  @InjectMocks private BetService betService;

  @Test
  void testSaveMetaEvents() {
    Assertions.assertDoesNotThrow(() -> betService.updateBets(getBets()));
  }

  @Test
  void testFindAllBets() {
    Assertions.assertDoesNotThrow(() -> betService.findAllBets());
  }

  private List<Bet> getBets() {
    return Arrays.asList(createMetaEvent());
  }

  private Bet createMetaEvent() {
    Bet bet = new Bet();
    bet.setEventIds(new HashSet<>());
    bet.setUsername("test-gvc");
    return bet;
  }
}
