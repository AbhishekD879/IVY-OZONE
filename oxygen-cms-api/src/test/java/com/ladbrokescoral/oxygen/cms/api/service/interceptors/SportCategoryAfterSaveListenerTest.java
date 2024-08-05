package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.SportCategoryDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SportPageConfigDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SportCategoryPublicService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
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
import org.mockito.Mock;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.test.util.ReflectionTestUtils;

@RunWith(Parameterized.class)
public class SportCategoryAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<SportCategory> {

  @Mock private SportCategoryPublicService service;
  @Getter @InjectMocks private SportCategoryAfterSaveListener listener;

  @Getter @Mock private SportCategory entity;
  @Mock private LadsCoralKafkaPublisher ladsCoralKafkaPublisher;
  @Getter private List<SportCategoryDto> collection = Arrays.asList(new SportCategoryDto());

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "sport-category"},
          {"connect", "api/connect", "sport-category"}
        });
  }

  @Before
  public void init() {
    ReflectionTestUtils.setField(
        listener, "coralSportcategoriesTopic", "coral-cms-sportcategories");
    ReflectionTestUtils.setField(listener, "ladsSportcategoriesTopic", "cms-sportcategories");
    given(service.findByBrand(anyString())).willReturn(this.getCollection());
  }

  @Test
  public void shouldAfterSaveEvent() throws Exception {
    given(service.findByBrand(anyString())).willReturn(this.getCollection());

    // given
    given(getEntity().getBrand()).willReturn(brand);
    given(getEntity().getCategoryId()).willReturn(16);
    given(getEntity().getTier()).willReturn(SportTier.TIER_1);
    given(service.getSportConfig(anyString(), anyInt()))
        .willReturn(SportPageConfigDto.builder().build());

    // when
    this.getListener()
        .onAfterSave(new AfterSaveEvent<SportCategory>(getEntity(), null, "sportcategories"));

    // then
    if (null != getCollection()) {
      then(context).should().upload(brand, path, filename, getCollection());
    }
  }

  @Test
  public void shouldAfterSaveEventNoupload() throws Exception {

    // given
    given(getEntity().getBrand()).willReturn(brand);
    given(getEntity().getCategoryId()).willReturn(null);
    given(service.findByBrand(anyString())).willReturn(this.getCollection());

    // when
    this.getListener()
        .onAfterSave(new AfterSaveEvent<SportCategory>(getEntity(), null, "sportcategories"));

    // then
    if (null != getCollection()) {
      then(context).should().upload(brand, path, filename, getCollection());
    }
  }

  @Test
  public void shouldAfterSaveEventNouploadWithTier() throws Exception {

    // given
    given(getEntity().getBrand()).willReturn(brand);
    given(getEntity().getCategoryId()).willReturn(16);
    given(getEntity().getTier()).willReturn(SportTier.UNTIED);
    given(service.findByBrand(anyString())).willReturn(this.getCollection());

    // when
    this.getListener()
        .onAfterSave(new AfterSaveEvent<SportCategory>(getEntity(), null, "sportcategories"));

    // then
    if (null != getCollection()) {
      then(context).should().upload(brand, path, filename, getCollection());
    }
  }

  @Test
  public void shouldAfterSaveEventWithArchivalEntity() throws Exception {

    // when
    this.getListener()
        .onAfterSave(new AfterSaveEvent<SportCategory>(getEntity(), null, "sportcategorArcive"));

    // then
    if (null != getCollection()) {
      then(context).shouldHaveNoInteractions();
    }
  }

  @After
  public void shouldHaveNoMoreInteractions() {}
}
