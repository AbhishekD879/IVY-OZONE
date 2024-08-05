package com.ladbrokescoral.cashout.service.updates;

import com.ladbrokescoral.cashout.model.response.UpdateDto;

public interface BetUpdatesTopic {
  void sendBetUpdate(UpdateDto betUpdate);

  void sendBetUpdate(String key, UpdateDto updateDto);

  void sendBetUpdateError(String key, Throwable ex);
}
