package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.GameDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Game;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.GamePublicService;
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
public class GameAfterSaveListenerTest extends AbstractAfterSaveListenerTest<Game> {

  @Mock private GamePublicService service;
  @Getter @InjectMocks private GameAfterSaveListener listener;
  @Getter @Mock private Game entity;
  @Getter @Mock private List<GameDto> collection = Arrays.asList(new GameDto());
  @Mock private LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma/one-two-free", "games"},
          {
            "connect", "api/connect/one-two-free", "games",
          }
        });
  }

  @Before
  public void init() {
    given(service.findByBrand(anyString())).willReturn(this.getCollection());
    ReflectionTestUtils.setField(listener, "ladsGamesTopic", "cms-games");
  }
}
