package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.BaseModularContentDto;
import com.ladbrokescoral.oxygen.cms.api.dto.ModularContentDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ModuleRibbonTab;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.ModularContentPublicService;
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
public class ModuleRibbonTabContentAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<ModuleRibbonTab> {

  @Mock private ModularContentPublicService service;
  @Getter @InjectMocks private ModuleRibbonTabContentAfterSaveListener listener;

  @Getter @Mock private ModuleRibbonTab entity;
  @Mock private LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Getter private List<BaseModularContentDto> collection = Arrays.asList(new ModularContentDto());

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "modular-content"},
          {"connect", "api/connect", "modular-content"}
        });
  }

  @Before
  public void init() {
    given(service.findByBrand(anyString())).willReturn(this.getCollection());
    ReflectionTestUtils.setField(
        listener, "coralModuleribbontabsTopic", "coral-cms-moduleribbontabs");
    ReflectionTestUtils.setField(listener, "ladsModuleribbontabsTopic", "cms-moduleribbontabs");
  }
}
