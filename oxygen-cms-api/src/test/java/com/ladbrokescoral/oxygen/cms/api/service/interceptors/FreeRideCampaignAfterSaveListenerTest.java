package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.FreeRidePublicCampaignDto;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.FreeRideCampaign;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.FreeRideCampaignPublicService;
import java.util.ArrayList;
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
public class FreeRideCampaignAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<FreeRideCampaign> {

  @Mock private FreeRideCampaignPublicService freeRideCampaignPublicService;

  @Getter @Mock private FreeRideCampaign entity;

  @Getter @InjectMocks private FreeRideCampaignAfterSaveListener listener;

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"ladbrokes", "api/ladbrokes", "freeride-campaign"},
          {"connect", "api/connect", "freeride-campaign"}
        });
  }

  @Before
  public void init() {
    given(freeRideCampaignPublicService.getAllCampaignByBrand(anyString()))
        .willReturn(this.getCollection());
  }

  @Override
  protected List<FreeRidePublicCampaignDto> getCollection() {
    List<FreeRidePublicCampaignDto> campaignList = new ArrayList<>();
    FreeRidePublicCampaignDto freeRidePublicCampaignDto = new FreeRidePublicCampaignDto();
    freeRidePublicCampaignDto.setBrand("BMA");
    campaignList.add(freeRidePublicCampaignDto);
    return campaignList;
  }
}
