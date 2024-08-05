package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.BybWidgetDataDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BybWidgetData;
import com.ladbrokescoral.oxygen.cms.api.exception.ElementAlreadyExistException;
import com.ladbrokescoral.oxygen.cms.api.repository.BybWidgetDataRepository;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.modelmapper.ModelMapper;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Service
public class BybWidgetDataService extends SortableService<BybWidgetData> {

  private final ModelMapper mapper;
  private final BybWidgetDataRepository bybWidgetDataRepository;

  public static final String SORT_ORDER_FIELD = "sortOrder";
  public static final Sort SORT_BY_SORT_ORDER_ASC = Sort.by(SORT_ORDER_FIELD);

  public BybWidgetDataService(BybWidgetDataRepository bybWidgetDataRepository, ModelMapper mapper) {
    super(bybWidgetDataRepository);
    this.mapper = mapper;
    this.bybWidgetDataRepository = bybWidgetDataRepository;
  }

  @Override
  public BybWidgetData save(BybWidgetData bybWidgetData) {

    return bybWidgetDataRepository
        .findByMarketId(bybWidgetData.getMarketId())
        .map(
            (BybWidgetData entity) -> {
              if (entity.getId().equals(bybWidgetData.getId())) return super.save(bybWidgetData);
              else throw new ElementAlreadyExistException();
            })
        .orElse(super.save(bybWidgetData));
  }

  public Optional<List<BybWidgetDataDto>> readByBrand(String brand) {

    return convertToDto(bybWidgetDataRepository.findByBrand(brand));
  }

  public Optional<List<BybWidgetDataDto>> getRecordsByBrandAndStatus(String brand, boolean status) {
    return status ? getActiveAndFutureRecordsByBrand(brand) : getExpiredRecordsByBrand(brand);
  }

  public Optional<List<BybWidgetDataDto>> getActiveRecordsByBrand(String brand) {
    return convertToDto(
        bybWidgetDataRepository.findActiveRecordsByBrandOrderBySortOrderAsc(
            brand, Instant.now(), SORT_BY_SORT_ORDER_ASC));
  }

  private Optional<List<BybWidgetDataDto>> getActiveAndFutureRecordsByBrand(String brand) {
    return convertToDto(
        bybWidgetDataRepository.findActiveAndFutureRecordsByBrandOrderBySortOrderAsc(
            brand, Instant.now(), SORT_BY_SORT_ORDER_ASC));
  }

  private Optional<List<BybWidgetDataDto>> getExpiredRecordsByBrand(String brand) {

    return convertToDto(
        bybWidgetDataRepository.findExpiredRecordsByBrandOrderBySortOrderAsc(
            brand, Instant.now(), SORT_BY_SORT_ORDER_ASC));
  }

  private Optional<List<BybWidgetDataDto>> convertToDto(List<BybWidgetData> data) {
    List<BybWidgetDataDto> bybWidgetDataDtos = new ArrayList<>();

    if (CollectionUtils.isEmpty(data)) return Optional.empty();

    data.forEach(entity -> bybWidgetDataDtos.add(mapper.map(entity, BybWidgetDataDto.class)));
    return Optional.ofNullable(bybWidgetDataDtos);
  }

  @Override
  protected boolean isNewElementCreatedFirstInTheList() {
    return false;
  }
}
