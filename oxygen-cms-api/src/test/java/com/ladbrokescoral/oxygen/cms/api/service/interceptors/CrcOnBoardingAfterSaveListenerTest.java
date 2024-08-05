package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding.CrcOnBoardingDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OnBoardDto;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CrcOnBoarding;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.OnBoardPublicService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.After;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;
import org.springframework.context.annotation.Import;

@RunWith(Parameterized.class)
@Import(ModelMapperConfig.class)
public class CrcOnBoardingAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<CrcOnBoarding> {
  @Mock private OnBoardPublicService service;

  @Getter @InjectMocks private CrcOnBoardingAfterSaveListener listener;

  @Getter @Spy private CrcOnBoarding entity = new CrcOnBoarding();

  @Getter @Spy private CrcOnBoardingDto dto = new CrcOnBoardingDto();

  @Getter private final List<CrcOnBoarding> collection = null;

  @Getter @Spy private OnBoardDto onBoardDto = new OnBoardDto();

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"bma", "api/bma/my-stable", "onboardings"}});
  }

  @Before
  public void init() {

    given(service.getOnBoard(anyString())).willReturn(onBoardDto);
  }

  @After
  public void verify() {
    then(context).should().upload(brand, "api/bma/my-stable", filename, Arrays.asList(onBoardDto));
  }
}
