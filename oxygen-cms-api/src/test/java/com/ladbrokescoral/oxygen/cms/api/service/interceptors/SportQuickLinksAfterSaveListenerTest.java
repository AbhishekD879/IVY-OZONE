package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.SportQuickLinkDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportQuickLink;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SportQuickLinkPublicService;
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
public class SportQuickLinksAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<SportQuickLink> {
  @Mock private LadsCoralKafkaPublisher ladsCoralKafkaPublisher;
  @Mock private SportQuickLinkPublicService service;
  @Getter @InjectMocks private SportQuickLinksAfterSaveListener listener;

  @Getter @Mock private SportQuickLink entity;
  @Getter @Mock private SportQuickLinkDto model;

  @Getter private List<SportQuickLinkDto> collection = Arrays.asList(model);

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "sport-quick-links"},
          {"connect", "api/connect", "sport-quick-links"}
        });
  }

  @Before
  public void init() {
    given(service.findAll(anyString())).willReturn(this.getCollection());
    ReflectionTestUtils.setField(
        listener, "coralSportquicklinksTopic", "coral-cms-sportquicklinks");
    ReflectionTestUtils.setField(listener, "ladsSportquicklinksTopic", "cms-sportquicklinks");
  }
}
