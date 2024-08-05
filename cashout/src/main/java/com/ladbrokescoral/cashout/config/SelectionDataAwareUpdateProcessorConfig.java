package com.ladbrokescoral.cashout.config;

import com.ladbrokescoral.cashout.converter.BetToCashoutOfferRequestConverter;
import com.ladbrokescoral.cashout.model.safbaf.Event;
import com.ladbrokescoral.cashout.model.safbaf.Market;
import com.ladbrokescoral.cashout.model.safbaf.Selection;
import com.ladbrokescoral.cashout.repository.SelectionPriceRepository;
import com.ladbrokescoral.cashout.service.updates.AsyncBetDetailService;
import com.ladbrokescoral.cashout.service.updates.AsyncCashoutOfferService;
import com.ladbrokescoral.cashout.service.updates.CashoutService;
import com.ladbrokescoral.cashout.service.updates.SafUpdateApplier;
import com.ladbrokescoral.cashout.service.updates.SelectionDataAwareUpdateProcessor;
import com.ladbrokescoral.cashout.service.updates.UserUpdateTrigger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SelectionDataAwareUpdateProcessorConfig {

  @Autowired
  @Qualifier("kafka-bet-details")
  private AsyncBetDetailService betDetailService;

  @Autowired
  @Qualifier("compositeCashoutSuspensionTrigger")
  private UserUpdateTrigger userUpdateTrigger;

  @Autowired private SelectionPriceRepository selectionPriceRepository;

  @Autowired
  @Qualifier("cashoutOfferProxy")
  private AsyncCashoutOfferService asyncCashoutOfferService;

  @Autowired private BetToCashoutOfferRequestConverter converter;

  @Value("${cashout.scheduler.bet-detail.cpu.factor:1}")
  private int cpuFactor;

  @Value("${cashout.allowed.suspended.markets}")
  private String[] twoUpMarkets;

  @Autowired private CashoutService cashoutOfferService;

  @Bean
  public SelectionDataAwareUpdateProcessor<Selection> selectionSelectionDataAwareUpdateProcessor(
      SafUpdateApplier<Selection> updateApplier) {
    return new SelectionDataAwareUpdateProcessor<>(
        updateApplier,
        userUpdateTrigger,
        selectionPriceRepository,
        converter,
        cpuFactor,
        cashoutOfferService,
        twoUpMarkets);
  }

  @Bean
  public SelectionDataAwareUpdateProcessor<Market> marketSelectionDataAwareUpdateProcessor(
      SafUpdateApplier<Market> updateApplier) {
    return new SelectionDataAwareUpdateProcessor<>(
        updateApplier,
        userUpdateTrigger,
        selectionPriceRepository,
        converter,
        cpuFactor,
        cashoutOfferService,
        twoUpMarkets);
  }

  @Bean
  public SelectionDataAwareUpdateProcessor<Event> eventSelectionDataAwareUpdateProcessor(
      SafUpdateApplier<Event> updateApplier) {
    return new SelectionDataAwareUpdateProcessor<>(
        updateApplier,
        userUpdateTrigger,
        selectionPriceRepository,
        converter,
        cpuFactor,
        cashoutOfferService,
        twoUpMarkets);
  }
}
