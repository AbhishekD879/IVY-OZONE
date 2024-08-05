package com.ladbrokescoral.oxygen.cms.api.service.siteserve;

import com.egalacoral.spark.siteserver.api.SiteServerApi;

public interface SiteServeApiProvider {

  SiteServerApi api(String brand);
}
