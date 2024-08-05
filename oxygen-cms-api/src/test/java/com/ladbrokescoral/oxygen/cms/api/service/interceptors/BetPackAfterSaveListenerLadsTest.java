package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackEntity;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BetPackMarketPlacePublicService;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.test.util.ReflectionTestUtils;

@RunWith(Parameterized.class)
public class BetPackAfterSaveListenerLadsTest extends AbstractAfterSaveListenerTest<BetPackEntity> {
  @Mock private BetPackMarketPlacePublicService service;

  @Mock private KafkaTemplate<String, List<String>> betPackKafkaTemplate;

  @Getter @InjectMocks private BetPackAfterSaveListener listener;

  @Getter @Mock BetPackEntity entity;

  @Getter private List<BetPackEntity> collection = Collections.EMPTY_LIST;

  @Getter private List<BetPackEntity> collectionV2 = Collections.EMPTY_LIST;

  @Parameterized.Parameters
  public static List<Object[]> data() throws IOException {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma/", "bet-pack"}, {"ladbrokes", "api/ladbrokes/", "bet-pack"}
        });
  }

  @Before
  public void init() {
    ReflectionTestUtils.setField(listener, "coralBetPackTopic", "coral-active-bet-packs-topic");
    given(service.findAllBetPacksBetweenDate(anyString())).willReturn(new ArrayList<>());
    given(service.getActiveBetPackByBrand(anyString())).willReturn(new ArrayList<>());
  }
}
