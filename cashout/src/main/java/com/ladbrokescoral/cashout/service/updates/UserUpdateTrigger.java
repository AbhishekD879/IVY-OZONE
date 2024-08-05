package com.ladbrokescoral.cashout.service.updates;

public interface UserUpdateTrigger {

  void triggerCashoutSuspension(UserUpdateTriggerDto suspensionDto);

  void triggerBetSettled(UserUpdateTriggerDto suspensionDto);
}
