package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.SportPageConfigDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SportTabConfigListDto;
import com.ladbrokescoral.oxygen.cms.api.entity.TrendingTab;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SportCategoryPublicService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.bson.Document;
import org.junit.After;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;
import org.springframework.test.util.ReflectionTestUtils;

@RunWith(Parameterized.class)
public class TrendingTabAfterSaveListenerTest extends AbstractAfterSaveListenerTest<TrendingTab> {

  @Mock private SportCategoryPublicService sportCategoryPublicService;
  @Mock private DeliveryNetworkService deliveryNetworkService;

  @Getter @InjectMocks private TrendingTabAfterSaveListener listener;

  @Getter @Spy private TrendingTab entity;
  @Getter private List<?> collection = null;
  @Mock private LadsCoralKafkaPublisher ladsCoralKafkaPublisher;
  private SportTabConfigListDto data1 = SportTabConfigListDto.builder("sport/tennis").build();
  private SportPageConfigDto data2 = SportPageConfigDto.builder().build();
  @Getter private Document model = new Document();

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma/sport-tabs", "100"},
          {"connect", "api/connect/sport-tabs", "100"}
        });
  }

  @Before
  public void init() {

    ReflectionTestUtils.setField(listener, "coralSporttabsTopic", "coral-cms-sporttabs");
    ReflectionTestUtils.setField(listener, "ladsSporttabsTopic", "cms-sporttabs");
    entity.setSportId(Integer.valueOf(filename));
    given(sportCategoryPublicService.getSportTabs(anyString(), anyInt())).willReturn(data1);
    given(sportCategoryPublicService.getSportConfig(anyString(), anyInt())).willReturn(data2);
  }

  @After
  public void verify() {
    if ("bma".equals(brand)) {
      then(context).should().upload(brand, "api/bma/sport-tabs", filename, data1);
      then(context).should().upload(brand, "api/bma/sport-config", filename, data2);
    }
    if ("connect".equals(brand)) {
      then(context).should().upload(brand, "api/connect/sport-tabs", filename, data1);
      then(context).should().upload(brand, "api/connect/sport-config", filename, data2);
    }
  }
}
