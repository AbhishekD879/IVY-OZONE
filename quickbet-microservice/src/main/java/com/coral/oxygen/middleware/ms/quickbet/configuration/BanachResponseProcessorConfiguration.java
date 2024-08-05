package com.coral.oxygen.middleware.ms.quickbet.configuration;

import com.coral.oxygen.middleware.ms.quickbet.processor.*;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class BanachResponseProcessorConfiguration {
  // Ordered chain of banach place bet processors
  private static final List<BanachResponseProcessor> chainOfProcessors =
      Arrays.asList(
          new OxiAuthProblemResponseProcessor(),
          new HighStakeErrorProcessor(),
          new EventAlreadyStartedProcessor(),
          new PlaytechAuthErrorProcessor(),
          new PriceChangeResponseProcessor(),
          new SuccessResponseProcessor(),
          new ObBetErrorResponseProcessor(),
          new DefaultErrorProcessor());

  @Bean
  public BanachResponseProcessor configBanachResponseProcessor() {
    Iterator<BanachResponseProcessor> iterator = chainOfProcessors.iterator();
    BanachResponseProcessor current = iterator.next();
    while (iterator.hasNext()) {
      BanachResponseProcessor next = iterator.next();
      current.setNextProcessor(next);
      current = next;
    }
    return chainOfProcessors.get(0);
  }
}
