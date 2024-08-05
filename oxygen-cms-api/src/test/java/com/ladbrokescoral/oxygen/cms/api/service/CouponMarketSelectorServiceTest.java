package com.ladbrokescoral.oxygen.cms.api.service;

import static org.assertj.core.api.AssertionsForClassTypes.assertThatThrownBy;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.entity.CouponMarketSelector;
import com.ladbrokescoral.oxygen.cms.api.repository.CouponMarketSelectorRepository;
import java.util.Arrays;
import java.util.UUID;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class CouponMarketSelectorServiceTest {

  @Mock private CouponMarketSelectorRepository couponMarketSelectorRepository;

  @InjectMocks private CouponMarketSelectorService couponMarketSelectorService;

  @Test
  public void saveHappyPath() {
    CouponMarketSelector couponMarketSelector = couponMarketSelector();

    couponMarketSelectorService.save(couponMarketSelector);

    verify(couponMarketSelectorRepository).save(couponMarketSelector);
  }

  @Test
  public void saveTemplateMarketNameNotUnique() {
    String templateName = "nonUnique";

    CouponMarketSelector couponMarketSelector = couponMarketSelector();
    couponMarketSelector.setTemplateMarketName(templateName);

    when(couponMarketSelectorRepository.existsByTemplateMarketNameAndIdNotAndBrandIs(
            templateName, couponMarketSelector.getId(), couponMarketSelector.getBrand()))
        .thenReturn(true);

    assertThatThrownBy(() -> couponMarketSelectorService.save(couponMarketSelector))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessage("CouponMarketSelector.templateMarketName must be unique within the same brand");

    verify(couponMarketSelectorRepository, never()).save(couponMarketSelector);
  }

  private CouponMarketSelector couponMarketSelector() {
    CouponMarketSelector couponMarketSelector = new CouponMarketSelector();

    couponMarketSelector.setId(UUID.randomUUID().toString());
    couponMarketSelector.setBrand("brand");
    couponMarketSelector.setTitle("title");
    couponMarketSelector.setHeader(Arrays.asList("header-1", "header-2"));
    couponMarketSelector.setTemplateMarketName("template-name");

    return couponMarketSelector;
  }
}
