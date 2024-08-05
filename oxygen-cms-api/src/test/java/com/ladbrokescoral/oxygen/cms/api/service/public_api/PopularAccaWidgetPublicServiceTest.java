package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.cms.api.dto.PopularAccaModuleData;
import com.ladbrokescoral.oxygen.cms.api.dto.PopularAccaModuleDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PopularAccaWidgetDataDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PopularAccaWidgetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PopularAccaWidget;
import com.ladbrokescoral.oxygen.cms.api.entity.PopularAccaWidgetData;
import com.ladbrokescoral.oxygen.cms.api.mapping.PopularAccaWidgetMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.PopularAccaWidgetDataRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.PopularAccaWidgetRepository;
import com.ladbrokescoral.oxygen.cms.api.service.PopularAccaWidgetDataService;
import com.ladbrokescoral.oxygen.cms.api.service.PopularAccaWidgetService;
import com.ladbrokescoral.oxygen.cms.api.service.SortableService;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.data.domain.Sort;

@RunWith(MockitoJUnitRunner.class)
@WebMvcTest(value = {PopularAccaWidgetPublicService.class})
public class PopularAccaWidgetPublicServiceTest {

  private static final String BRAND = "bma";
  private static final Sort SORT_BY_SORT_ORDER_ASC = SortableService.SORT_BY_SORT_ORDER_ASC;

  private static final String TITLE = "title";
  private static final int SPORT_ID = 0;
  private static final int SORT_ORDER = 1;

  private PopularAccaWidgetDataService popularAccaWidgetDataService;

  @Mock private PopularAccaWidgetService popularAccaWidgetService;

  @Mock private ModelMapper modelMapper;

  @Mock private PopularAccaWidgetMapper popularAccaWidgetMapper;

  private PopularAccaWidgetPublicService popularAccaWidgetPublicService;

  @Mock private PopularAccaWidgetDataRepository popularAccaWidgetDataRepository;

  @Mock private PopularAccaWidgetRepository popularAccaWidgetRepository;

  @Before
  public void setUp() {
    popularAccaWidgetDataService =
        new PopularAccaWidgetDataService(popularAccaWidgetDataRepository, modelMapper);
    popularAccaWidgetPublicService =
        new PopularAccaWidgetPublicService(
            popularAccaWidgetDataService,
            popularAccaWidgetService,
            modelMapper,
            popularAccaWidgetMapper);
  }

  @Test
  public void testGetPopularAccaModuleDtosByBrand() {
    PopularAccaWidget entity = createPopularAccaWidget();
    ModelMapper mapper = new ModelMapper();
    PopularAccaWidgetDto dto = mapper.map(entity, PopularAccaWidgetDto.class);

    when(modelMapper.map(any(PopularAccaWidget.class), eq(PopularAccaWidgetDto.class)))
        .thenReturn(dto);

    PopularAccaWidgetData data = createPopularAccaWidgetData();
    PopularAccaWidgetDataDto dtaDto = mapper.map(data, PopularAccaWidgetDataDto.class);
    when(modelMapper.map(any(PopularAccaWidgetData.class), eq(PopularAccaWidgetDataDto.class)))
        .thenReturn(dtaDto);

    when(popularAccaWidgetService.readByBrand(BRAND)).thenReturn(Optional.of(entity));

    when(popularAccaWidgetDataRepository.findActiveRecordsByBrandOrderBySortOrderAsc(
            eq(BRAND), any(Instant.class), eq(SORT_BY_SORT_ORDER_ASC)))
        .thenReturn(Collections.singletonList(createPopularAccaWidgetData()));

    when(popularAccaWidgetMapper.toDtoData(any(PopularAccaWidgetDataDto.class)))
        .thenReturn(createPopularAccaWidgetModuleData());

    when(popularAccaWidgetMapper.toDto(any(PopularAccaWidgetDto.class)))
        .thenReturn(createPopularAccaWidgetModuleDto());

    List<PopularAccaModuleDto> result =
        popularAccaWidgetPublicService.getPopularAccaModuleDtosByBrand(BRAND);

    assertNotNull(result);
    assertFalse(result.isEmpty());
    assertEquals(1, result.size());
  }

  private PopularAccaWidget createPopularAccaWidget() {
    PopularAccaWidget widget = new PopularAccaWidget();
    widget.setId("124");
    widget.setBrand(BRAND);
    widget.setTitle(TITLE);
    return widget;
  }

  private PopularAccaWidgetData createPopularAccaWidgetData() {

    PopularAccaWidgetData dto = new PopularAccaWidgetData();
    dto.setTitle(TITLE);
    dto.setDisplayFrom(Instant.now());
    dto.setDisplayTo(Instant.now().plusSeconds(3600));
    dto.setBrand(BRAND);
    dto.setLocations(createLocations());

    return dto;
  }

  private List<String> createLocations() {
    List<String> locations = new ArrayList<>();
    locations.add("Sportbook Homepage");
    locations.add("football");
    return locations;
  }

  public static PopularAccaModuleData createPopularAccaWidgetModuleData() {
    PopularAccaModuleData moduleData = new PopularAccaModuleData();

    moduleData.setTitle(TITLE);
    moduleData.setSortOrder(SORT_ORDER);

    return moduleData;
  }

  private PopularAccaModuleDto createPopularAccaWidgetModuleDto() {

    PopularAccaModuleData data = new PopularAccaModuleData();
    data.setTitle(TITLE);
    data.setSortOrder(SORT_ORDER);

    PopularAccaModuleDto moduleDto = new PopularAccaModuleDto();
    moduleDto.setSportId(SPORT_ID);
    moduleDto.setTitle(TITLE);
    moduleDto.setData(Collections.singletonList(data));

    return moduleDto;
  }
}
