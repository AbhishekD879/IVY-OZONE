package com.egalacoral.spark.siteserver.api;

import com.egalacoral.spark.siteserver.model.Event;
import java.util.List;
import java.util.Optional;
import org.junit.Assert;

/** Created by llegkyy on 18.08.16. */
public class SiteServerAPITest {

  SiteServerAPI siteServerAPI;
  SimpleFilter filter;
  public static String OPEN_BET_EVENT_TYPE = "1878";

  // @Before
  public void init() {
    SiteServerAPI.Builder builder =
        new SiteServerAPI.Builder("http://backoffice-tst2.coral.co.uk/");
    siteServerAPI = builder.build();
    SimpleFilter.SimpleFilterBuilder filterBuilder = new SimpleFilter.SimpleFilterBuilder();
    filter = filterBuilder.build();
  }

  // @Test
  public void testGetClassToSubTypeForClass() {
    Optional<List<Event>> events = siteServerAPI.getEventForType(OPEN_BET_EVENT_TYPE, filter);
    Assert.assertTrue("There should be some undisplayed types", events.isPresent());
    Assert.assertTrue("List should be populated", events.get().size() > 0);
  }
}
