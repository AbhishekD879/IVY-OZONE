package com.oxygen.publisher.inplay.service;

import com.oxygen.publisher.service.AbstractIoServerHealthIndicatorService;
import org.springframework.stereotype.Component;

@Component
public class InplaySocketServerHealthService extends AbstractIoServerHealthIndicatorService {

  public static final String FEATURED_QUERY_PARAMS = "transport=websocket&EIO=3";

  @Override
  protected String getQueryParams() {
    return FEATURED_QUERY_PARAMS;
  }
}
