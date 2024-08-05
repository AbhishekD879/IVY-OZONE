package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.BybWidgetDataDto;
import com.ladbrokescoral.oxygen.cms.api.dto.BybWidgetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BybWidget;
import com.ladbrokescoral.oxygen.cms.api.mapping.BybWidgetMapper;
import com.ladbrokescoral.oxygen.cms.api.service.BybWidgetDataService;
import com.ladbrokescoral.oxygen.cms.api.service.BybWidgetService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BybWidgetPublicService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(value = {BybWidgetApi.class, BybWidgetPublicService.class, BybWidgetMapper.class})
@AutoConfigureMockMvc(addFilters = false)
@Import(ModelMapperConfig.class)
public class BybWidgetApiTest extends AbstractControllerTest {

  @MockBean BybWidgetDataService bybWidgetDataService;
  @MockBean BybWidgetService bybWidgetService;

  ModelMapper mapper = new ModelMapper();

  @Test
  public void testReadActiveRecordsByBrand() throws Exception {
    BybWidget entity = mapper.map(createDto(), BybWidget.class);

    when(bybWidgetService.readByBrand(Mockito.anyString())).thenReturn(Optional.of(entity));
    List<BybWidgetDataDto> listData = new ArrayList<>();
    listData.add(createData());
    when(bybWidgetDataService.getActiveRecordsByBrand(Mockito.anyString()))
        .thenReturn(Optional.of(listData));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/byb-widgets")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private BybWidgetDto createDto() {
    BybWidgetDto dto = new BybWidgetDto();
    dto.setTitle("BYB_WIDGET");
    dto.setShowAll(true);
    dto.setMarketCardVisibleSelections(10);
    dto.setBrand("bma");
    return dto;
  }

  private BybWidgetDataDto createData() {

    BybWidgetDataDto dto = new BybWidgetDataDto();
    dto.setTitle("data");
    dto.setDisplayFrom(Instant.now());
    dto.setDisplayTo(Instant.now());
    dto.setEventId("123");
    dto.setMarketId("123");
    dto.setBrand("bma");
    dto.setLocations(createLocations());

    return dto;
  }

  private List<String> createLocations() {
    List<String> locs = new ArrayList<>();
    locs.add("home");
    locs.add("football");
    return locs;
  }
}
