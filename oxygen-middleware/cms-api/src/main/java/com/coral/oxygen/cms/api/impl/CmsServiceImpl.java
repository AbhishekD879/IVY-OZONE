package com.coral.oxygen.cms.api.impl;

import com.coral.oxygen.cms.api.CmsService;
import com.coral.oxygen.cms.api.HealthStatus;
import com.coral.oxygen.middleware.JsonFacade;
import com.coral.oxygen.middleware.RuntimeTypeAdapterFactory;
import com.coral.oxygen.middleware.pojos.model.cms.*;
import com.coral.oxygen.middleware.pojos.model.cms.featured.*;
import com.coral.oxygen.middleware.pojos.model.output.AssetManagement;
import com.fatboyindustrial.gsonjodatime.Converters;
import com.google.gson.JsonSyntaxException;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Trace;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import okhttp3.OkHttpClient;
import retrofit2.Call;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

@Slf4j
public class CmsServiceImpl implements CmsService {

  private static final RuntimeTypeAdapterFactory typeAdapter =
      RuntimeTypeAdapterFactory.of(SportPageModuleDataItem.class)
          .registerSubtype(ModularContentItem.class, "FEATURED")
          .registerSubtype(
              CommonModule.class,
              "COMMON_MODULE") // TODO: legacy structure, good place for refactoring
          .registerSubtype(SportsQuickLink.class, "QUICK_LINK")
          .registerSubtype(RecentlyPlayedGame.class, "RECENTLY_PLAYED_GAMES")
          .registerSubtype(InPlayConfig.class, "IN_PLAY")
          .registerSubtype(SurfaceBet.class, "SURFACE_BET")
          .registerSubtype(HighlightCarousel.class, "HIGHLIGHTS_CAROUSEL")
          .registerSubtype(AemBannersConfig.class, "AEM_BANNERS")
          .registerSubtype(CmsRacingModule.class, "RACING_MODULE")
          .registerSubtype(TeamBets.class, "BETS_BASED_ON_YOUR_TEAM")
          .registerSubtype(FanBets.class, "BETS_BASED_ON_OTHER_FANS")
          .registerSubtype(VirtualEvent.class, "VIRTUAL_NEXT_EVENTS")
          .registerSubtype(PopularBet.class, "POPULAR_BETS")
          .registerSubtype(BybWidget.class, "BYB_WIDGET")
          .registerSubtype(LuckyDip.class, "LUCKY_DIP")
          .registerSubtype(SuperButton.class, "SUPER_BUTTON")
          .registerSubtype(PopularAccaWidget.class, "POPULAR_ACCA");

  private CmsEndpoint cmsEndpoint;

  private HealthStatus healthStatus = HealthStatus.OK;

  private class CMSApiException extends RuntimeException {

    CMSApiException(Throwable t) {
      super(t);
    }

    CMSApiException(String msg) {
      super(msg);
    }
  }

  public CmsServiceImpl(String baseUrl, OkHttpClient okHttpClient) {
    cmsEndpoint =
        new Retrofit.Builder()
            .baseUrl(baseUrl)
            .client(okHttpClient)
            .addConverterFactory(
                GsonConverterFactory.create(
                    Converters.registerDateTime(
                            JsonFacade.GSON_BUILDER.registerTypeAdapterFactory(typeAdapter))
                        .create()))
            .build()
            .create(CmsEndpoint.class);
  }

  @Trace(dispatcher = true)
  @Override
  public Collection<SportPage> requestPages() {
    try {
      final String transactionName = "/sports-pages";
      NewRelic.setTransactionName(null, transactionName);
      Collection<SportPage> sportsPages =
          executeRequest(cmsEndpoint.findAllPagesByBrand()).orElse(Collections.emptyList());
      setHealthOK();
      return sportsPages;
    } catch (IOException e) {
      setHealthFail();
      NewRelic.noticeError(e);
      return Collections.emptyList();
    }
  }

  public Collection<SportPage> requestPages(long lastRunTime) {
    try {
      final String transactionName = "/sports-pages";
      NewRelic.setTransactionName(null, transactionName);
      Collection<SportPage> sportsPages =
          executeRequest(cmsEndpoint.findAllPagesByBrand(lastRunTime))
              .orElse(Collections.emptyList());
      setHealthOK();
      return sportsPages;
    } catch (IOException e) {
      setHealthFail();
      NewRelic.noticeError(e);
      return Collections.emptyList();
    }
  }

  @Trace(dispatcher = true)
  @Override
  public ModularContent requestModularContent() {
    try {
      final String transactionName = "/modular-content";
      NewRelic.setTransactionName(null, transactionName);
      ModularContent modularContent =
          executeRequest(cmsEndpoint.getModularContent())
              .orElseThrow(() -> new CMSApiException("Failed to retrieve modular-content"));
      setHealthOK();
      return modularContent;
    } catch (IOException e) {
      setHealthFail();
      NewRelic.noticeError(e);
      throw new CMSApiException(e);
    }
  }

