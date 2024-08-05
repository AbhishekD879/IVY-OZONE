package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackOnboarding;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BetPackMarketPlacePublicOnboardingService;
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
public class BetPackOnboardingAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<BetPackOnboarding> {

  @Mock private BetPackMarketPlacePublicOnboardingService service;

  @Getter @InjectMocks private BetPackOnboardingAfterSaveListener listener;

  @Getter @Spy private BetPackOnboarding entity = new BetPackOnboarding();

  @Getter private final List<BetPackOnboarding> collection = null;

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"bma", "api/bma/bet-pack", "onboarding"}});
  }

  @Before
  public void init() {
    given(service.getBpmpOnboardingByBrand(anyString())).willReturn(Arrays.asList(entity));
  }

  @After
  public void verify() {
    then(context).should().upload(brand, "api/bma/bet-pack", filename, entity);
  }
}
