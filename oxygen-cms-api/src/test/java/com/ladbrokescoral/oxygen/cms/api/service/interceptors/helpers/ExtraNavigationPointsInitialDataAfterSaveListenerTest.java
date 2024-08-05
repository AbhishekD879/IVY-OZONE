package com.ladbrokescoral.oxygen.cms.api.service.interceptors.helpers;

import com.ladbrokescoral.oxygen.cms.api.dto.InitialDataCFDto;
import com.ladbrokescoral.oxygen.cms.api.dto.InitialDataDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ExtraNavigationPoint;
import com.ladbrokescoral.oxygen.cms.api.service.InitialDataService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.interceptors.AbstractAfterSaveListenerTest;
import com.ladbrokescoral.oxygen.cms.util.CustomExecutors;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.ExecutorService;
import lombok.Getter;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;

@RunWith(Parameterized.class)
public class ExtraNavigationPointsInitialDataAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<ExtraNavigationPoint> {

  @Mock private InitialDataService service;
  @Mock private CustomExecutors customExecutors;
  @Mock private DeliveryNetworkService deliveryNetworkService;

  @Getter @InjectMocks private ExtraNavigationPointsInitialDataAfterSaveListener listener;

  @Getter @Mock private ExtraNavigationPoint entity;
  @Getter private List<?> collection = null;

  private InitialDataDto data = new InitialDataDto();

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"bma", "api/bma/initial-data", null}});
  }

  @Before
  public void init() {
    ExecutorService executorService = mock(ExecutorService.class);
    given(customExecutors.getSingleThreadLastTaskExecutor(brand)).willReturn(executorService);

    doAnswer(
            invocation -> {
              ((Runnable) invocation.getArgument(0)).run();
              return null;
            })
        .when(executorService)
        .execute(any());

    given(service.fetchInitialData(anyString(), anyString(), anyString())).willReturn(data);
    given(service.fetchCFInitialData(anyString(), anyString())).willReturn(new InitialDataCFDto());
  }

  @Test
  public void shouldAfterSaveEvent() throws Exception {

    // given
    given(getEntity().getBrand()).willReturn(brand);

    // when
    this.getListener()
        .onAfterSave(
            new AfterSaveEvent<ExtraNavigationPoint>(getEntity(), null, "extranavigationPoint"));

    // then
    if (null != getCollection()) {
      then(context).should().upload(brand, path, filename, getCollection());
    }
  }

  @After
  public void verify() {

    then(context).should().upload(brand, path, "mobile", data);
    then(context).should().upload(brand, path, "tablet", data);
    then(context).should().upload(brand, path, "desktop", data);
    then(context)
        .should()
        .uploadCFContent(brand, "api/bma/cf/initial-data", "mobile", new InitialDataCFDto());
  }
}