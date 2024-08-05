package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.BankingMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BankingMenu;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BankingMenuPublicService;
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
public class BankingMenuAfterSaveListenerTest extends AbstractAfterSaveListenerTest<BankingMenu> {

  @Mock private BankingMenuPublicService service;
  @Getter @InjectMocks private BankingMenuAfterSaveListener listener;

  @Getter @Mock private BankingMenu entity;
  @Getter private List<BankingMenuDto> collection = Arrays.asList(new BankingMenuDto());

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "banking-menu"},
          {"connect", "api/connect", "banking-menu"}
        });
  }

  @Before
  public void init() {

    given(service.findByBrand(anyString())).willReturn(this.getCollection());
  }
}
