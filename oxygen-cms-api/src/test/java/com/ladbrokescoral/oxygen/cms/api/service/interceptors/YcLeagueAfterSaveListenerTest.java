package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.YcLeagueDto;
import com.ladbrokescoral.oxygen.cms.api.entity.YourCallLeague;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.YourCallLeaguePublicService;
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
public class YcLeagueAfterSaveListenerTest extends AbstractAfterSaveListenerTest<YourCallLeague> {

  @Mock private YourCallLeaguePublicService service;
  @Getter @InjectMocks private YcLeagueAfterSaveListener listener;

  @Getter @Mock private YourCallLeague entity;
  @Mock private LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Getter private List<YcLeagueDto> collection = Arrays.asList(new YcLeagueDto());

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "yc-leagues"},
          {"connect", "api/connect", "yc-leagues"}
        });
  }

  @Before
  public void init() {
    given(service.findByBrand(anyString())).willReturn(this.getCollection());
    ReflectionTestUtils.setField(listener, "coralYcleaguesTopic", "coral-cms-ycleagues");
    ReflectionTestUtils.setField(listener, "ladsYcleaguesTopic", "cms-ycleagues");
  }
}
