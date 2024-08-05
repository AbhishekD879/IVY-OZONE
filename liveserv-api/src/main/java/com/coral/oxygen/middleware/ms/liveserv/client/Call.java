package com.coral.oxygen.middleware.ms.liveserv.client;

import com.coral.oxygen.middleware.ms.liveserv.exceptions.ServiceException;
import java.io.IOException;

public interface Call {

  String execute(String request) throws IOException, InterruptedException, ServiceException;
}
