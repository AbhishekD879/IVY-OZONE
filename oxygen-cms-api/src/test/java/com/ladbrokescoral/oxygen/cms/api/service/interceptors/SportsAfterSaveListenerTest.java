package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.SportDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Sport;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SportPublicService;
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
public class SportsAfterSaveListenerTest extends AbstractAfterSaveListenerTest<Sport> {

  @Mock private SportPublicService service;
  @Getter @InjectMocks private SportsAfterSaveListener listener;

  @Getter @Mock private Sport entity;
  @Mock private LadsCoralKafkaPublisher ladsCoralKafkaPublisher;
  @Getter private List<SportDto> collection = Arrays.asList(new SportDto());

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "sports"},
          {"connect", "api/connect", "sports"}
        });
  }

  @Before
  public void init() {
    ReflectionTestUtils.setField(listener, "coralSportsTopic", "coral-cms-sports");
    ReflectionTestUtils.setField(listener, "ladsSportsTopic", "cms-sports");
    given(service.find(anyString())).willReturn(this.getCollection());
  }
}
