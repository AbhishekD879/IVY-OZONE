package com.ladbrokescoral.cashout.service.updates;

import com.ladbrokescoral.cashout.model.context.UserRequestContextAccHistory;

public interface UpdateProcessor<T> {
  void process(UserRequestContextAccHistory userRequestContext, T msg);
}
