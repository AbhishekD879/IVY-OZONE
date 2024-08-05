package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.DesktopQuickLinkDto;
import com.ladbrokescoral.oxygen.cms.api.entity.DesktopQuickLink;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.DesktopQuickLinkPublicService;
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
public class DesktopQuickLinksAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<DesktopQuickLink> {

  @Mock private DesktopQuickLinkPublicService service;
  @Getter @InjectMocks private DesktopQuickLinksAfterSaveListener listener;

  @Getter @Mock private DesktopQuickLink entity;

  @Getter private List<DesktopQuickLinkDto> collection = Arrays.asList(new DesktopQuickLinkDto());

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "desktop-quick-links"},
          {"connect", "api/connect", "desktop-quick-links"}
        });
  }

  @Before
  public void init() {

    given(service.findByBrand(anyString())).willReturn(this.getCollection());
  }
}
