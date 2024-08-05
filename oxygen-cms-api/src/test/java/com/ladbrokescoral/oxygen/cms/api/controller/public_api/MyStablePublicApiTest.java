package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.MyStableDto;
import com.ladbrokescoral.oxygen.cms.api.entity.MyStable;
import com.ladbrokescoral.oxygen.cms.api.repository.MyStableRepository;
import com.ladbrokescoral.oxygen.cms.api.service.MyStableService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(value = {MyStablePublicApi.class, MyStableService.class, ModelMapper.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
public class MyStablePublicApiTest extends AbstractControllerTest {
  MyStableDto myStableDto;
  @Mock MyStableService myStableService;
  ModelMapper mapper = new ModelMapper();
  MyStable entity;
  @MockBean MyStableRepository repository;

  @Before
  public void init() {

    myStableDto = getMyStableDto();
    entity = mapper.map(myStableDto, MyStable.class);

    entity.setId("1");
    entity.setCreatedBy("system");
    entity.setUpdatedAt(Instant.now());
    when(repository.save(any())).thenReturn(entity);
  }

  @Test
  public void testFindByBrand() throws Exception {

    given(repository.findByBrand("bma")).willReturn(Arrays.asList(entity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/my-stable/configuration")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testFindByBrandNotFound() throws Exception {
    List<MyStable> myStables = new ArrayList<>();
    given(repository.findByBrand("bma")).willReturn(myStables);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/my-stable/configuration")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(myStableDto)))
        .andExpect(status().isNotFound());
  }

  private static MyStableDto getMyStableDto() {
    MyStableDto myStableDto = new MyStableDto();
    myStableDto.setActive(true);
    myStableDto.setId("1");
    myStableDto.setEntryPointLabel("tile");
    myStableDto.setEditNoteIcon("Notes");
    myStableDto.setBrand("bma");
    myStableDto.setEntryPointIcon("entry point icon");
    myStableDto.setCreatedAt(Instant.now());
    myStableDto.setUpdatedAt(Instant.now());
    myStableDto.setCreatedBy("System");
    myStableDto.setTodayRunningHorsesText("No Horses Text");
    myStableDto.setTodayRunningHorsesSvg("horses.svg");

    return myStableDto;
  }
}
