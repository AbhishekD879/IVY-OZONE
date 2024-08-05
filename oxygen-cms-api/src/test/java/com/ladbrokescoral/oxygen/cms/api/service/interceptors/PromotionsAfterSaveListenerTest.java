package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.PromotionContainerDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PromotionDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PromotionV2Dto;
import com.ladbrokescoral.oxygen.cms.api.dto.PromotionWithSectionContainerDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Promotion;
import com.ladbrokescoral.oxygen.cms.api.service.PromotionSectionService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.PromotionPublicService;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.ExecutorService;
import lombok.Getter;
import org.junit.After;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.mockito.Mock;

@RunWith(Parameterized.class)
public class PromotionsAfterSaveListenerTest extends AbstractAfterSaveListenerTest<Promotion> {

  @Mock private PromotionPublicService service;
  @Mock private PromotionSectionService promotionSectionService;
  @Mock private ExecutorService executorService;

  @Getter @InjectMocks private PromotionsAfterSaveListener listener;

  @Getter @Mock private Promotion entity;

  @Getter private List<PromotionContainerDto<?>> collection = null;

  private PromotionWithSectionContainerDto dto = new PromotionWithSectionContainerDto();
  private PromotionContainerDto<PromotionDto> dto1 = new PromotionContainerDto<PromotionDto>();
  private PromotionContainerDto<PromotionV2Dto> dto2 = new PromotionContainerDto<PromotionV2Dto>();

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"bma", null, null}});
  }

  @Before
  public void init() {

    doAnswer(
            invocation -> {
              ((Runnable) invocation.getArgument(0)).run();
              return null;
            })
        .when(executorService)
        .execute(any());

    given(service.findByBrandGroupedBySections(anyString()))
        .willReturn(new PromotionWithSectionContainerDto());

    given(service.findByBrand(anyString())).willReturn(new PromotionContainerDto<PromotionDto>());

    given(service.findByBrandAndCategories(anyString(), anyString()))
        .willReturn(new PromotionContainerDto<PromotionV2Dto>());
  }

  @After
  public void verify() {

    then(context).should().upload(brand, "api/bma", "promotions", dto1);
    then(context).should().upload(brand, "api/bma", "grouped-promotions", dto);
    then(context).should().upload(brand, "api/v2/bma/promotions", "1", dto2);
    then(context).should().upload(brand, "api/v2/bma/promotions", "2", dto2);
    then(context).should().upload(brand, "api/v2/bma/promotions", "3", dto2);
    then(context).should().upload(brand, "api/v2/bma/promotions", "1000", dto2);
    then(context).should().upload(brand, "api/v2/bma/promotions", "19998", dto2);
    then(context).should().upload(brand, "api/v3/bma", "promotions_1", dto2);
    then(context).should().upload(brand, "api/v3/bma", "promotions_2", dto2);
    then(context).should().upload(brand, "api/v3/bma", "promotions_3", dto2);
    then(context).should().upload(brand, "api/v3/bma", "promotions_1000", dto2);
    then(context).should().upload(brand, "api/v3/bma", "promotions_19998", dto2);
  }
}
