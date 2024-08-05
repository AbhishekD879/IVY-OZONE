package com.coral.oxygen.edp.model.mapping;

import static org.mockito.ArgumentMatchers.any;

import com.coral.oxygen.edp.model.output.OutputEvent;
import com.egalacoral.spark.siteserver.model.Event;
import java.util.ArrayList;
import java.util.List;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class EventLiveStreamAvailableMapperTest {

  private EventLiveStreamAvailableMapper mapper;

  @Mock private EventMapper chian;

  @Before
  public void setUp() {
    Mockito.when(chian.map(any(), any())).thenReturn(new OutputEvent());
    mapper = new EventLiveStreamAvailableMapper(chian);
  }

  @Test
  public void testNullDrillDownTagNames() {
    // preparation
    Event event = new Event();

    // acton
    OutputEvent result = mapper.map(null, event);

    // verification
    Assert.assertFalse(result.isLiveStreamAvailable());
  }

  @Test
  public void testEmptyDrillDownTagNames() {
    // preparation
    Event event = new Event();
    event.setDrilldownTagNames("");

    // acton
    OutputEvent result = mapper.map(null, event);

    // verification
    Assert.assertFalse(result.isLiveStreamAvailable());
  }

  @Test
  public void testSomeDrillDownTagNames() {
    // preparation
    Event event = new Event();
    event.setDrilldownTagNames("123");

    // acton
    OutputEvent result = mapper.map(null, event);

    // verification
    Assert.assertFalse(result.isLiveStreamAvailable());
  }

  @Test
  public void testDrillDownTagNamesForLiveStream() {

    List<String> validDrilldownTagNames = new ArrayList<>();

    validDrilldownTagNames.add("EVFLAG_RVA");
    validDrilldownTagNames.add("EVFLAG_PVM");
    validDrilldownTagNames.add("EVFLAG_AVA");
    validDrilldownTagNames.add("EVFLAG_IVM");
    validDrilldownTagNames.add("EVFLAG_RPM");

    for (String ddTagName : validDrilldownTagNames) {
      // preparation
      Event event = new Event();
      event.setDrilldownTagNames(ddTagName);

      // acton
      OutputEvent result = mapper.map(null, event);

      // verification
      Assert.assertTrue(result.isLiveStreamAvailable());
    }
  }
}
