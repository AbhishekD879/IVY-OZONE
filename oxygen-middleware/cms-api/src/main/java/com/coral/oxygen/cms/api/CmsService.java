package com.coral.oxygen.cms.api;

import com.coral.oxygen.middleware.pojos.model.cms.*;
import com.coral.oxygen.middleware.pojos.model.cms.featured.ModularContent;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPage;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportsCategory;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportsQuickLink;
import com.coral.oxygen.middleware.pojos.model.output.AssetManagement;
import java.util.Collection;
import java.util.List;

public interface CmsService {

  Collection<SportPage> requestPages();

  Collection<SportPage> requestPages(long lastRunTime);

  ModularContent requestModularContent();

  List<SportsQuickLink> requestSportsQuickLink();

  CmsInplayData requestInplayData();

  CmsSystemConfig requestSystemConfig();

  List<CmsYcLeague> requestYcLeagues();

  HealthStatus getHealthStatus();

  Collection<SportsCategory> getSportsCategories();

  Collection<AssetManagement> getAssetManagementInfoByBrand();
  // BMA-62182: Get list for Fanzones from Oxygen-cms-api
  Collection<Fanzone> getFanzones();

  /**
   * Get list of virtual sports by brand
   *
   * @return
   */
  List<VirtualSportDto> getVirtualSportsByBrand();
}
