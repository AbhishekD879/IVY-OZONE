package com.ladbrokescoral.oxygen.questionengine.listeners;

import com.ladbrokescoral.oxygen.event.ConfigMapEvent;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

import static org.junit.Assert.assertNotNull;

@RunWith(MockitoJUnitRunner.class)
public class CmsConfigEventListenerTest {

  @Mock private Map<String, List<String>> configMap;

  @InjectMocks private CmsConfigEventListener cmsConfigEventListener;

  @Test
  public void configMapEventTest() {
    Map<String, List<String>> configMap = new HashMap<>();
    configMap.put("/quiz", Arrays.asList("quiz"));

    assertNotNull(cmsConfigEventListener);
    ConfigMapEvent event = new ConfigMapEvent("cms", configMap);
    cmsConfigEventListener.onApplicationEvent(event);
  }
}
