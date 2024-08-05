package com.coral.oxygen.middleware.ms.liveserv.impl;

import com.coral.oxygen.middleware.ms.liveserv.exceptions.ServiceException;

/** Created by azayats on 08.05.17. */
public interface EventIdResolver {

  long resolveEventId(String channel) throws ServiceException;
}
