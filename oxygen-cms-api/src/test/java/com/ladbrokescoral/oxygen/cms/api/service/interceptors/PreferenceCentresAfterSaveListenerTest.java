package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.PreferenceCentre;
import com.ladbrokescoral.oxygen.cms.api.service.PreferenceCentresService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;

@RunWith(Parameterized.class)
public class PreferenceCentresAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<PreferenceCentre> {

  @Mock private PreferenceCentresService service;
  @Getter @InjectMocks private PreferenceCentresAfterSaveListener listener;
  @Getter @Mock private PreferenceCentre entity;
  @Getter @Mock private List<PreferenceCentre> collection = Arrays.asList(entity);

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "fanzone-preference-center"},
          {"connect", "api/connect", "fanzone-preference-center"}
        });
  }

  @Before
  public void init() {
    given(service.findByBrand(anyString())).willReturn(this.getCollection());
  }
}
