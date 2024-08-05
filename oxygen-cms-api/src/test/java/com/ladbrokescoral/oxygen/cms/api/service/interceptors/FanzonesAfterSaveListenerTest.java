package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.Fanzone;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesService;
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
public class FanzonesAfterSaveListenerTest extends AbstractAfterSaveListenerTest<Fanzone> {

  @Mock private FanzonesService service;
  @Getter @InjectMocks private FanzonesAfterSaveListener listener;
  @Getter @Mock private Fanzone entity;
  @Getter @Mock private List<Fanzone> collection = Arrays.asList(entity);
  @Mock private LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "fanzone"},
          {"connect", "api/connect", "fanzone"}
        });
  }

  @Before
  public void init() {
    given(service.findByBrand(anyString())).willReturn(this.getCollection());
    ReflectionTestUtils.setField(listener, "coralFanzoneTopic", "coral-cms-fanzones");
    ReflectionTestUtils.setField(listener, "ladsFanzoneTopic", "cms-fanzones");
  }
}
