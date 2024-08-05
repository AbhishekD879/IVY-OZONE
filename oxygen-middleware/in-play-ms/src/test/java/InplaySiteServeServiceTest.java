import static com.coral.oxygen.middleware.pojos.model.output.PrimaryMarkets.*;

import com.coral.oxygen.middleware.common.service.MarketTemplateNameService;
import com.coral.oxygen.middleware.common.utils.QueryFilterBuilder;
import com.coral.oxygen.middleware.in_play.service.OutrightOutcomesFilter;
import com.coral.oxygen.middleware.in_play.service.siteserver.InplaySiteServeService;
import com.coral.oxygen.middleware.pojos.model.output.PrimaryMarkets;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.Mockito;

public class InplaySiteServeServiceTest {

  @Mock SiteServerApi siteServerApi;
  @Mock MarketTemplateNameService marketTemplateNameService;
  @Mock OutrightOutcomesFilter topThreeOutrightOutcomesFilter;
  @Mock QueryFilterBuilder queryFilterBuilder;

  private static final List<PrimaryMarkets> SPROTS_WITH_PRIMARY_MARKETS =
      Arrays.asList(FOOTBALL, TENNIS, BASKETBALL);
  InplaySiteServeService service = null;

  @Before
  public void setUp() {
    marketTemplateNameService = Mockito.mock(MarketTemplateNameService.class);
    service =
        new InplaySiteServeService(
            siteServerApi,
            marketTemplateNameService,
            topThreeOutrightOutcomesFilter,
            queryFilterBuilder);
  }

  @Test
  public void testMergeEventsWithOutrightMarkets()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    Method method =
        service
            .getClass()
            .getDeclaredMethod("mergeEventsWithOutrightMarkets", List.class, List.class);
    method.setAccessible(true);
    Mockito.doReturn(true)
        .when(marketTemplateNameService)
        .containsName(Mockito.any(), Mockito.anyString());
    Children children1 = new Children();
    children1.setMarket(null);
    Event event = new Event();
    event.setId("100");
    event.setChildren(new ArrayList<>(Collections.singletonList(children1)));
    Market market = new Market();
    market.setTemplateMarketName("OUTRIGHT");
    Children children = new Children();
    children.setMarket(market);
    Event event1 = new Event();
    event1.setId("100");
    event1.setChildren(new ArrayList<>(Collections.singletonList(children)));
    List<Event> list1 = new ArrayList<>();
    list1.add(event);
    List<Event> list2 = new ArrayList<>();
    list2.add(event1);
    List list = (List) method.invoke(service, list1, list2);
    Assert.assertTrue(list.size() > 0);
  }

  @Test
  public void testFilterEventsWithMarkets()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    Method method = service.getClass().getDeclaredMethod("filterEventsWithMarkets", List.class);
    method.setAccessible(true);
    Event event = new Event();
    Children children = new Children();
    children.setMarket(new Market());
    event.setChildren(Arrays.asList(children));
    List<Event> list = (List<Event>) method.invoke(service, Arrays.asList(event));
    Assert.assertTrue(list.size() > 0);
  }

  @Test
  public void testFilterEventsWithMarketsNegativeCase()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    Method method = service.getClass().getDeclaredMethod("filterEventsWithMarkets", List.class);
    method.setAccessible(true);
    Event event = new Event();
    List<Event> list = (List<Event>) method.invoke(service, Arrays.asList(event));
    Assert.assertFalse(list.size() > 0);
  }
}
