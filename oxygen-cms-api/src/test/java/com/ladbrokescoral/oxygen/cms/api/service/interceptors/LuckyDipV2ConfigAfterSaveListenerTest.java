package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipV2ConfigurationPublicDto;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipV2Config;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.LuckyDipV2ConfigPublicProcessor;
import java.io.IOException;
import java.util.Arrays;
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
public class LuckyDipV2ConfigAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<LuckyDipV2Config> {
  @Mock LuckyDipV2ConfigPublicProcessor luckyDipV2ConfigPublicProcessor;

  @Getter @Mock private LuckyDipV2Config entity;

  @Getter @InjectMocks private LuckyDipV2ConfigAfterSaveListener listener;

  @Getter private List<?> collection = null;

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"ladbrokes", "api/ladbrokes", "lucky-dip"}});
  }

  List<LuckyDipV2ConfigurationPublicDto> luckyDipV2Configs;

  @Before
  public void init() throws IOException {
    luckyDipV2Configs =
        TestUtil.deserializeWithJackson("controller/private_api/lucky-dip-config.json", List.class);
    given(luckyDipV2ConfigPublicProcessor.getAllActiveLDByBrand(anyString()))
        .willReturn(luckyDipV2Configs);
  }

  @After
  public void verify() {
    then(context).should().upload(brand, "api/ladbrokes", "lucky-dip", luckyDipV2Configs);
  }
}
