package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.BybWidgetDto;
import com.ladbrokescoral.oxygen.cms.api.dto.BybWidgetModuleData;
import com.ladbrokescoral.oxygen.cms.api.dto.BybWidgetModuleDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BybWidget;
import com.ladbrokescoral.oxygen.cms.api.mapping.BybWidgetMapper;
import com.ladbrokescoral.oxygen.cms.api.service.BybWidgetDataService;
import com.ladbrokescoral.oxygen.cms.api.service.BybWidgetService;
import java.util.*;
import java.util.stream.Collectors;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

@Service
public class BybWidgetPublicService {
  private BybWidgetDataService bybWidgetDataService;
  private BybWidgetService bybWidgetService;
  private ModelMapper modelMapper;
  private final BybWidgetMapper bybWidgetMapper;

  private static final String HOME_PAGE = "Sportbook Homepage";
  private static final String FOOTBALL_PAGE = "Football Homepage";

  private static final Integer FOOTBALL = 16;
  static Map<String, Integer> pageMap = new HashMap<>();

  public BybWidgetPublicService(
      BybWidgetDataService bybWidgetDataService,
      BybWidgetService bybWidgetService,
      ModelMapper modelMapper,
      BybWidgetMapper bybWidgetMapper) {
    this.bybWidgetDataService = bybWidgetDataService;
    this.bybWidgetService = bybWidgetService;
    this.modelMapper = modelMapper;
    this.bybWidgetMapper = bybWidgetMapper;
  }

  static {
    pageMap.put(HOME_PAGE, 0);
    pageMap.put(FOOTBALL_PAGE, FOOTBALL);
  }

  public Optional<BybWidgetDto> readByBrand(String brand) {

    return bybWidgetService
        .readByBrand(brand)
        .map(
            (BybWidget entity) -> {
              BybWidgetDto dto = modelMapper.map(entity, BybWidgetDto.class);
              bybWidgetDataService.getActiveRecordsByBrand(brand).ifPresent(dto::setData);
              return dto;
            });
  }

  public List<BybWidgetModuleDto> getBybWidgetModuleDtosByBrand(String brand) {

    return readByBrand(brand).map(this::prepareBybWidgetModule).orElseGet(ArrayList::new);
  }

  private List<BybWidgetModuleDto> prepareBybWidgetModule(BybWidgetDto dto) {
    Map<Integer, List<BybWidgetModuleData>> moduledata = new HashMap<>();
    dto.getData()
        .forEach(
            data ->
                data.getLocations().stream()
                    .filter(loc -> pageMap.containsKey(loc))
                    .map(pageMap::get)
                    .forEach(
                        (Integer loc) -> {
                          BybWidgetModuleData widgetData = bybWidgetMapper.toDtoData(data);
                          moduledata.computeIfAbsent(loc, v -> new ArrayList<>());
                          moduledata.computeIfPresent(
                              loc,
                              (Integer key, List<BybWidgetModuleData> val) -> {
                                widgetData.setSortOrder(val.size());
                                val.add(widgetData);
                                return val;
                              });
                        }));

    return moduledata.entrySet().stream()
        .map(k -> updatePageId(dto, k))
        .collect(Collectors.toList());
  }

  private BybWidgetModuleDto updatePageId(
      BybWidgetDto dto, Map.Entry<Integer, List<BybWidgetModuleData>> k) {
    BybWidgetModuleDto moduleDto = bybWidgetMapper.toDto(dto);
    moduleDto.setData(k.getValue());
    moduleDto.setSportId(k.getKey());
    return moduleDto;
  }
}
