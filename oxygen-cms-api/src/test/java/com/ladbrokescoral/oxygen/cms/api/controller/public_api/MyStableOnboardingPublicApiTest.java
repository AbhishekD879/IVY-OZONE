package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding.MyStableOnboardingDto;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.MyStableOnboarding;
import com.ladbrokescoral.oxygen.cms.api.repository.MyStableOnboardingRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.MyStableOnboardingService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.time.Instant;
import java.util.Arrays;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(value = {MyStableOnboardingPublicApi.class, MyStableOnboardingService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
public class MyStableOnboardingPublicApiTest extends AbstractControllerTest {
  @MockBean MyStableOnboardingRepository repository;
  @MockBean ImageService imageService;
  MyStableOnboarding entity;
  MyStableOnboardingDto dto;
  ModelMapper mapper = new ModelMapper();

  @Before
  public void init() {
    dto = createDto();
    entity = mapper.map(dto, MyStableOnboarding.class);
    entity.setId("12121212121");
    entity.setCreatedBy("system");
    entity.setUpdatedAt(Instant.now());
  }

  private MyStableOnboardingDto createDto() {
    MyStableOnboardingDto eachWayOnboarding = new MyStableOnboardingDto();
    eachWayOnboarding.setButtonText("Click here");
    eachWayOnboarding.setImageUrl("image1");
    eachWayOnboarding.setIsEnable(true);
    eachWayOnboarding.setBrand("bma");
    return eachWayOnboarding;
  }

  @Test
  public void testFindByBrand() throws Exception {
    given(repository.findByBrand("bma")).willReturn(Arrays.asList(entity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/my-stable/onboarding")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testFindByBrandNotFound() throws Exception {
    given(repository.findByBrand("bma")).willReturn(null);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/my-stable/onboarding")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().isNotFound());
  }
}
