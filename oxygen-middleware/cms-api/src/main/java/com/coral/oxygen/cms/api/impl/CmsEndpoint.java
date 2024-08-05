package com.coral.oxygen.cms.api.impl;

import com.coral.oxygen.middleware.pojos.model.cms.*;
import com.coral.oxygen.middleware.pojos.model.cms.featured.ModularContent;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPage;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportsCategory;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportsQuickLink;
import com.coral.oxygen.middleware.pojos.model.output.AssetManagement;
import java.util.Collection;
import java.util.List;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Path;

/** Created by azayats on 01.11.16. */
public interface CmsEndpoint {

  @GET("modular-content")
  Call<ModularContent> getModularContent();

  @GET("system-configuration")
  Call<CmsSystemConfig> getSystemConfig();

  @GET("yc-leagues")
  Call<List<CmsYcLeague>> getYcLeagues();

  @GET("sport-quick-link")
  Call<List<SportsQuickLink>> getQuickLinks();

  @GET("sports-pages")
  Call<Collection<SportPage>> findAllPagesByBrand();

  @GET("sports-pages/{lastRunTime}")
  Call<Collection<SportPage>> findAllPagesByBrand(@Path("lastRunTime") long lastRunTime);

  @GET("sport-category")
  Call<Collection<SportsCategory>> getSportsCategories();

  @GET("inplay-data")
  Call<CmsInplayData> getInplayData();

  @GET("asset-management/brand")
  Call<Collection<AssetManagement>> getAssetManagementInfo();
  // BMA-62182: Get list for Fanzones from Oxygen-cms-api using cmsEndpoint.findAllFanzoneByBrand()
  // api request
  @GET("fanzone")
  Call<Collection<Fanzone>> findAllFanzoneByBrand();

  @GET("virtual-sports")
  Call<Collection<VirtualSportDto>> findVirtualSportsConfigs();
}
