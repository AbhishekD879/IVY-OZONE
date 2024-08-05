package com.oxygen.publisher.sportsfeatured.context;

import com.corundumstudio.socketio.SocketIOServer;
import com.newrelic.api.agent.Trace;
import com.oxygen.publisher.sportsfeatured.SportsServiceRegistry;
import com.oxygen.publisher.sportsfeatured.model.PageCacheUpdate;
import com.oxygen.publisher.sportsfeatured.model.PageRawIndex;
import com.oxygen.publisher.sportsfeatured.model.SportsCachedData;
import com.oxygen.publisher.sportsfeatured.service.FeaturedService;
import java.util.Map;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;

/** Created by Aliaksei Yarotski on 12/28/17. */
@Slf4j
public class SportsMiddlewareContext {

  @Getter private final SportsCachedData featuredCachedData;
  private final SportsServiceRegistry serviceRegistry;

  public SportsMiddlewareContext(
      SportsServiceRegistry serviceRegistry, SportsCachedData sportsCachedData) {
    this.featuredCachedData = sportsCachedData;
    this.serviceRegistry = serviceRegistry;
  }

  @Trace(dispatcher = true)
  public void applyWorkingCache(PageCacheUpdate newPage) {
    log.info("##### NEW PAGE CACHE -> wait for commit ######## {}", newPage.getPageVersion());
    synchronized (newPage.getEntityGUID().intern()) {
      if (!newPage.isFullFill()) {
        log.error(
            "#### the page update did not read. Lock operation was failed. {} ",
            newPage.getPageVersion());
        return;
      }
      featuredCachedData.updatePage(newPage);
      log.info("###### {} NEW PAGE CACHE ######", newPage.getPageVersion());
    }
  }

  public FeaturedService featuredService() {
    return serviceRegistry.getFeaturedService();
  }

  public SocketIOServer socketIOServer() {
    return serviceRegistry.getSocketIOServer();
  }

  public void registerNewPageId(final PageRawIndex pageRawIndex) {

    final String sportId = String.valueOf(pageRawIndex.getSportId());
    if (!featuredCachedData.getSportPageData().containsKey(sportId)) {
      log.info("inserting new sportId in sportPageMap cache: {}", sportId);
      featuredCachedData.insertSportPageData(Map.of(sportId, pageRawIndex));
    }
  }

  public void removePageIdFromCache(final String sportId) {

    featuredCachedData.removeSportIdFromSportPageMapCache(sportId);
  }
}
