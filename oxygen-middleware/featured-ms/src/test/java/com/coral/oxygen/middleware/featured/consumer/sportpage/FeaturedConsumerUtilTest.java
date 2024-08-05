package com.coral.oxygen.middleware.featured.consumer.sportpage;

import com.coral.oxygen.middleware.featured.consumer.FeaturedConsumerUtil;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.featured.InplayModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.SurfaceBetModule;
import java.util.HashMap;
import java.util.Map;
import org.junit.Assert;
import org.junit.Test;

public class FeaturedConsumerUtilTest {
  @Test
  public void shouldNotAlterEventsModuleDataIfModuleDataIsNull() {
    // Given
    Map<Long, EventsModuleData> eventsModuleData = new HashMap<>();
    SurfaceBetModule module = new SurfaceBetModule();
    module.setData(null);
    // When
    FeaturedConsumerUtil.setEventsModuleData(eventsModuleData, module, null);
    // Then
    Assert.assertTrue(eventsModuleData.isEmpty());
  }

  @Test
  public void shouldNotThrowExceptionWhenInplayModuleDataIsNull() {
    // Given
    InplayModule inplayModule = new InplayModule();
    inplayModule.setData(null);

    //
    FeaturedConsumerUtil.removeUnusedSportsSegments(inplayModule);

    // Then
    Assert.assertNull(inplayModule.getData());
  }
}
