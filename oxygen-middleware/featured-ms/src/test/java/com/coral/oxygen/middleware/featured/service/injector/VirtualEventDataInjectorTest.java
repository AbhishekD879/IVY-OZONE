package com.coral.oxygen.middleware.featured.service.injector;

import static org.mockito.ArgumentMatchers.any;

import com.coral.oxygen.middleware.common.mappers.EventMapper;
import com.coral.oxygen.middleware.common.service.featured.IdsCollector;
import com.coral.oxygen.middleware.common.utils.QueryFilterBuilder;
import com.coral.oxygen.middleware.featured.consumer.sportpage.VirtualEventsModuleProcessorTest;
import com.coral.oxygen.middleware.pojos.model.output.featured.VirtualEventModule;
import com.egalacoral.spark.siteserver.api.ExistsFilter;
import com.egalacoral.spark.siteserver.api.LimitRecordsFilter;
import com.egalacoral.spark.siteserver.api.LimitToFilter;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.jupiter.api.Assertions;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class VirtualEventDataInjectorTest {

  private VirtualEventDataInjector virtualEventDataInjector;

  @Mock private SiteServerApi siteServerAPI;
  @Mock private EventMapper eventMapper;
  @Mock private QueryFilterBuilder queryFilterBuilder;

  private IdsCollector idsCollector;

  @Before
  public void init() {
    virtualEventDataInjector =
        new VirtualEventDataInjector(eventMapper, siteServerAPI, queryFilterBuilder);

    idsCollector = new IdsCollector(Arrays.asList(234L, 333L, 45467L));
  }

  @Test
  public void eventDataInjectorTest() {
    Assertions.assertDoesNotThrow(
        () -> virtualEventDataInjector.injectDataEvents(createVirutalModule()));
  }

  @Test
  public void eventDataInjectorTestForInjectData() {
    Assertions.assertDoesNotThrow(() -> virtualEventDataInjector.injectData(null, idsCollector));
  }

  @Test
  public void eventDataInjectorTestForEvents() {
    Mockito.doReturn(Mockito.mock(SimpleFilter.class))
        .when(queryFilterBuilder)
        .getFilterForVirtualEvents();

    Assertions.assertDoesNotThrow(
        () -> virtualEventDataInjector.injectDataEvents(createVirutalModule()));
  }

  @Test
  public void eventDataInjectorTestForEventsNonFootball() {
    Mockito.doReturn(Mockito.mock(SimpleFilter.class))
        .when(queryFilterBuilder)
        .getFilterForVirtualEvents();

    Mockito.doReturn(Optional.of(getSiteServEvents()))
        .when(siteServerAPI)
        .getNextNEventToOutcomeForType(
            Mockito.anyInt(),
            any(List.class),
            any(SimpleFilter.class),
            any(ExistsFilter.class),
            any(LimitToFilter.class),
            any(LimitRecordsFilter.class),
            any(Boolean.class),
            any(Boolean.class));

    Assertions.assertDoesNotThrow(
        () -> virtualEventDataInjector.injectDataEvents(createVirutalModule()));
  }

  private List<Event> getSiteServEvents() {
    return VirtualEventsModuleProcessorTest.getLiveServEvents();
  }

  private Children toChildren(Event e) {
    Children children = new Children();
    children.setEvent(e);
    return children;
  }

  private VirtualEventModule createVirutalModule() {
    VirtualEventModule virtualEventModule = new VirtualEventModule();
    virtualEventModule.setTypeIds("12345,12684");
    // virtualEventModule.setLimit(12);
    return virtualEventModule;
  }
}
