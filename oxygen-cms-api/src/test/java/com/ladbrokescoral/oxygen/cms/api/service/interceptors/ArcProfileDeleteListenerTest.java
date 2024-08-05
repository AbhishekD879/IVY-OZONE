package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.ArcProfileDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ArcProfile;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.ArcProfilePublicService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.bson.Document;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;

@RunWith(Parameterized.class)
public class ArcProfileDeleteListenerTest extends AbstractAfterDeleteListenerModelTest {
  @Mock private ArcProfilePublicService arcProfilePublicService;
  @Getter @InjectMocks private ArcProfileSaveListener listener;
  @Getter @Spy ArcProfile entity = new ArcProfile();
  // @Getter @Spy ArcProfileDto model = new ArcProfileDto();
  @Getter private ArcProfileDto arcProfileDto = new ArcProfileDto();
  @Getter private List<ArcProfileDto> collection = Arrays.asList(new ArcProfileDto());
  @Getter private Document model = new Document();

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"bma", "api/bma/arc-profile/2", "1"}});
  }

  @Before
  public void init() {
    model.put("modelRiskLevel", 2);
    model.put("reasonCode", 1);
    model.put("brand", "bma");

    entity.setModelRiskLevel(2);
    entity.setReasonCode(1);
    entity.setBrand("bma");
  }
}
