package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.CouponAndMarketSwitcherCFDto;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CouponAndMarketSwitcher;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.CouponAndMarketSwitcherWidgetService;
import java.time.Instant;
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
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;

@RunWith(Parameterized.class)
public class CouponAndMarketSwitcherWidgetListenerTest
    extends AbstractAfterSaveListenerTest<CouponAndMarketSwitcher> {
  @InjectMocks private CouponAndMarketSwitcherWidgetService service;
  @Getter private CouponAndMarketSwitcherWidgetListener listener;
  @Getter private CouponAndMarketSwitcher entity = null;
  @Getter private List<CouponAndMarketSwitcher> collection = null;
  ModelMapper mapper = new ModelMapper();

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"bma", "api/bma", "couponAndMarketSwitcherWidget"}});
  }

  public CouponAndMarketSwitcherCFDto getModelClass() {
    return mapper.map(getEntity(), CouponAndMarketSwitcherCFDto.class);
  }

  @Before
  public void init() {
    entity = createEntity();
    service = new CouponAndMarketSwitcherWidgetService(null, mapper, null, null, null);
    listener = new CouponAndMarketSwitcherWidgetListener(service, context);
  }

  private CouponAndMarketSwitcher createEntity() {
    CouponAndMarketSwitcher entity = new CouponAndMarketSwitcher();
    entity.setButtonText("Ok,Thanks!");
    entity.setBrand("ladbrokes");
    entity.setIsEnable(true);
    entity.setImageUrl("file.svg");
    entity.setId("121");
    entity.setCreatedBy("system");
    entity.setUpdatedAt(Instant.now());
    return entity;
  }

  @Test
  public void shouldAfterSaveEvent() throws Exception {
    entity.setBrand(brand);
    this.getListener().onAfterSave(new AfterSaveEvent<CouponAndMarketSwitcher>(entity, null, "11"));
    then(context).should().upload(brand, path, filename, getModelClass());
  }

  @After
  public void shouldHaveNoMoreInteractions() {
    then(context).shouldHaveNoMoreInteractions();
  }
}
