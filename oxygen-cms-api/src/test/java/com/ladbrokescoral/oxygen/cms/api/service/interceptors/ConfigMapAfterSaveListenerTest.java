package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.ApiCollectionConfig;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.test.util.ReflectionTestUtils;

@RunWith(Parameterized.class)
public class ConfigMapAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<ApiCollectionConfig> {

  @Mock private LadsCoralKafkaPublisher ladsCoralKafkaPublisher;
  @Getter @InjectMocks private ConfigMapAfterSaveListener listener;

  @Getter @Mock private ApiCollectionConfig entity;
  @Getter private List<ApiCollectionConfig> collection = null;

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "configMap"},
          {"connect", "api/connect", "configMap"},
          {" ", " ", " "}
        });
  }

  @Before
  public void init() {
    ReflectionTestUtils.setField(listener, "coralConfigMapTopic", "coral-cms-config-map");
    ReflectionTestUtils.setField(listener, "ladsConfigMapTopic", "cms-config-map");
  }
}
