package com.coral.oxygen.middleware.ms.quickbet.connector;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.*;

import com.coral.oxygen.middleware.ms.quickbet.*;
import com.coral.oxygen.middleware.ms.quickbet.configuration.OveraskReadBetConfiguration;
import com.entain.oxygen.bettingapi.model.bet.api.request.BetRef;
import io.vavr.collection.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class OveraskReadBetTaskFactoryTest {
  @InjectMocks private OveraskReadBetTaskFactory overaskReadBetTaskFactory;

  @Test
  void create() {
    Session session = mock(Session.class);
    String bettingToken = "testBettingToken";
    List<BetRef> bet = List.of(mock(BetRef.class));
    OveraskReadBetConfiguration overaskReadBetConfiguration =
        mock(OveraskReadBetConfiguration.class);

    OveraskReadBetTask overaskReadBetTask =
        overaskReadBetTaskFactory.create(session, bettingToken, bet, overaskReadBetConfiguration);

    assertNotNull(overaskReadBetTask);
  }
}
