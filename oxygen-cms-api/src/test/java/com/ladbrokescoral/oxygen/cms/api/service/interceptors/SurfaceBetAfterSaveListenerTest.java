package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.SurfaceBet;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.test.util.ReflectionTestUtils;

@RunWith(Parameterized.class)
public class SurfaceBetAfterSaveListenerTest extends AbstractAfterSaveListenerTest<SurfaceBet> {

  @Getter @InjectMocks private SurfaceBetAfterSaveListener listener;
  @Getter @Mock private SurfaceBet entity;
  @Getter private List<?> collection = null;
  @Mock private LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", null},
          {"connect", "api/connect", null}
        });
  }

  @Before
  public void init() {
    ReflectionTestUtils.setField(listener, "coralSurfaceBetTopic", "coral-cms-surfaceBet");
    ReflectionTestUtils.setField(listener, "ladsSurfaceBetTopic", "cms-surfaceBet");
  }
}
