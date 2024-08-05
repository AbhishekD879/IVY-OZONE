package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.BottomMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BottomMenu;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BottomMenuPublicService;
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
public class BottomMenuAfterSaveListenerTest extends AbstractAfterSaveListenerTest<BottomMenu> {

  @Mock private BottomMenuPublicService service;
  @Getter @InjectMocks private BottomMenuAfterSaveListener listener;

  @Getter @Mock private BottomMenu entity;
  @Getter private List<BottomMenuDto> collection = Arrays.asList(new BottomMenuDto());

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "bottom-menu"},
          {"connect", "api/connect", "bottom-menu"}
        });
  }

  @Before
  public void init() {

    given(service.findByBrand(anyString())).willReturn(this.getCollection());
  }
}
