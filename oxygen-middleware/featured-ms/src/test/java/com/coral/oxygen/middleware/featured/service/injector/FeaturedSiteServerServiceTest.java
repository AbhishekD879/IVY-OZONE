package com.coral.oxygen.middleware.featured.service.injector;

import com.coral.oxygen.middleware.common.service.MarketTemplateNameService;
import com.egalacoral.spark.siteserver.api.ExistsFilter;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Category;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Pool;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.junit.Assert;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

class FeaturedSiteServerServiceTest {

  private SiteServerApi siteServerApi = Mockito.mock(SiteServerApi.class);
  private MarketTemplateNameService marketTemplateNameService =
      Mockito.mock(MarketTemplateNameService.class);

  FeaturedSiteServerService featuredSiteServerService =
      new FeaturedSiteServerService(siteServerApi, marketTemplateNameService);

  @Test
  void testGetActiveClassesWithOpenEvents() {
    Mockito.doReturn(createClass(123, 21))
        .when(siteServerApi)
        .getClasses(Mockito.any(SimpleFilter.class), Mockito.any(ExistsFilter.class));
    List<Category> categoryList = featuredSiteServerService.getActiveClassesWithOpenEvents("21");
    Assert.assertNotNull(categoryList);
  }

  @Test
  void testGetAllEventToMarketForEvent() {
    Mockito.doReturn(Optional.of(Arrays.asList(Mockito.mock(Event.class))))
        .when(siteServerApi)
        .getEventToMarketForEvent(
            Mockito.any(), Mockito.any(), Mockito.any(), Mockito.anyBoolean());
    List<Event> events =
        featuredSiteServerService.getAllEventToMarketForEvent(Arrays.asList("123"));
    Assert.assertNotNull(events);
  }

  @Test
  void testGetPoolTypes() {
    Mockito.doReturn(Optional.of(Arrays.asList(createPool("123"))))
        .when(siteServerApi)
        .getPoolForEvent(Mockito.any(), Mockito.any());
    List<Pool> pools =
        featuredSiteServerService.getPoolTypes(Arrays.asList("123"), Arrays.asList("UQDP"));
    Assert.assertNotNull(pools);
  }

  @Test
  void getEventToMarketForMarketTest() {
    Mockito.doReturn(Optional.of(Arrays.asList(new Event())))
        .when(siteServerApi)
        .getEventToMarketForType(Mockito.any(), Mockito.any(), Mockito.anyBoolean());
    Optional<List<Event>> children =
        featuredSiteServerService.getEventToMarketForType(Arrays.asList("123"));
    Assertions.assertNotNull(children);
  }

  private Optional<List<Category>> createClass(Integer id, Integer categoryId) {
    Category eventClass = Mockito.mock(Category.class);
    eventClass.setCategoryId(categoryId);
    eventClass.setId(id);
    return Optional.of(Arrays.asList(eventClass));
  }

  static Pool createPool(String marketIds) {
    Pool pool = new Pool();
    pool.setId("12");
    pool.setType("UQDP");
    pool.setMarketIds(marketIds);
    return pool;
  }
}
