package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.GamificationDetailsPublicDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SeasonGamificationDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Gamification;
import com.ladbrokescoral.oxygen.cms.api.service.GamificationPublicService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SeasonPublicService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import lombok.Getter;
import org.junit.After;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.test.util.ReflectionTestUtils;

@RunWith(Parameterized.class)
public class GamificationAfterSaveListenerTest extends AbstractAfterSaveListenerTest<Gamification> {

  @Mock GamificationPublicService gamificationPublicService;

  @Mock SeasonPublicService seasonPublicService;

  @Getter @Mock private Gamification entity;

  @Getter @InjectMocks private GamificationAfterSaveListener listener;

  @Getter private List<?> collection = null;
  @Mock private LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"ladbrokes", "api/ladbrokes/one-two-free", "gamification"},
          {"ladbrokes", "api/ladbrokes/one-two-free", "current-future-seasons"}
        });
  }

  @Before
  public void init() {
    given(gamificationPublicService.findGamificationByBrand(anyString()))
        .willReturn(Collections.singletonList(new GamificationDetailsPublicDto()));
    given(seasonPublicService.getCurrentFutureSeasons(anyString()))
        .willReturn(Collections.singletonList(new SeasonGamificationDto()));
    ReflectionTestUtils.setField(listener, "ladsGamificationTopic", "cms-gamification");
  }

  @After
  public void verify() {
    then(context)
        .should()
        .upload(
            brand,
            "api/ladbrokes/one-two-free",
            "gamification",
            Collections.singletonList(new GamificationDetailsPublicDto()));
    then(context)
        .should()
        .upload(
            brand,
            "api/ladbrokes/one-two-free",
            "current-future-seasons",
            Collections.singletonList(new SeasonGamificationDto()));
  }
}
