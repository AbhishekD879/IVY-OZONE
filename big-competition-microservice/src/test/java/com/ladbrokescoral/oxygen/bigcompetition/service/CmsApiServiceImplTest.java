package com.ladbrokescoral.oxygen.bigcompetition.service;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.bigcompetition.service.impl.CmsApiServiceImpl;
import com.ladbrokescoral.oxygen.cms.client.api.CmsApiClient;
import com.ladbrokescoral.oxygen.cms.client.model.BybWidgetDto;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class CmsApiServiceImplTest {

  private CmsApiServiceImpl cmsApiService;

  @Mock CmsApiClient cmsApiClient;

  private static final String BRAND = "ladbrokes";

  @Before
  public void setup() {
    cmsApiService = new CmsApiServiceImpl(cmsApiClient);
  }

  @Test
  public void testGetBybWidget() {

    when(cmsApiClient.getBybWidget(BRAND)).thenReturn(Optional.empty());
    Optional<BybWidgetDto> bybWidget = cmsApiService.getBybWidget(BRAND);
    assertFalse(bybWidget.isPresent());
  }
}
