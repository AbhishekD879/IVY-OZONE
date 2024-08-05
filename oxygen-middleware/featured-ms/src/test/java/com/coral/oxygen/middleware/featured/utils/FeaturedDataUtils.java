package com.coral.oxygen.middleware.featured.utils;

import com.coral.oxygen.middleware.RuntimeTypeAdapterFactory;
import com.coral.oxygen.middleware.common.service.ModuleAdapter;
import com.coral.oxygen.middleware.pojos.model.cms.featured.CmsRacingModule;
import com.coral.oxygen.middleware.pojos.model.cms.featured.CommonModule;
import com.coral.oxygen.middleware.pojos.model.cms.featured.HighlightCarousel;
import com.coral.oxygen.middleware.pojos.model.cms.featured.InPlayConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.ModularContentItem;
import com.coral.oxygen.middleware.pojos.model.cms.featured.RecentlyPlayedGame;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPage;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModuleDataItem;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportsQuickLink;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SurfaceBet;
import com.coral.oxygen.middleware.pojos.model.cms.featured.VirtualEvent;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedModel;
import com.egalacoral.spark.siteserver.model.Aggregation;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;
import java.lang.reflect.Type;
import java.util.List;

public class FeaturedDataUtils {

  public static List<ModularContentItem> getModularContentItemsFromResource(String resourceName) {
    String contentJson = TestUtils.getResourse(resourceName);
    Type listType = new TypeToken<List<ModularContentItem>>() {}.getType();
    return ModuleAdapter.FEATURED_GSON.fromJson(contentJson, listType);
  }

  public static ModularContentItem getModularContentItemFromResource(String resourceName) {
    String featuredItemJson = TestUtils.getResourse(resourceName);
    return ModuleAdapter.FEATURED_GSON.fromJson(featuredItemJson, ModularContentItem.class);
  }

  public static FeaturedModel getFeaturedModelFromResource(String resourceName) {
    String featuredModelJson = TestUtils.getResourse(resourceName);
    return ModuleAdapter.FEATURED_GSON.fromJson(featuredModelJson, FeaturedModel.class);
  }

  public static List<Children> getSSEventsFromResource(String resourceName) {
    String eventsJson = TestUtils.getResourse(resourceName);
    Type listType = new TypeToken<List<Children>>() {}.getType();
    return ModuleAdapter.FEATURED_GSON.fromJson(eventsJson, listType);
  }

  public static List<Event> getSSEventToOutcomeForOutcome(String resourceName) {
    String eventJson = TestUtils.getResourse(resourceName);
    Type listType = new TypeToken<List<Event>>() {}.getType();
    return ModuleAdapter.FEATURED_GSON.fromJson(eventJson, listType);
  }

  public static List<Children> getSSEventCommentaryForEvent(String resourceName) {
    String eventJson = TestUtils.getResourse(resourceName);
    Type listType = new TypeToken<List<Children>>() {}.getType();
    return ModuleAdapter.FEATURED_GSON.fromJson(eventJson, listType);
  }

  public static List<Aggregation> getSSMarketsCountForEvent(String resourceName) {
    String marketsCountJson = TestUtils.getResourse(resourceName);
    Type listType = new TypeToken<List<Aggregation>>() {}.getType();
    return ModuleAdapter.FEATURED_GSON.fromJson(marketsCountJson, listType);
  }

  public static List<SportsQuickLink> getCmsQuickLinksFromResource(String resourceName) {
    String quickLinksJson = TestUtils.getResourse(resourceName);
    Type listType = new TypeToken<List<SportsQuickLink>>() {}.getType();

    return ModuleAdapter.FEATURED_GSON.fromJson(quickLinksJson, listType);
  }

  public static List<SportPage> getCmsSportPagesFromResource(String resourceName) {
    String json = TestUtils.getResourse(resourceName);
    Type listType = new TypeToken<List<SportPage>>() {}.getType();

    RuntimeTypeAdapterFactory<SportPageModuleDataItem> sportPageDataAdapterFactory =
        RuntimeTypeAdapterFactory.of(SportPageModuleDataItem.class)
            .registerSubtype(CommonModule.class, "COMMON_MODULE")
            .registerSubtype(HighlightCarousel.class, "HIGHLIGHTS_CAROUSEL")
            .registerSubtype(InPlayConfig.class, "IN_PLAY")
            .registerSubtype(ModularContentItem.class, "FEATURED")
            .registerSubtype(SportsQuickLink.class, "QUICK_LINK")
            .registerSubtype(SurfaceBet.class, "SURFACE_BET")
            .registerSubtype(CmsRacingModule.class, "RACING_MODULE")
            .registerSubtype(VirtualEvent.class, "VIRTUAL_NEXT_EVENTS")
            .registerSubtype(RecentlyPlayedGame.class, "RECENTLY_PLAYED_GAMES");

    Gson gson = new GsonBuilder().registerTypeAdapterFactory(sportPageDataAdapterFactory).create();

    return gson.fromJson(json, listType);
  }
}
