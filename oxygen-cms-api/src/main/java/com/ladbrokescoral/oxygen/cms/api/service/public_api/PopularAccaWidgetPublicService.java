package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.PopularAccaModuleData;
import com.ladbrokescoral.oxygen.cms.api.dto.PopularAccaModuleDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PopularAccaWidgetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PopularAccaWidget;
import com.ladbrokescoral.oxygen.cms.api.mapping.PopularAccaWidgetMapper;
import com.ladbrokescoral.oxygen.cms.api.service.PopularAccaWidgetDataService;
import com.ladbrokescoral.oxygen.cms.api.service.PopularAccaWidgetService;
import java.util.*;
import java.util.stream.Collectors;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

@Service
public class PopularAccaWidgetPublicService {
  private PopularAccaWidgetDataService popularAccaWidgetDataService;
  private PopularAccaWidgetService popularAccaWidgetService;
  private ModelMapper modelMapper;
  private final PopularAccaWidgetMapper popularAccaWidgetMapper;

  private static final String HOME_PAGE = "Sportbook Homepage";
  private static final String FOOTBALL_PAGE = "Football Homepage";

  private static final Integer FOOTBALL = 16;
  static Map<String, Integer> pageMap = new HashMap<>();

  public PopularAccaWidgetPublicService(
      PopularAccaWidgetDataService popularAccaWidgetDataService,
      PopularAccaWidgetService popularAccaWidgetService,
      ModelMapper modelMapper,
      PopularAccaWidgetMapper popularAccaWidgetMapper) {
    this.popularAccaWidgetDataService = popularAccaWidgetDataService;
    this.popularAccaWidgetService = popularAccaWidgetService;
    this.modelMapper = modelMapper;
    this.popularAccaWidgetMapper = popularAccaWidgetMapper;
  }

  static {
    pageMap.put(HOME_PAGE, 0);
    pageMap.put(FOOTBALL_PAGE, FOOTBALL);
  }

  public Optional<PopularAccaWidgetDto> readByBrand(String brand) {

    return popularAccaWidgetService
        .readByBrand(brand)
        .map(
            (PopularAccaWidget entity) -> {
              PopularAccaWidgetDto dto = modelMapper.map(entity, PopularAccaWidgetDto.class);
              popularAccaWidgetDataService.getActiveRecordsByBrand(brand).ifPresent(dto::setData);
              return dto;
            });
  }

  public List<PopularAccaModuleDto> getPopularAccaModuleDtosByBrand(String brand) {

    return readByBrand(brand).map(this::preparePopularAccaModule).orElseGet(ArrayList::new);
  }

  private List<PopularAccaModuleDto> preparePopularAccaModule(PopularAccaWidgetDto dto) {
    Map<Integer, List<PopularAccaModuleData>> moduledata = new HashMap<>();
    dto.getData()
        .forEach(
            data ->
                data.getLocations().stream()
                    .filter(loc -> pageMap.containsKey(loc))
                    .map(pageMap::get)
                    .forEach(
                        (Integer loc) -> {
                          PopularAccaModuleData widgetData =
                              popularAccaWidgetMapper.toDtoData(data);
                          moduledata.computeIfAbsent(loc, v -> new ArrayList<>());
                          moduledata.computeIfPresent(
                              loc,
                              (Integer key, List<PopularAccaModuleData> val) -> {
                                widgetData.setSortOrder(val.size());
                                val.add(widgetData);
                                return val;
                              });
                        }));

    return moduledata.entrySet().stream()
        .map(k -> updateWidgetData(dto, k))
        .collect(Collectors.toList());
  }

  private PopularAccaModuleDto updateWidgetData(
      PopularAccaWidgetDto dto, Map.Entry<Integer, List<PopularAccaModuleData>> k) {
    PopularAccaModuleDto moduleDto = popularAccaWidgetMapper.toDto(dto);
    moduleDto.setData(k.getValue());
    moduleDto.setSportId(k.getKey());
    return moduleDto;
  }
}
