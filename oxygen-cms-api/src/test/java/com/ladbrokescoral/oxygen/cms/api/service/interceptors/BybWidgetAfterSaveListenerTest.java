package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.BDDMockito.given;
import static org.mockito.BDDMockito.then;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.cms.api.dto.BybWidgetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BybWidget;
import com.ladbrokescoral.oxygen.cms.api.entity.BybWidgetData;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BybWidgetPublicService;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import lombok.Getter;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.jupiter.api.AfterEach;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnit;
import org.mockito.junit.MockitoRule;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;

@RunWith(Parameterized.class)
public class BybWidgetAfterSaveListenerTest {

  @Mock private BybWidgetPublicService service;
  @Getter @InjectMocks private BybWidgetAfterSaveListener listener;
  @Getter @InjectMocks private BybWidgetDataAfterSaveListener bybWidgetDatalistener;

  @Getter @Mock private BybWidget bybWidget;
  @Getter @Mock private BybWidgetData bybWidgetData;

  @Getter private BybWidgetDto collection = new BybWidgetDto();
  @Rule public MockitoRule rule = MockitoJUnit.rule();

  @Mock protected DeliveryNetworkService context;

  @Parameterized.Parameter(0)
  public String brand;

  @Parameterized.Parameter(1)
  public String path;

  @Parameterized.Parameter(2)
  public String filename;

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "byb-widgets"},
          {"connect", "api/connect", "byb-widgets"}
        });
  }

  @Before
  public void init() {
    bybWidget.setBrand(brand);
    given(service.readByBrand(anyString())).willReturn(Optional.of(this.getCollection()));
  }

  @Test
  public void shouldBybWidgetAfterSaveEvent() throws Exception {

    // given
    given(bybWidget.getBrand()).willReturn(brand);

    // when
    this.getListener().onAfterSave(new AfterSaveEvent<>(bybWidget, null, "11"));

    // then
    if (null != getCollection()) {
      then(context).should().upload(brand, path, filename, getCollection());
    }
    then(context).should(times(1)).upload(any(), any(), any(), any());
  }

  @Test
  public void shouldBybWidgetDataAfterSaveEvent() throws Exception {

    // given
    given(bybWidgetData.getBrand()).willReturn(brand);

    // when
    this.getBybWidgetDatalistener().onAfterSave(new AfterSaveEvent<>(bybWidgetData, null, "11"));

    // then
    if (null != getCollection()) {
      then(context).should().upload(brand, path, filename, getCollection());
    }
    then(context).should(times(1)).upload(any(), any(), any(), any());
  }

  @AfterEach
  public void shouldHaveNoMoreInteractions() {
    then(context).shouldHaveNoMoreInteractions();
  }
}
