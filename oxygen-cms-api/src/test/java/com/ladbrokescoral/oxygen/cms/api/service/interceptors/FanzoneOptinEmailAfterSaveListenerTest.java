package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneOptinEmail;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesOptinEmailService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;

@RunWith(Parameterized.class)
public class FanzoneOptinEmailAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<FanzoneOptinEmail> {

  @Mock private FanzonesOptinEmailService service;
  @Getter @InjectMocks private FanzoneOptinEmailAfterSaveListener listener;
  @Getter @Mock private FanzoneOptinEmail entity;
  @Getter @Mock private List<FanzoneOptinEmail> collection = Arrays.asList(entity);

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "fanzone-optin-email"},
          {"connect", "api/connect", "fanzone-optin-email"}
        });
  }

  @Before
  public void init() {
    given(service.findByBrand(anyString())).willReturn(this.getCollection());
  }
}
