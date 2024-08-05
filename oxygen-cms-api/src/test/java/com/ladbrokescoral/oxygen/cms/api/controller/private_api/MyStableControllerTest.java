package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.MyStableDto;
import com.ladbrokescoral.oxygen.cms.api.entity.MyStable;
import com.ladbrokescoral.oxygen.cms.api.repository.MyStableRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.MyStableService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.time.Instant;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(
    value = {
      MyStableController.class,
      MyStableService.class,
      ModelMapper.class,
      MyStable.class,
      MyStableRepository.class
    })
@Import(ModelMapperConfig.class)
@MockBean(BrandService.class)
@AutoConfigureMockMvc(addFilters = false)
public class MyStableControllerTest extends AbstractControllerTest {

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
    when(repository.findById(any())).thenReturn(Optional.of(entity));
  }

  @Test
  public void createTest() throws Exception {

    when(myStableService.save(any(MyStable.class))).thenReturn(entity);
    given(myStableService.prepareModelBeforeSave(any())).willReturn(entity);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/my-stable/configuration")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(myStableDto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void getByBrandElse() throws Exception {

    Mockito.when(repository.getByBrand("bma")).thenReturn(null);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/my-stable/configuration/brand/bma")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getMyStable())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void getByBrand() throws Exception {

    when(repository.getByBrand("bma")).thenReturn(getMyStable());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/my-stable/configuration/brand/bma")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getMyStable())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void getById() throws Exception {

    when(repository.findById("123")).thenReturn(Optional.of(getMyStable()));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/my-stable/configuration/123")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void getByIdWithoutException() throws Exception {
    entity = getMyStable();
    given(myStableService.findByIds("1")).willReturn(Optional.of(entity));
    when(repository.findById("1")).thenReturn(Optional.of(entity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/my-stable/configuration/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void getByIdNotFound() throws Exception {

    when(repository.findById("123")).thenReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/my-stable/configuration/123")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testUpdateIdNotFound() throws Exception {
    String id = "111";
    when(repository.findById(id)).thenReturn(Optional.ofNullable(null));
    myStableDto.setId(id);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/my-stable/configuration/" + id)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(myStableDto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUpdate() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/my-stable/configuration/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(myStableDto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void deleteById() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/my-stable/configuration/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(myStableDto)))
        .andExpect(status().is2xxSuccessful());
  }

  private static MyStableDto getMyStableDto() {
    MyStableDto myStableDto = new MyStableDto();
    myStableDto.setActive(true);
    myStableDto.setId("1");
    myStableDto.setEntryPointLabel("tile");
    myStableDto.setSaveIcon("Notes");
    myStableDto.setBrand("bma");
    myStableDto.setEntryPointIcon("entry point icon");
    myStableDto.setCreatedAt(Instant.now());
    myStableDto.setUpdatedAt(Instant.now());
    myStableDto.setCreatedBy("System");
    myStableDto.setHorsesRunningToday(true);
    myStableDto.setUnbookmarkIcon("unbookmarked");
    myStableDto.setBookmarkIcon("bookmark");
    myStableDto.setNoHorsesCtaButton("noHorsesCtaButton");
    myStableDto.setEmptyStableLabel2("noHorsesSvg");
    myStableDto.setEmptyStableLabel1("NoHorses");
    myStableDto.setNoHorsesCtaButton("new notes");
    myStableDto.setTodayRunningHorsesText("No Horses Today");
    myStableDto.setTodayRunningHorsesSvg("No Horses svg");

    return myStableDto;
  }

  @Test
  public void testOnboarding() {
    MyStable myStable = new MyStable();
    myStable.setBrand("coral");
    assertEquals(myStable, myStable.content());
  }

  private static MyStable getMyStable() {
    MyStable myStable = new MyStable();
    myStable.setActive(true);
    myStable.setBrand("bma");
    myStable.setId("1");
    myStable.setEntryPointIcon("EntryIcon");
    myStable.setSignpostingIcon("signposting");
    myStable.setBookmarkIcon("bookmarkIcon");
    myStable.setUnbookmarkIcon("unbookmarkIcon");
    myStable.setNoHorsesCtaButton("noHorsesButton");
    myStable.setNoHorsesIcon("noHorses.svg");
    myStable.setEmptyStableLabel2("Please click here to add");
    myStable.setEditNoteIcon("new Notes");
    myStable.setCreatedByUserName("ozoneqa@coral.co.uk");
    myStable.setUpdatedByUserName("ozoneqa@coral.co.uk");
    myStable.setTodayRunningHorsesText("NoHorsesToday");
    myStable.setTodayRunningHorsesSvg("first.svg");
    return myStable;
  }
}
