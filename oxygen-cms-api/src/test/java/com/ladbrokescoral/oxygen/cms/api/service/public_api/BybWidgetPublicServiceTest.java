package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.cms.api.dto.BybWidgetDataDto;
import com.ladbrokescoral.oxygen.cms.api.dto.BybWidgetDto;
import com.ladbrokescoral.oxygen.cms.api.dto.BybWidgetModuleData;
import com.ladbrokescoral.oxygen.cms.api.dto.BybWidgetModuleDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BybWidget;
import com.ladbrokescoral.oxygen.cms.api.entity.BybWidgetData;
import com.ladbrokescoral.oxygen.cms.api.mapping.BybWidgetMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.BybWidgetDataRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.BybWidgetRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BybWidgetDataService;
import com.ladbrokescoral.oxygen.cms.api.service.BybWidgetService;
import java.time.Instant;
import java.util.*;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.data.domain.Sort;

@RunWith(MockitoJUnitRunner.class)
@WebMvcTest(value = {BybWidgetPublicService.class})
public class BybWidgetPublicServiceTest {

  private static final String BRAND = "bma";
  private static final Sort SORT_BY_SORT_ORDER_ASC = BybWidgetDataService.SORT_BY_SORT_ORDER_ASC;

  private static final String TITLE = "title";
  private static final String EVENT_ID = "123";
  private static final String MARKET_ID = "1234567";
  private static final int MARKET_CARD_VISIBLE_SELECTIONS = 2;
  private static final boolean SHOW_ALL = true;
  private static final int SPORT_ID = 0;
  private static final int SORT_ORDER = 1;

  private BybWidgetDataService bybWidgetDataService;

  @Mock private BybWidgetService bybWidgetService;

  @Mock private ModelMapper modelMapper;

  @Mock private BybWidgetMapper bybWidgetMapper;

  private BybWidgetPublicService bybWidgetPublicService;

  @Mock private BybWidgetDataRepository bybWidgetDataRepository;

  @Mock private BybWidgetRepository bybWidgetRepository;

  @Before
  public void setUp() throws Exception {
    bybWidgetDataService = new BybWidgetDataService(bybWidgetDataRepository, modelMapper);
    bybWidgetPublicService =
        new BybWidgetPublicService(
            bybWidgetDataService, bybWidgetService, modelMapper, bybWidgetMapper);
  }

  @Test
  public void testGetBybWidgetModuleDtosByBrand() {
    BybWidget entity = createBybWidget();
    ModelMapper mapper = new ModelMapper();
    BybWidgetDto dto = mapper.map(entity, BybWidgetDto.class);

    when(modelMapper.map(any(BybWidget.class), eq(BybWidgetDto.class))).thenReturn(dto);

    BybWidgetData data = createBybWidgetData();
    BybWidgetDataDto dtaDto = mapper.map(data, BybWidgetDataDto.class);
    when(modelMapper.map(any(BybWidgetData.class), eq(BybWidgetDataDto.class))).thenReturn(dtaDto);

    when(bybWidgetService.readByBrand(BRAND)).thenReturn(Optional.of(entity));

    when(bybWidgetDataRepository.findActiveRecordsByBrandOrderBySortOrderAsc(
            eq(BRAND), any(Instant.class), eq(SORT_BY_SORT_ORDER_ASC)))
        .thenReturn(Collections.singletonList(createBybWidgetData()));

    when(bybWidgetMapper.toDtoData(any(BybWidgetDataDto.class)))
        .thenReturn(createBybWidgetModuleData());

    when(bybWidgetMapper.toDto(any(BybWidgetDto.class))).thenReturn(createBybWidgetModuleDto());

    List<BybWidgetModuleDto> result = bybWidgetPublicService.getBybWidgetModuleDtosByBrand(BRAND);

    assertNotNull(result);
    assertFalse(result.isEmpty());
    assertEquals(1, result.size());
  }

  private BybWidget createBybWidget() {
    BybWidget widget = new BybWidget();
    widget.setId("124");
    widget.setBrand(BRAND);
    widget.setTitle(TITLE);
    widget.setMarketCardVisibleSelections(MARKET_CARD_VISIBLE_SELECTIONS);
    widget.setShowAll(SHOW_ALL);
    return widget;
  }

  private BybWidgetData createBybWidgetData() {

    BybWidgetData dto = new BybWidgetData();
    dto.setTitle(TITLE);
    dto.setDisplayFrom(Instant.now());
    dto.setDisplayTo(Instant.now().plusSeconds(3600));
    dto.setEventId(EVENT_ID);
    dto.setMarketId(MARKET_ID);
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

  public static BybWidgetModuleData createBybWidgetModuleData() {
    BybWidgetModuleData moduleData = new BybWidgetModuleData();

    moduleData.setTitle(TITLE);
    moduleData.setMarketId(MARKET_ID);
    moduleData.setEventId(EVENT_ID);
    moduleData.setSortOrder(SORT_ORDER);

    return moduleData;
  }

  private BybWidgetModuleDto createBybWidgetModuleDto() {

    BybWidgetModuleData data = new BybWidgetModuleData();
    data.setTitle(TITLE);
    data.setEventId(EVENT_ID);
    data.setMarketId(MARKET_ID);
    data.setSortOrder(SORT_ORDER);

    BybWidgetModuleDto moduleDto = new BybWidgetModuleDto();
    moduleDto.setSportId(SPORT_ID);
    moduleDto.setTitle(TITLE);
    moduleDto.setData(Collections.singletonList(data));
    moduleDto.setMarketCardVisibleSelections(MARKET_CARD_VISIBLE_SELECTIONS);
    moduleDto.setShowAll(SHOW_ALL);

    return moduleDto;
  }
}
