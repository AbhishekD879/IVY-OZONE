package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.BadgeDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Badge;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BadgePublicService;
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
public class BadgeAfterSaveListenerTest extends AbstractAfterSaveListenerTest<Badge> {

  @Mock BadgePublicService badgePublicService;

  @Getter @Mock private Badge entity;

  @Getter @InjectMocks private BadgeAfterSaveListener listener;

  @Getter private List<BadgeDto> collection = Arrays.asList(new BadgeDto());

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"ladbrokes", "api/ladbrokes/one-two-free", "badge"}});
  }

  @Before
  public void init() {
    given(badgePublicService.findAllByBrand(anyString())).willReturn(this.getCollection());
  }
}
