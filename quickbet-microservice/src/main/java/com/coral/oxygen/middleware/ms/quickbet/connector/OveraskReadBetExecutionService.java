package com.coral.oxygen.middleware.ms.quickbet.connector;

import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.configuration.OveraskReadBetConfiguration;
import com.entain.oxygen.bettingapi.model.bet.api.request.BetRef;
import com.google.common.primitives.Longs;
import io.vavr.collection.List;
import java.util.Optional;
import java.util.concurrent.Future;
import java.util.concurrent.ScheduledThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class OveraskReadBetExecutionService {
  private final ScheduledThreadPoolExecutor overaskReadBetThreadPoolExecutor;
  private final OveraskReadBetConfiguration overaskConfiguration;
  private final OveraskReadBetTaskFactory overaskReadBetTaskFactory;

  private static final Long EXTRA_DELAY_MILISECONDS = 1_000L;

  @Autowired
  public OveraskReadBetExecutionService(
      ScheduledThreadPoolExecutor scheduledThreadPoolExecutor,
      OveraskReadBetConfiguration overaskReadBetConfiguration,
      OveraskReadBetTaskFactory overaskReadBetTaskFactory) {
    this.overaskReadBetThreadPoolExecutor = scheduledThreadPoolExecutor;
    this.overaskConfiguration = overaskReadBetConfiguration;
    this.overaskReadBetTaskFactory = overaskReadBetTaskFactory;
  }

  public void scheduleReadBet(Session session, List<BetRef> betsToRead, String bppToken) {
    scheduleReadBet(session, betsToRead, bppToken, null);
  }

  public void scheduleReadBet(
      Session session, List<BetRef> betsToRead, String bppToken, String confirmationExpectedAt) {
    OveraskReadBetTask readBetTask =
        overaskReadBetTaskFactory.create(session, bppToken, betsToRead, overaskConfiguration);
    Long initialDelay = getInitialDelay(confirmationExpectedAt);
    Future readBetAsyncTask =
        overaskReadBetThreadPoolExecutor.scheduleWithFixedDelay(
            readBetTask, initialDelay, overaskConfiguration.getRetryDelay(), TimeUnit.MILLISECONDS);

    session.registerPendingTask(readBetTask.getTaskId(), readBetAsyncTask, betsToRead);
    session.save();
  }

  private Long getInitialDelay(String confirmationExpectedAt) {
    return Optional.ofNullable(confirmationExpectedAt)
        .map(Longs::tryParse)
        .map(delay -> delay * 1_000 + EXTRA_DELAY_MILISECONDS) // to miliseconds + 1 second
        .orElse(overaskConfiguration.getDefaultInitialDelay());
  }
}
