package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.RGYConfigurationEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.RGYMetaInfoEntity;
import com.ladbrokescoral.oxygen.cms.api.service.RGYConfigService;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;

@RunWith(Parameterized.class)
public class RGYGlobalSwitchAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<RGYMetaInfoEntity> {

  @Getter @InjectMocks private RGYGlobalSwitchAfterSaveListener listener;

  @Getter @Mock private RGYMetaInfoEntity entity;

  @Mock private RGYConfigService rgyConfigService;

  @Getter @Mock
  private final List<RGYConfigurationEntity> collection =
      Arrays.asList(new RGYConfigurationEntity());

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"bma", "api/bma", "rgy-config"}});
  }

  @Before
  public void init() {
    given(rgyConfigService.readByBrandAndBonusSuppressionTrue(Mockito.any()))
        .willReturn(getCollection());
  }

  @Test
  public void shouldAfterSaveEvent() throws Exception {

    // given
    given(getEntity().getBrand()).willReturn(brand);

    // when
    this.getListener().onAfterSave(new AfterSaveEvent<RGYMetaInfoEntity>(getEntity(), null, "11"));

    // then
    then(context).should().upload(brand, path, filename, Collections.emptyList());
  }

  @Test
  public void shouldAfterSaveEventTrue() throws Exception {

    // given
    given(getEntity().getBrand()).willReturn(brand);
    given(getEntity().isRgyEnabled()).willReturn(true);

    // when
    this.getListener().onAfterSave(new AfterSaveEvent<RGYMetaInfoEntity>(getEntity(), null, "11"));

    // then
    then(context).should().upload(brand, path, filename, getCollection());
  }
}
