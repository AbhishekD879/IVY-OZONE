package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipMappingPublicDto;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipMapping;
import com.ladbrokescoral.oxygen.cms.api.service.LuckyDipMappingPublicService;
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
public class LuckyDipMappingAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<LuckyDipMapping> {

  @Mock LuckyDipMappingPublicService luckyDipMappingPublicService;

  @Getter @Mock private LuckyDipMapping entity;

  @Getter @InjectMocks private LuckyDipMappingAfterSaveListener listener;

  @Getter private List<?> collection = null;

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"ladbrokes", "api/ladbrokes", "lucky-dip-mapping"}});
  }

  @Before
  public void init() {
    given(luckyDipMappingPublicService.findAllActiveLuckyDipMappingsByBrand(anyString()))
        .willReturn(Collections.singletonList(new LuckyDipMappingPublicDto()));
  }

  @After
  public void verify() {
    then(context)
        .should()
        .upload(
            brand,
            "api/ladbrokes",
            "lucky-dip-mapping",
            Collections.singletonList(new LuckyDipMappingPublicDto()));
  }
}
