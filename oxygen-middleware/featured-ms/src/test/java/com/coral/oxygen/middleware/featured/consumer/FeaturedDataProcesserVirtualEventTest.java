package com.coral.oxygen.middleware.featured.consumer;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.Mockito.*;

import com.coral.oxygen.cms.api.CmsService;
import com.coral.oxygen.cms.api.SystemConfigProvider;
import com.coral.oxygen.middleware.common.configuration.CmsConfiguration;
import com.coral.oxygen.middleware.common.configuration.GsonConfiguration;
import com.coral.oxygen.middleware.common.configuration.MappersConfiguration;
import com.coral.oxygen.middleware.common.configuration.OkHttpClientCreator;
import com.coral.oxygen.middleware.common.configuration.SiteServerAPIConfiguration;
import com.coral.oxygen.middleware.common.configuration.cfcache.DeliveryNetworkService;
import com.coral.oxygen.middleware.common.service.AssetManagementService;
import com.coral.oxygen.middleware.common.service.DateTimeHelper;
import com.coral.oxygen.middleware.common.service.MarketTemplateNameService;
import com.coral.oxygen.middleware.common.service.SportsConfig;
import com.coral.oxygen.middleware.common.service.featured.FeaturedModelChangeDetector;
import com.coral.oxygen.middleware.common.service.featured.FeaturedModuleChangeDetector;
import com.coral.oxygen.middleware.common.service.featured.OddsCardHeader;
import com.coral.oxygen.middleware.common.service.notification.MessagePublisher;
import com.coral.oxygen.middleware.common.utils.OrdinalToNumberConverter;
import com.coral.oxygen.middleware.common.utils.QueryFilterBuilder;
import com.coral.oxygen.middleware.featured.aem.AemMetaConsumer;
import com.coral.oxygen.middleware.featured.configuration.FeaturedConfiguration;
import com.coral.oxygen.middleware.featured.consumer.sportpage.*;
import com.coral.oxygen.middleware.featured.consumer.sportpage.bets.PopularBetModuleProcessor;
import com.coral.oxygen.middleware.featured.consumer.sportpage.virtual.VirtualEventsModuleProcessor;
import com.coral.oxygen.middleware.featured.service.*;
import com.coral.oxygen.middleware.featured.service.injector.DFRacingEventsModuleInjector;
import com.coral.oxygen.middleware.featured.service.injector.EventDataInjector;
import com.coral.oxygen.middleware.featured.service.injector.FeaturedCommentaryInjector;
import com.coral.oxygen.middleware.featured.service.injector.MarketsCountInjector;
import com.coral.oxygen.middleware.featured.service.injector.RacingEventsModuleInjector;
import com.coral.oxygen.middleware.featured.service.injector.SingleOutcomeEventsModuleInjector;
import com.coral.oxygen.middleware.featured.service.injector.VirtualEventDataInjector;
import com.coral.oxygen.middleware.featured.utils.FeaturedDataUtils;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPage;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedModel;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedModelsData;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import java.util.ArrayList;
import java.util.List;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
@SpringBootTest(
    classes = {
      CmsConfiguration.class,
      SiteServerAPIConfiguration.class,
      EventDataInjector.class,
      SingleOutcomeEventsModuleInjector.class,
      RacingEventsModuleInjector.class,
      MarketsCountInjector.class,
      FeaturedCommentaryInjector.class,
      MappersConfiguration.class,
      SportsConfig.class,
      GsonConfiguration.class,
      OrdinalToNumberConverter.class,
      FeaturedConfiguration.class,
      HighlightCarouselModuleProcessor.class,
      FanzoneHighlightCarouselModuleProcessor.class,
      SurfaceBetModuleProcessor.class,
      FanzoneSurfaceBetModuleProcessor.class,
      OkHttpClientCreator.class,
      FeaturedModuleProcessor.class,
      MarketTemplateNameService.class,
      QuickLinkModuleProcessor.class,
      RecentlyPlayedGameModuleProcessor.class,
      DFRacingEventsModuleInjector.class,
      AemCarouselsProcessor.class,
      RacingModuleProcessor.class,
      DateTimeHelper.class,
      QueryFilterBuilder.class,
      FeaturedModelStorageService.class,
      VirtualEventsModuleProcessor.class,
      MarketsCountInjector.class,
      DeliveryNetworkService.class,
      VirtualEventDataInjector.class,
      FeaturedDataProcessor.class,
      FanBetsFZModuleProcessor.class,
      TeamBetsFZModuleProcessor.class,
      FanzoneQuickLinkModuleProcessor.class,
      BybWidgetProcessor.class,
      LuckyDipModuleProcessor.class
    })
