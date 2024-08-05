package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.SportCategoryNativeDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SportCategoryPublicService;
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
public class SportCategoryNativeAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<SportCategory> {

  @Mock private SportCategoryPublicService service;
  @Getter @InjectMocks private SportCategoryNativeAfterSaveListener listener;

  @Getter @Mock private SportCategory entity;
  @Mock private LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Getter
  private List<SportCategoryNativeDto> collection = Arrays.asList(new SportCategoryNativeDto());

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "sport-category-native"},
          {"connect", "api/connect", "sport-category-native"}
        });
  }

  @Before
  public void init() {
    ReflectionTestUtils.setField(
        listener, "coralSportcategoriesTopic", "coral-cms-sportcategories");
    ReflectionTestUtils.setField(listener, "ladsSportcategoriesTopic", "cms-sportcategories");
    given(service.findNative(anyString())).willReturn(this.getCollection());
  }
}
