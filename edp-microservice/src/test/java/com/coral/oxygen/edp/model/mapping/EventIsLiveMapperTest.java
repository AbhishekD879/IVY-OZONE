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
public class EventIsLiveMapperTest {

  private EventIsLiveMapper mapper;

  @Mock private EventMapper chian;

  @Before
  public void setUp() {
    Mockito.when(chian.map(any(), any())).thenReturn(new OutputEvent());
    mapper = new EventIsLiveMapper(chian);
  }

  @Test
  public void testNullRawIsOffCode() {
    // preparation
    Event event = new Event();

    // acton
    OutputEvent result = mapper.map(null, event);

    // verification
    Assert.assertFalse(result.getEventIsLive());
  }

  @Test
  public void testNullIsStarted() {
    // preparation
    Event event = new Event();
    event.setRawIsOffCode("-");

    // acton
    OutputEvent result = mapper.map(null, event);

    // verification
    Assert.assertFalse(result.getEventIsLive());
  }

  @Test
  public void testRawIsOffCodeEqualsY() {
    // preparation
    Event event = new Event();
    event.setRawIsOffCode("Y");

    // acton
    OutputEvent result = mapper.map(null, event);

    // verification
    Assert.assertTrue(result.getEventIsLive());
  }

  @Test
  public void testEventIsStarted() {
    // preparation
    Event event = new Event();
    event.setRawIsOffCode("-");
    event.setIsStarted(true);

    // acton
    OutputEvent result = mapper.map(null, event);

    // verification
    Assert.assertTrue(result.getEventIsLive());
  }

  @Test
  public void testEventIsNotStarted() {
    // preparation
    Event event = new Event();
    event.setRawIsOffCode("-");
    event.setIsStarted(false);

    // acton
    OutputEvent result = mapper.map(null, event);

    // verification
    Assert.assertFalse(result.getEventIsLive());
  }
}
