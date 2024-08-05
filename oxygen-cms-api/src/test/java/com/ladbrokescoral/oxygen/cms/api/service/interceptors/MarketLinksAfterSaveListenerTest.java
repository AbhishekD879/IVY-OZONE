package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.MarketLink;
import com.ladbrokescoral.oxygen.cms.api.service.MarketLinkService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;

@RunWith(Parameterized.class)
public class MarketLinksAfterSaveListenerTest extends AbstractAfterSaveListenerTest<MarketLink> {
  @Mock private MarketLinkService service;
  @Getter @InjectMocks private MarketLinksAfterSaveListener listener;

  @Getter @Mock private MarketLink entity;
  @Getter private List<MarketLink> collection = Arrays.asList(entity);

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "market-links"},
          {"ladbrokes", "api/ladbrokes", "market-links"}
        });
  }

  @Before
  public void init() {
    given(service.getMarketLinksByBrand(anyString())).willReturn(this.getCollection());
  }
}
