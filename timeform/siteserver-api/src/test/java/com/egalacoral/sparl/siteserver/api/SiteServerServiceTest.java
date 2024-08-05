package com.egalacoral.sparl.siteserver.api;

import com.egalacoral.spark.siteserver.api.BinaryOperation;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerAPI;
import com.egalacoral.spark.siteserver.model.Event;
import java.io.IOException;
import java.util.List;
import org.joda.time.DateTime;

/** Created by oleg.perushko@symphony-solutions.eu on 8/3/16 */
public class SiteServerServiceTest {

  // @Test
  public void test() throws IOException {
    /** Example how you can use SiteServerAPI fro query data */
    final SiteServerAPI api =
        new SiteServerAPI.Builder("http://backoffice-tst2.coral.co.uk/")
            .setLoggingLevel(SiteServerAPI.Level.BODY)
            .setConnectionTimeout(1)
            .setReadTimeout(1)
            .setMaxNumberOfRetries(1)
            .setVersion("2.9")
            .build();

    final SimpleFilter simpleFilter =
        new SimpleFilter.SimpleFilterBuilder()
            .addBinaryOperation(
                "event.startTime", BinaryOperation.greaterThanOrEqual, DateTime.now().minusDays(1))
            .addBinaryOperation(
                "event.startTime", BinaryOperation.lessThan, DateTime.now().plusDays(1))
            .build();

    List<Event> events = api.getEventForType("1862", simpleFilter).get();
    System.out.printf("List of events for type 1868: " + events);
  }
}
