package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.MyStableOnboardingCFDto;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.MyStableOnboarding;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.MyStableOnboardingService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.modelmapper.ModelMapper;
import org.springframework.context.annotation.Import;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;

@RunWith(Parameterized.class)
@Import(ModelMapperConfig.class)
public class MyStableOnboardingAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<MyStableOnboarding> {
  @InjectMocks private MyStableOnboardingService service;
  @Getter private MyStableOnboardingAfterSaveListener listener;
  @Getter private MyStableOnboarding entity = null;
  @Getter private List<MyStableOnboarding> collection = null;
  ModelMapper mapper = new ModelMapper();

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma/my-stable", "onboarding"},
          {"connect", "api/connect/my-stable", "onboarding"}
        });
  }

  public MyStableOnboardingCFDto getModelClass() {
    return mapper.map(getEntity(), MyStableOnboardingCFDto.class);
  }

  @Before
  public void init() {
    entity = new MyStableOnboarding();
    entity.setButtonText("Thanks");
    entity.setImageUrl("/images/image");
    entity.setIsEnable(true);
    service = new MyStableOnboardingService(null, null, null, null, mapper);
    listener = new MyStableOnboardingAfterSaveListener(service, context);
  }

  @Test
  public void shouldAfterSaveEvent() throws Exception {

    // given
    entity.setBrand(brand);

    // when
    this.getListener().onAfterSave(new AfterSaveEvent<MyStableOnboarding>(entity, null, "11"));

    then(context).should().upload(brand, path, filename, getModelClass());
  }

  @After
  public void shouldHaveNoMoreInteractions() {
    then(context).shouldHaveNoMoreInteractions();
  }
}
