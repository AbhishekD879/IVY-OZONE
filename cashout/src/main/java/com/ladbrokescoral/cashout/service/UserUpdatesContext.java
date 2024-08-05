package com.ladbrokescoral.cashout.service;

import com.ladbrokescoral.cashout.model.response.ErrorBetResponse;
import com.ladbrokescoral.cashout.model.response.UpdateBetResponse;
import com.ladbrokescoral.cashout.model.response.UpdateCashoutResponse;

public interface UserUpdatesContext {
  void sendBetUpdate(String emitKey, UpdateBetResponse updateBetResponse);

  void sendBetUpdateError(String emitKey, ErrorBetResponse errorBetResponse);

  void sendCashoutUpdate(String emitKey, UpdateCashoutResponse updateCashoutResponse);
}
