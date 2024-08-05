package com.coral.oxygen.edp.model.mapping;

import static org.mockito.ArgumentMatchers.any;

import com.coral.oxygen.edp.model.output.OutputEvent;
import com.egalacoral.spark.siteserver.model.Event;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class EventIsUSMapperTest {

  private EventIsUSMapper mapper;

  @Mock private EventMapper chian;

  @Before
  public void setUp() {
    Mockito.when(chian.map(any(), any())).thenReturn(new OutputEvent());
    mapper = new EventIsUSMapper(chian);
  }

  @Test
  public void testNullFlagType() {
    // preparation
    Event event = new Event();

    // acton
    OutputEvent result = mapper.map(null, event);

    // verification
    Assert.assertFalse(result.getIsUS());
  }

  @Test
  public void testEventIsUs() {
    // preparation
    Event event = new Event();
    event.setTypeFlagCodes("EU,US,UA");

    // acton
    OutputEvent result = mapper.map(null, event);

    // verification
    Assert.assertTrue(result.getIsUS());
  }

  @Test
  public void testEventIsNotUs() {
    // preparation
    Event event = new Event();
    event.setTypeFlagCodes("EU,UA");

    // acton
    OutputEvent result = mapper.map(null, event);

    // verification
    Assert.assertFalse(result.getIsUS());
  }
}
