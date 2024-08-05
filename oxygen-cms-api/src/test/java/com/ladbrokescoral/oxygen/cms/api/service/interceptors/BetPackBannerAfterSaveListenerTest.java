package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackBanner;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BetPackMarketPlacePublicBannerService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.After;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;

@RunWith(Parameterized.class)
public class BetPackBannerAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<BetPackBanner> {

  @Mock private BetPackMarketPlacePublicBannerService service;

  @Getter @InjectMocks private BetPackBannerAfterSaveListener listener;

  @Getter @Spy private BetPackBanner entity = new BetPackBanner();

  @Getter private final List<BetPackBanner> collection = null;

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"bma", "api/bma/bet-pack", "banner"}});
  }

  @Before
  public void init() {
    given(service.getBetPackBannerByBrand(anyString())).willReturn(Arrays.asList(entity));
  }

  @After
  public void verify() {
    then(context).should().upload(brand, "api/bma/bet-pack", filename, entity);
  }
}
