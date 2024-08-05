package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.OtfGameTabsDto;
import com.ladbrokescoral.oxygen.cms.api.entity.OtfGameTabs;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.OtfGameTabPublicService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;

@RunWith(Parameterized.class)
public class OtfGameTabsListenerTest extends AbstractAfterSaveListenerTest<OtfGameTabs> {

  @Mock OtfGameTabPublicService otfGameTabPublicService;

  @Getter @Mock private OtfGameTabs entity;

  @Getter @InjectMocks private OtfGameTabsListener listener;

  @Getter private List<OtfGameTabsDto> collection = Arrays.asList(new OtfGameTabsDto());

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {{"ladbrokes", "api/ladbrokes/one-two-free", "otf-tab-config"}});
  }

  @Before
  public void init() {
    given(otfGameTabPublicService.findByBrand(anyString())).willReturn(this.getCollection());
  }
}
