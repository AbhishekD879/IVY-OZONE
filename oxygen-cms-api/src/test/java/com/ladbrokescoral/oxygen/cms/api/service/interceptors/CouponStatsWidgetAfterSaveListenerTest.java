package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.CouponStatsWidgetCFDto;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CouponStatsWidget;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.CouponStatsWidgetService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.modelmapper.ModelMapper;
import org.springframework.context.annotation.Import;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;

@RunWith(Parameterized.class)
@Import(ModelMapperConfig.class)
public class CouponStatsWidgetAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<CouponStatsWidget> {

  @InjectMocks private CouponStatsWidgetService service;
  @Getter private CouponStasWidgetAfterSaveListener listener;
  @Getter private CouponStatsWidget entity = null;
  @Getter private List<CouponStatsWidget> collection = null;
  ModelMapper mapper = new ModelMapper();

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "coupon-stats-widget"},
          {"connect", "api/connect", "coupon-stats-widget"}
        });
  }

  public CouponStatsWidgetCFDto getModelClass() {
    return mapper.map(getEntity(), CouponStatsWidgetCFDto.class);
  }

  @Before
  public void init() {
    entity = new CouponStatsWidget();
    entity.setButtonText("Thanks");
    entity.setImageUrl("/images/image");
    entity.setIsEnable(true);
    service = new CouponStatsWidgetService(null, null, null, null, mapper);
    listener = new CouponStasWidgetAfterSaveListener(service, context);
  }

  @Test
  public void shouldAfterSaveEvent() throws Exception {

    // given
    entity.setBrand(brand);

    // when
    this.getListener().onAfterSave(new AfterSaveEvent<CouponStatsWidget>(entity, null, "11"));

    then(context).should().upload(brand, path, filename, getModelClass());
  }

  @After
  public void shouldHaveNoMoreInteractions() {
    then(context).shouldHaveNoMoreInteractions();
  }
}
