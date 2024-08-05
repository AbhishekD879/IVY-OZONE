package com.ladbrokescoral.cashout.service.updates;

import com.ladbrokescoral.cashout.model.context.UserRequestContextAccHistory;
import com.ladbrokescoral.cashout.model.safbaf.Market;
import java.util.Objects;
import org.springframework.stereotype.Component;

@Component
public class MarketUpdateApplier implements SafUpdateApplier<Market> {

  @Override
  public boolean couldChangeCashoutAvailability(
      UserRequestContextAccHistory context, Market update) {
    return update.statusChanged()
        || Objects.nonNull(update.getHandicapValue())
        || Objects.nonNull(update.getHandicapMakeup());
  }
}
