package com.oxygen.publisher.sportsfeatured.context;

import static org.mockito.Mockito.*;

import com.oxygen.publisher.sportsfeatured.SportsServiceRegistry;
import com.oxygen.publisher.sportsfeatured.model.FeaturedModel;
import com.oxygen.publisher.sportsfeatured.model.PageCacheUpdate;
import com.oxygen.publisher.sportsfeatured.model.PageRawIndex;
import com.oxygen.publisher.sportsfeatured.model.SportsCachedData;
import com.oxygen.publisher.sportsfeatured.service.SportsPageIdRegistration;
import java.util.HashMap;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

public class SportsMiddlewareContextTest {

  public SportsMiddlewareContext testedClass;
  private PageRawIndex.GenerationKey generation;
  private FeaturedModel thisModel;
  private SportsServiceRegistry serviceRegistry;
  private SportsCachedData sportsCachedData;
  private SportsPageIdRegistration namespaceRegistrator;

  @Before
  public void init() {
    serviceRegistry = mock(SportsServiceRegistry.class);
    namespaceRegistrator = mock(SportsPageIdRegistration.class);
    when(serviceRegistry.getSportsPageIdRegistration()).thenReturn(namespaceRegistrator);
    sportsCachedData = mock(SportsCachedData.class);
    testedClass = new SportsMiddlewareContext(serviceRegistry, sportsCachedData);

    generation = PageRawIndex.GenerationKey.fromString("sport::16::100");
    thisModel = new FeaturedModel();
    thisModel.setPageId("16");
  }

  @Test
  public void applyWorkingCache_FailOnEmptyData() {
    PageCacheUpdate newPageData = new PageCacheUpdate(generation);
    testedClass.applyWorkingCache(newPageData);
    verify(sportsCachedData, never()).updatePage(Mockito.any());
  }

  @Test
  public void applyWorkingCache_FailOnVersion() {
    PageCacheUpdate newPageData =
        PageCacheUpdate.builder()
            .pageVersion(PageRawIndex.GenerationKey.fromString("sport::16::99"))
            .pageModel(thisModel)
            .moduleMap(new HashMap<>())
            .primaryMarketCache(new HashMap<>())
            .build();

    testedClass.applyWorkingCache(newPageData);
    verify(sportsCachedData, atLeast(1)).updatePage(Mockito.any());
  }

  @Test
  public void applyWorkingCache_OK() {
    PageCacheUpdate newPageData =
        PageCacheUpdate.builder()
            .pageVersion(generation)
            .pageModel(thisModel)
            .moduleMap(new HashMap<>())
            .primaryMarketCache(new HashMap<>())
            .build();
    testedClass.applyWorkingCache(newPageData);
    verify(sportsCachedData, atLeast(1)).updatePage(Mockito.any());
  }
}
