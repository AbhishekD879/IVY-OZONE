package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
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
public class SportModulesAfterSaveListenerTest extends AbstractAfterSaveListenerTest<SportModule> {

  @Getter @InjectMocks private SportModulesAfterSaveListener listener;
  @Getter @Mock private SportModule entity;
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
    ReflectionTestUtils.setField(listener, "coralSportModulesTopic", "coral-cms-sportModules");
    ReflectionTestUtils.setField(listener, "ladsSportModulesTopic", "cms-sportModules");
  }
}
