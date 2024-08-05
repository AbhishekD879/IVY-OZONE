package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.PopularAccaWidgetDataDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PopularAccaWidgetData;
import com.ladbrokescoral.oxygen.cms.api.repository.PopularAccaWidgetDataRepository;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Service
public class PopularAccaWidgetDataService extends SortableService<PopularAccaWidgetData> {

  private final ModelMapper mapper;
  private final PopularAccaWidgetDataRepository popularAccaWidgetDataRepository;

  public PopularAccaWidgetDataService(
      PopularAccaWidgetDataRepository popularAccaWidgetDataRepository, ModelMapper mapper) {
    super(popularAccaWidgetDataRepository);
    this.mapper = mapper;
    this.popularAccaWidgetDataRepository = popularAccaWidgetDataRepository;
  }

  public Optional<List<PopularAccaWidgetDataDto>> readByBrand(String brand) {

    return convertToDto(popularAccaWidgetDataRepository.findByBrand(brand));
  }

  public Optional<List<PopularAccaWidgetDataDto>> getRecordsByBrandAndStatus(
      String brand, boolean status) {
    return status ? getActiveAndFutureRecordsByBrand(brand) : getExpiredRecordsByBrand(brand);
  }

  public Optional<List<PopularAccaWidgetDataDto>> getActiveRecordsByBrand(String brand) {
    return convertToDto(
        popularAccaWidgetDataRepository.findActiveRecordsByBrandOrderBySortOrderAsc(
            brand, Instant.now(), SORT_BY_SORT_ORDER_ASC));
  }

  private Optional<List<PopularAccaWidgetDataDto>> getActiveAndFutureRecordsByBrand(String brand) {
    return convertToDto(
        popularAccaWidgetDataRepository.findActiveAndFutureRecordsByBrandOrderBySortOrderAsc(
            brand, Instant.now(), SORT_BY_SORT_ORDER_ASC));
  }

  private Optional<List<PopularAccaWidgetDataDto>> getExpiredRecordsByBrand(String brand) {

    return convertToDto(
        popularAccaWidgetDataRepository.findExpiredRecordsByBrandOrderBySortOrderAsc(
            brand, Instant.now(), SORT_BY_SORT_ORDER_ASC));
  }

  private Optional<List<PopularAccaWidgetDataDto>> convertToDto(List<PopularAccaWidgetData> data) {
    List<PopularAccaWidgetDataDto> popularAccaWidgetDataDtos = new ArrayList<>();

    if (CollectionUtils.isEmpty(data)) return Optional.empty();

    data.forEach(
        entity ->
            popularAccaWidgetDataDtos.add(mapper.map(entity, PopularAccaWidgetDataDto.class)));
    return Optional.ofNullable(popularAccaWidgetDataDtos);
  }

  @Override
  protected boolean isNewElementCreatedFirstInTheList() {
    return false;
  }
}
