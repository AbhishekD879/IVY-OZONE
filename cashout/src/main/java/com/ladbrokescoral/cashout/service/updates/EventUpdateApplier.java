package com.ladbrokescoral.cashout.service.updates;

import com.ladbrokescoral.cashout.model.context.UserRequestContextAccHistory;
import com.ladbrokescoral.cashout.model.safbaf.Event;
import org.springframework.stereotype.Component;

@Component
public class EventUpdateApplier implements SafUpdateApplier<Event> {

  @Override
  public boolean couldChangeCashoutAvailability(
      UserRequestContextAccHistory context, Event update) {
    return update.statusChanged();
  }
}
