package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.ConnectMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ConnectMenu;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.ConnectMenuPublicService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.mockito.Mock;

@RunWith(Parameterized.class)
public class ConnectMenuAfterSaveListenerTest extends AbstractAfterSaveListenerTest<ConnectMenu> {

  @Mock private ConnectMenuPublicService service;
  @Getter @InjectMocks private ConnectMenuAfterSaveListener listener;

  @Getter @Mock private ConnectMenu entity;
  @Getter private List<ConnectMenuDto> collection = Arrays.asList(new ConnectMenuDto());

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "connect-menu"},
          {"connect", "api/connect", "connect-menu"}
        });
  }

  @Before
  public void init() {

    given(service.findByBrand(anyString())).willReturn(this.getCollection());
  }
}
