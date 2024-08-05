package com.ladbrokescoral.cashout.config;

import com.ladbrokescoral.cashout.service.updates.UserUpdateTrigger;
import com.ladbrokescoral.cashout.service.updates.UserUpdateTriggerDto;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;

// todo get rid of it once event-stream is removed from code and only websockets are supported
@Configuration
public class CompositeCashoutSuspensionTriggerConfiguration {

  @Bean
  @Primary
  public UserUpdateTrigger compositeCashoutSuspensionTrigger(
      List<UserUpdateTrigger> userUpdateTriggers) {
    return new CompositeUserUpdateTrigger(userUpdateTriggers);
  }

  @RequiredArgsConstructor
  static class CompositeUserUpdateTrigger implements UserUpdateTrigger {
    private final List<UserUpdateTrigger> userUpdateTriggers;

    @Override
    public void triggerCashoutSuspension(UserUpdateTriggerDto suspensionDto) {
      userUpdateTriggers.forEach(t -> t.triggerCashoutSuspension(suspensionDto));
    }

    @Override
    public void triggerBetSettled(UserUpdateTriggerDto suspensionDto) {
      userUpdateTriggers.forEach(t -> t.triggerBetSettled(suspensionDto));
    }
  }
}
