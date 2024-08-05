package com.coral.oxygen.middleware.ms.liveserv.impl;

import static com.coral.oxygen.middleware.ms.liveserv.model.ChannelType.valueOf;

import com.coral.oxygen.middleware.ms.liveserv.exceptions.ServiceException;
import com.coral.oxygen.middleware.ms.liveserv.model.ChannelType;
import java.util.Objects;

/** Created by azayats on 08.05.17. */
public class BaseEventIdResolver implements EventIdResolver {

  @Override
  public long resolveEventId(String channel) throws ServiceException {
    ChannelType type;
    long id;
    Objects.requireNonNull(channel);
    try {
      type = valueOf(channel.substring(0, 6));
      String idStr = channel.substring(6, 16);
      id = Long.parseLong(idStr);
    } catch (Exception e) {
      throw new IllegalArgumentException(e);
    }
    switch (type) {
      case sEVENT:
      case SEVENT:
      case sSCBRD:
      case sCLOCK:
      case sICENT:
        return id;
      default:
        return resolve(type, id);
    }
  }

  protected long resolve(ChannelType type, long id) throws ServiceException {
    throw new ServiceException("Unsupported channel type " + type);
  }
}
