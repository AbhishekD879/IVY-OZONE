package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.BDDMockito.given;
import static org.mockito.BDDMockito.then;
import static org.mockito.Mockito.times;

import com.ladbrokescoral.oxygen.cms.api.dto.PopularAccaWidgetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PopularAccaWidget;
import com.ladbrokescoral.oxygen.cms.api.entity.PopularAccaWidgetData;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.PopularAccaWidgetPublicService;
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
public class PopularAccaWidgetAfterSaveListenerTest {

  @Mock private PopularAccaWidgetPublicService service;
  @Getter @InjectMocks private PopularAccaWidgetAfterSaveListener listener;

  @Getter @InjectMocks
  private PopularAccaWidgetDataAfterSaveListener popularAccaWidgetDataAfterSaveListener;

  @Getter @Mock private PopularAccaWidget popularAccaWidget;
  @Getter @Mock private PopularAccaWidgetData popularAccaWidgetData;

  @Getter private PopularAccaWidgetDto collection = new PopularAccaWidgetDto();
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
          {"bma", "api/bma", "popular-acca-widgets"},
          {"connect", "api/connect", "popular-acca-widgets"}
        });
  }

  @Before
  public void init() {
    popularAccaWidget.setBrand(brand);
    given(service.readByBrand(anyString())).willReturn(Optional.of(this.getCollection()));
  }

  @Test
  public void shouldPopularAccaWidgetAfterSaveEvent() {

    // given
    given(popularAccaWidget.getBrand()).willReturn(brand);

    // when
    this.getListener().onAfterSave(new AfterSaveEvent<>(popularAccaWidget, null, "11"));

    // then
    if (null != getCollection()) {
      then(context).should().upload(brand, path, filename, getCollection());
    }
    then(context).should(times(1)).upload(any(), any(), any(), any());
  }

  @Test
  public void shouldPopularAccaWidgetDataAfterSaveEvent() {

    // given
    given(popularAccaWidgetData.getBrand()).willReturn(brand);

    // when
    this.getPopularAccaWidgetDataAfterSaveListener()
        .onAfterSave(new AfterSaveEvent<>(popularAccaWidgetData, null, "11"));

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
