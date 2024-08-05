package com.coral.oxygen.middleware.ms.liveserv.model.messages;

import com.coral.oxygen.middleware.ms.liveserv.exceptions.ServiceException;

/** Created by azayats on 08.05.17. */
public class SubscriptionError extends AbstractErrorEnvelope {

  public SubscriptionError(String channel, ServiceException ex) {
    super(EnvelopeType.SUBSCRIPTION_ERROR, channel, ex.getMessage(), ex);
  }
}
