package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.RssReward;
import com.ladbrokescoral.oxygen.cms.api.service.RssRewardService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;

@RunWith(Parameterized.class)
public class RssRewardAfterSaveListenerTest extends AbstractAfterSaveListenerTest<RssReward> {
  @Mock private RssRewardService service;
  @Getter @InjectMocks private RssRewardAfterSaveListener listener;
  @Getter @Mock private RssReward entity;
  @Getter @Mock private RssReward model;
  @Getter private List<RssReward> collection = Arrays.asList(model);
  @Mock private LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Parameterized.Parameters
  public static List<Object[]> data() throws IOException {
    return Arrays.asList(new Object[][] {{"bma", "api/bma/rss-reward", "rss-reward"}});
  }

  @Before
  public void init() {
    given(service.getRssReward(anyString())).willReturn(null);
  }
}
