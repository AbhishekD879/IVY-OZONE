package com.coral.oxygen.middleware.ms.quickbet.converter;

import com.entain.oxygen.bettingapi.model.bet.api.request.BetRef;
import io.vavr.collection.List;

public interface PlaceBetResponseAdapter {

  boolean allFinished();

  boolean isOverask();

  boolean isBetInRun();

  Object getResponse();

  String getConfirmationExpectedAt();

  String getProvider();

  List<Long> getIds();

  List<BetRef> getBetsToRead();
}
