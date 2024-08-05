package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.segment.Segment;
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
public class SegmentAfterSaveListenerTest extends AbstractAfterSaveListenerTest<Segment> {

  @Getter @InjectMocks private SegmentAfterSaveListener listener;
  @Getter @Mock private Segment entity;
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
    ReflectionTestUtils.setField(listener, "coralSegmentsTopic", "coral-cms-segments");
    ReflectionTestUtils.setField(listener, "ladsSegmentsTopic", "cms-segments");
  }
}