public class FeaturedDataProcesserVirtualEventTest {

  @MockBean CmsService cmsService;

  @MockBean SiteServerApi siteServerApi;

  @Autowired VirtualEventDataInjector virtualEventDataInjector;

  @Autowired DateTimeHelper dateTimeHelper;

  @Autowired SingleOutcomeEventsModuleInjector singleOutcomeDataInjector;

  @MockBean RacingEventsModuleInjector racingDataInjector;

  @MockBean DFRacingEventsModuleInjector dfRacingEventsModuleInjector;

  @MockBean FeaturedCommentaryInjector commentaryInjector;

  @MockBean FeaturedDataFilter featuredDataFilter;

  @MockBean OddsCardHeader oddsCardHeader;

  @MockBean private BybService bybService;

  @MockBean private InplayModuleConsumer inplayModuleConsumer;

  @MockBean SportPageFilter sportPageFilter;

  @Autowired FeaturedDataProcessor featuredDataProcessor;

  @MockBean AemMetaConsumer aemMetaConsumer;

  @MockBean AemCarouselsProcessor aemCarouselsProcessor;

  @MockBean SystemConfigProvider systemConfigProvider;

  @MockBean RacingModuleProcessor racingModuleProcessor;

  @MockBean FeaturedModelStorageService storageService;

  @MockBean AssetManagementService assetManagementService;

  @MockBean private FeaturedModuleChangeDetector featuredModuleChangeDetector;
  @MockBean private FeaturedModelChangeDetector featuredModelChangeDetector;
  @MockBean private MessagePublisher messagePublisher;
  @MockBean private FeaturedLiveServerSubscriber featuredLiveServerSubscriber;

  @MockBean private DeliveryNetworkService deliveryNetworkService;

  @MockBean private FanzoneQuickLinkModuleProcessor fanzoneQuickLinkModuleProcessor;
  @MockBean private BybWidgetProcessor processor;

  @MockBean private FeaturedNextRacesConfigProcessor featuredNextRacesConfigProcessor;

  @MockBean private PopularBetModuleProcessor popularBetModuleProcessor;
  @MockBean private LuckyDipModuleProcessor luckyDipModuleProcessor;

  @MockBean private PopularAccaModuleProcessor popularAccaModuleProcessor;

  FaeturemodelUtil util = new FaeturemodelUtil();

  @Test
  public void processpageForVirtualEvents() {
    FeaturedModelsData model = createFeaturedModelData();

    when(storageService.getPreviousVersion(10l)).thenReturn(9l);
    when(storageService.getFeaturedModel("0", 9l)).thenReturn(null);

    FeaturedModel result = util.creatFeatureModel(false);
    result.setFeatureStructureChanged(true);
    when(storageService.save(any(FeaturedModel.class), anyLong())).thenReturn(result);
    featuredDataProcessor.process(model);
    verify(messagePublisher, times(142)).publish(any(), any());
  }

  private FeaturedModel getFeaturedModelsData(String fileName) {
    return FeaturedDataUtils.getFeaturedModelFromResource(fileName);
  }

  private List<SportPage> getSportPages() {
    return FeaturedDataUtils.getCmsSportPagesFromResource(
        "featured_consumption_cms_sportPages_output_with_virtual_next_events.json");
  }

  private FeaturedModelsData createFeaturedModelData() {
    List<FeaturedModel> featuredModels = new ArrayList<>();
    FeaturedModel featuredModel = getFeaturedModelsData("featured_model_data.json");
    featuredModels.add(featuredModel);
    return new FeaturedModelsData(featuredModels, getSportPages());
  }
}
