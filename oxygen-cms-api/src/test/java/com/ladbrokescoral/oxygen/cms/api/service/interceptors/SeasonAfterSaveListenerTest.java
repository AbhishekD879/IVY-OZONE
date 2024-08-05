package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.SeasonDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SeasonGamificationDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Season;
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
public class SeasonAfterSaveListenerTest extends AbstractAfterSaveListenerTest<Season> {

  @Mock SeasonPublicService seasonPublicService;

  @Getter @Mock private Season entity;

  @Getter @InjectMocks private SeasonAfterSaveListener listener;

  @Getter private List<?> collection = null;
  @Mock private LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"ladbrokes", "api/ladbrokes/one-two-free", "season"},
          {"ladbrokes", "api/ladbrokes/one-two-free", "current-future-seasons"}
        });
  }

  @Before
  public void init() {
    given(seasonPublicService.findAllByBrand(anyString()))
        .willReturn(Collections.singletonList(new SeasonDto()));
    given(seasonPublicService.getCurrentFutureSeasons(anyString()))
        .willReturn(Collections.singletonList(new SeasonGamificationDto()));
    ReflectionTestUtils.setField(listener, "ladsSeasonTopic", "cms-season");
  }

  @After
  public void verify() {
    then(context)
        .should()
        .upload(
            brand,
            "api/ladbrokes/one-two-free",
            "season",
            Collections.singletonList(new SeasonDto()));
    then(context)
        .should()
        .upload(
            brand,
            "api/ladbrokes/one-two-free",
            "current-future-seasons",
            Collections.singletonList(new SeasonGamificationDto()));
  }
}
