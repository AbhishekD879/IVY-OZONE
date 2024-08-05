package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.BaseModularContentDto;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.ModularContentPublicService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import java.util.*;
import lombok.Getter;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.test.util.ReflectionTestUtils;

@RunWith(Parameterized.class)
public class HomeModuleContentAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<HomeModule> {
  @Mock private ModularContentPublicService service;
  @Getter @InjectMocks private HomeModuleContentAfterSaveListener listener;

  @Getter @Mock private HomeModule entity;
  @Mock private LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Getter
  private List<BaseModularContentDto> collection = Arrays.asList(new BaseModularContentDto() {});

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "modular-content"}, {"connect", "api/connect", "modular-content"}
        });
  }

  @Before
  public void init() {
    ReflectionTestUtils.setField(listener, "coralHomemodulesTopic", "coral-cms-homemodules");
    ReflectionTestUtils.setField(listener, "ladsHomemodulesTopic", "cms-homemodules");
    given(service.findByBrand(anyString())).willReturn(this.getCollection());
  }

  @Test
  public void shouldAfterSaveEvent() throws Exception {
    given(service.findByBrand(anyString())).willReturn(this.getCollection());
    if ("bma".equals(brand)) {
      // given
      given(getEntity().getBrand()).willReturn(brand);
      given(getEntity().getId()).willReturn("12");
      given(getEntity().getPublishToChannels()).willReturn(Arrays.asList("bma"));

      // when
      this.getListener().onAfterSave(new AfterSaveEvent<HomeModule>(getEntity(), null, "bma"));

      // then
      if (null != getCollection()) {
        then(context).should().upload(brand, path, filename, getCollection());
      }
    }
    if ("connect".equals(brand)) {
      given(getEntity().getBrand()).willReturn(brand);
      given(getEntity().getId()).willReturn("12");
      given(getEntity().getPublishToChannels()).willReturn(Arrays.asList("connect"));

      // when
      this.getListener().onAfterSave(new AfterSaveEvent<HomeModule>(getEntity(), null, "bma"));

      // then
      if (null != getCollection()) {
        then(context).should().upload(brand, path, filename, getCollection());
      }
    }
  }

  @After
  public void shouldHaveNoMoreInteractions() {}
}
