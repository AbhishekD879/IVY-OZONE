package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipConfigurationPublicDto;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipConfiguration;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.LuckyDipConfigPublicService;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import lombok.Getter;
import org.junit.After;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.mockito.Mock;

@RunWith(Parameterized.class)
public class LuckyDipConfigAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<LuckyDipConfiguration> {
  @Mock LuckyDipConfigPublicService configPublicService;

  @Getter @Mock private LuckyDipConfiguration entity;

  @Getter @InjectMocks private LuckyDipConfigAfterSaveListener listener;

  @Getter private List<?> collection = null;

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"ladbrokes", "api/ladbrokes", "luckydip"}});
  }

  @Before
  public void init() {
    given(configPublicService.getAllLuckyDipConfigByBrand(anyString()))
        .willReturn(Collections.singletonList(new LuckyDipConfigurationPublicDto()));
  }

  @After
  public void verify() {
    then(context)
        .should()
        .upload(
            brand,
            "api/ladbrokes",
            "luckydip",
            Collections.singletonList(new LuckyDipConfigurationPublicDto()));
  }
}
