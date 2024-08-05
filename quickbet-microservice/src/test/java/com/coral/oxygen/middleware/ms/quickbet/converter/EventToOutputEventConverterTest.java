package com.coral.oxygen.middleware.ms.quickbet.converter;

import static org.assertj.core.api.Assertions.assertThat;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputEvent;
import com.coral.oxygen.middleware.ms.quickbet.utils.TestUtils;
import com.egalacoral.spark.siteserver.model.Event;
import org.junit.jupiter.api.Test;

public class EventToOutputEventConverterTest {
  @Test
  public void testConvert() {
    Event event =
        TestUtils.deserializeWithGson(
            "converter/eventToOutputEventConverter/event.json", Event.class);

    EventToOutputEventConverter converter =
        new EventToOutputEventConverter(
            new MarketToOutputMarketConverter(new OutcomeToOutputOutcomeConverter()));
    OutputEvent expectedResult =
        TestUtils.deserializeWithGson(
            "converter/eventToOutputEventConverter/output_event.json", OutputEvent.class);
    OutputEvent outputEvent = converter.convert(event);
    assertThat(outputEvent).isEqualTo(expectedResult);
  }
}