  @Trace(dispatcher = true)
  @Override
  public List<SportsQuickLink> requestSportsQuickLink() {
    try {
      final String transactionName = "/sport-quick-link";
      NewRelic.setTransactionName(null, transactionName);
      List<SportsQuickLink> quickLinks =
          executeRequest(cmsEndpoint.getQuickLinks()).orElse(Collections.emptyList());
      setHealthOK();
      return quickLinks;
    } catch (IOException e) {
      setHealthFail();
      NewRelic.noticeError(e);
      return Collections.emptyList();
    }
  }

  @Trace(dispatcher = true)
  @Override
  public CmsInplayData requestInplayData() {
    try {
      final String transactionName = "/inplay-data";
      NewRelic.setTransactionName(null, transactionName);
      CmsInplayData cmsInplayData =
          executeRequest(cmsEndpoint.getInplayData())
              .orElseThrow(() -> new CMSApiException("Failed to retrieve /inplay-data"));
      setHealthOK();
      return cmsInplayData;
    } catch (IOException e) {
      setHealthFail();
      NewRelic.noticeError(e);
      throw new CMSApiException(e);
    }
  }

  @Trace(dispatcher = true)
  @Override
  public CmsSystemConfig requestSystemConfig() {
    try {
      final String transactionName = "/system-configuration";
      NewRelic.setTransactionName(null, transactionName);
      CmsSystemConfig cmsSystemConfig =
          executeRequest(cmsEndpoint.getSystemConfig()).orElse(new CmsSystemConfig());
      setHealthOK();
      return cmsSystemConfig;
    } catch (IOException | JsonSyntaxException e) {
      setHealthFail();
      NewRelic.noticeError(e);
      log.error("Unable parse CMS config", e);
      return new CmsSystemConfig();
    }
  }

  @Trace(dispatcher = true)
  @Override
  public List<CmsYcLeague> requestYcLeagues() {
    try {
      final String transactionName = "/yc-leagues";
      NewRelic.setTransactionName(null, transactionName);
      List<CmsYcLeague> leagues =
          executeRequest(cmsEndpoint.getYcLeagues()).orElse(Collections.emptyList());
      setHealthOK();
      return leagues;
    } catch (IOException | JsonSyntaxException e) {
      setHealthFail();
      NewRelic.noticeError(e);
      log.error("Unable parse YC leagues", e);
      return new ArrayList<>();
    }
  }

  private <T> Optional<T> executeRequest(Call<T> call) throws IOException {
    Response<T> response = call.execute();
    if (!response.isSuccessful()) {
      String errorBody = response.errorBody() != null ? response.errorBody().string() : null;
      log.warn("[CmsServiceImpl] Response code: {}, errorBody: {}.", response.code(), errorBody);

      return Optional.empty();
    }
    return Optional.ofNullable(response.body());
  }

  @Override
  public HealthStatus getHealthStatus() {
    return healthStatus;
  }

  @Override
  public Collection<SportsCategory> getSportsCategories() {
    try {
      final String transactionName = "/sport-category";
      NewRelic.setTransactionName(null, transactionName);
      Collection<SportsCategory> sportsCategories =
          executeRequest(cmsEndpoint.getSportsCategories()).orElse(Collections.emptyList());
      setHealthOK();
      return sportsCategories;
    } catch (IOException | JsonSyntaxException e) {
      setHealthFail();
      NewRelic.noticeError(e);
      log.error("Unable parse YC leagues", e);
      return Collections.emptyList();
    }
  }

  public Collection<AssetManagement> getAssetManagementInfoByBrand() {
    try {
      Collection<AssetManagement> assetManagementDtos =
          executeRequest(cmsEndpoint.getAssetManagementInfo()).orElse(Collections.emptyList());
      setHealthOK();
      log.info("called cms api for assetmanagement {}", assetManagementDtos.size());
      return assetManagementDtos;
    } catch (IOException e) {
      setHealthFail();
      return Collections.emptyList();
    }
  }
  // BMA-62182: Get list for Fanzones from Oxygen-cms-api using cmsEndpoint.findAllFanzoneByBrand()
  // api request
  @Trace(dispatcher = true)
  @Override
  public Collection<Fanzone> getFanzones() {
    try {
      final String transactionName = "/fanzone";
      NewRelic.setTransactionName(null, transactionName);
      Collection<Fanzone> fanzones =
          executeRequest(cmsEndpoint.findAllFanzoneByBrand()).orElse(Collections.emptyList());
      setHealthOK();
      return fanzones;
    } catch (IOException e) {
      setHealthFail();
      return Collections.emptyList();
    }
  }

  @Trace(dispatcher = true)
  @Override
  public List<VirtualSportDto> getVirtualSportsByBrand() {
    try {
      final String transactionName = "/virtual-sports";
      NewRelic.setTransactionName(null, transactionName);
      List<VirtualSportDto> virtualSportDtoCollection =
          (List<VirtualSportDto>)
              executeRequest(cmsEndpoint.findVirtualSportsConfigs())
                  .orElse(Collections.emptyList());
      setHealthOK();
      return virtualSportDtoCollection;
    } catch (IOException ie) {
      setHealthFail();
      return Collections.emptyList();
    }
  }

  private void setHealthOK() {
    healthStatus = HealthStatus.OK;
  }

  private void setHealthFail() {
    healthStatus = HealthStatus.OUT_OF_SERVICE;
  }
}
