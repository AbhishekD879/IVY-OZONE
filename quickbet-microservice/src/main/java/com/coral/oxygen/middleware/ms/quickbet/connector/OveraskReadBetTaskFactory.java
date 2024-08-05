package com.coral.oxygen.middleware.ms.quickbet.connector;

import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.configuration.OveraskReadBetConfiguration;
import com.coral.oxygen.middleware.ms.quickbet.converter.BetToReceiptResponseDtoConverter;
import com.coral.oxygen.middleware.ms.quickbet.converter.MultiReadBetResponseAdapterFactory;
import com.coral.oxygen.middleware.ms.quickbet.impl.SelectionOperations;
import com.entain.oxygen.bettingapi.model.bet.api.request.BetRef;
import com.entain.oxygen.bettingapi.service.BettingService;
import io.vavr.collection.List;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Component;

@Component
public class OveraskReadBetTaskFactory {

  private final SelectionOperations selectionOperations;
  private final BettingService bettingService;
  private final BetToReceiptResponseDtoConverter betToReceiptResponseDtoConverter;
  private final MultiReadBetResponseAdapterFactory multiReadBetResponseAdapterFactory;

  @Lazy // this is due to circular dependency
  public OveraskReadBetTaskFactory(
      SelectionOperations selectionOperations,
      BettingService bettingService,
      BetToReceiptResponseDtoConverter betToReceiptResponseDtoConverter,
      MultiReadBetResponseAdapterFactory multiReadBetResponseAdapterFactory) {
    this.selectionOperations = selectionOperations;
    this.bettingService = bettingService;
    this.betToReceiptResponseDtoConverter = betToReceiptResponseDtoConverter;
    this.multiReadBetResponseAdapterFactory = multiReadBetResponseAdapterFactory;
  }

  OveraskReadBetTask create(
      Session session,
      String bettingToken,
      List<BetRef> bet,
      OveraskReadBetConfiguration overaskReadBetConfiguration) {

    return new OveraskReadBetTask(
        session,
        bet,
        new BetReader(bettingToken, bettingService),
        overaskReadBetConfiguration,
        multiReadBetResponseAdapterFactory,
        new OveraskResponseFactory(session, selectionOperations, betToReceiptResponseDtoConverter));
  }
}
