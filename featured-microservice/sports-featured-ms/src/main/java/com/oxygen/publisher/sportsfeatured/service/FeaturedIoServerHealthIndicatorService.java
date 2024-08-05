package com.oxygen.publisher.sportsfeatured.service;

import com.oxygen.publisher.service.AbstractIoServerHealthIndicatorService;
import org.springframework.stereotype.Component;

@Component
public class FeaturedIoServerHealthIndicatorService extends AbstractIoServerHealthIndicatorService {

  public static final String FEATURED_QUERY_PARAMS =
      "transport=websocket&EIO=3&module=featured&sport=0";

  @Override
  protected String getQueryParams() {
    return FEATURED_QUERY_PARAMS;
  }
}
