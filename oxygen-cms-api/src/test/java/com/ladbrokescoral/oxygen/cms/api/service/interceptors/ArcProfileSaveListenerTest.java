package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.ArcProfileDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ArcProfile;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.ArcProfilePublicService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;

@RunWith(Parameterized.class)
public class ArcProfileSaveListenerTest extends AbstractAfterSaveListenerModelTest {
  @Mock private ArcProfilePublicService arcProfilePublicService;
  @Getter @InjectMocks private ArcProfileSaveListener listener;
  @Getter @Spy ArcProfile entity = new ArcProfile();
  @Getter @Spy ArcProfileDto model = new ArcProfileDto();
  @Getter private ArcProfileDto arcProfileDto = new ArcProfileDto();
  @Getter private List<ArcProfileDto> collection = Arrays.asList(new ArcProfileDto());

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"bma", "api/bma/arc-profile/2", "1"}});
  }

  @Before
  public void init() {
    model.setModelRiskLevel("2");
    model.setReasonCode("1");
    model.setBrand("bma");
    entity.setModelRiskLevel(2);
    entity.setReasonCode(1);
    entity.setBrand("bma");
    given(
            arcProfilePublicService.findArcProfileByBrandAndModelRiskLevelAndReasonCode(
                anyString(), any(), any()))
        .willReturn(model);
  }
}
