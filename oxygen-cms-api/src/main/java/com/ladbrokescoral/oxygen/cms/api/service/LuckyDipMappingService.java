package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipMappingDto;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipMapping;
import com.ladbrokescoral.oxygen.cms.api.exception.BadRequestException;
import com.ladbrokescoral.oxygen.cms.api.repository.LuckyDipMappingRepository;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class LuckyDipMappingService extends SortableService<LuckyDipMapping> {

  @Value("${luckyDip.enableTypeIdsValidation}")
  private boolean enableTypeIdsValidation;

  private static final int TYPE_ID_MAX_COUNT = 100;

  private final LuckyDipMappingRepository luckyDipMappingRepository;
  private final ModelMapper modelMapper;

  @Autowired
  public LuckyDipMappingService(
      final LuckyDipMappingRepository repository, ModelMapper modelMapper) {
    super(repository);
    this.luckyDipMappingRepository = repository;
    this.modelMapper = modelMapper;
  }

  @Override
  public boolean isNewElementCreatedFirstInTheList() {
    return false;
  }

  public LuckyDipMapping convertDtoToEntity(LuckyDipMappingDto luckyDipMappingDto) {
    return modelMapper.map(luckyDipMappingDto, LuckyDipMapping.class);
  }

  public void validateCategoryAndTypeIds(LuckyDipMapping luckyDipMapping) {
    validateTypeIdCount(luckyDipMapping);
    if (Boolean.TRUE.equals(luckyDipMapping.getActive())) {
      List<LuckyDipMapping> allByBrandAndActiveTrue = getAllByBrandAndActiveTrue(luckyDipMapping);

      validateCategoryIds(luckyDipMapping, allByBrandAndActiveTrue);
      validateTypeIds(luckyDipMapping, allByBrandAndActiveTrue);
    }
  }

  public void validateCategoryIds(
      LuckyDipMapping luckyDipMapping, List<LuckyDipMapping> allByBrandAndActiveTrue) {
    Set<String> existingCategoryIds = getExistingCategoryIds(allByBrandAndActiveTrue);
    if (existingCategoryIds.contains(luckyDipMapping.getCategoryId())) {
      log.error("categoryId duplicated: {}", luckyDipMapping.getCategoryId());
      throw new BadRequestException("categoryId duplicated");
    }
  }

  public void validateTypeIds(
      LuckyDipMapping luckyDipMapping, List<LuckyDipMapping> allByBrandAndActiveTrue) {
    if (enableTypeIdsValidation) {
      validateWithinCurrentTypeIds(luckyDipMapping);
      validateWithExistingTypeIds(luckyDipMapping, allByBrandAndActiveTrue);
    }
  }

  private void validateTypeIdCount(LuckyDipMapping luckyDipMapping) {
    if (Arrays.stream(luckyDipMapping.getTypeIds().split(",")).count() > TYPE_ID_MAX_COUNT) {
      throw new BadRequestException("Maximum Type ID Limit Reached");
    }
  }

  public void validateWithinCurrentTypeIds(LuckyDipMapping luckyDipMapping) {
    Set<String> set = new HashSet<>();
    Stream.of(luckyDipMapping.getTypeIds().split(","))
        .forEach(
            (String typeId) -> {
              if (!set.add(typeId)) {
                log.error("typeId:{} duplicated within the current request", typeId);
                throw new BadRequestException(
                    "typeId:" + typeId + " duplicated within the current request");
              }
            });
  }

  public void validateWithExistingTypeIds(
      LuckyDipMapping luckyDipMapping, List<LuckyDipMapping> allByBrandAndActiveTrue) {
    allByBrandAndActiveTrue.stream()
        .forEach(
            (LuckyDipMapping ldMapping) -> {
              Set<String> existingTypeIds =
                  Arrays.stream(ldMapping.getTypeIds().split(",")).collect(Collectors.toSet());

              Stream.of(luckyDipMapping.getTypeIds().split(","))
                  .forEach(
                      (String typeId) -> {
                        if (existingTypeIds.contains(typeId)) {
                          log.error(
                              "typeId:{} already there for the categoryId:{}",
                              typeId,
                              ldMapping.getCategoryId());
                          throw new BadRequestException(
                              "typeId:"
                                  + typeId
                                  + " already there for the categoryId:"
                                  + ldMapping.getCategoryId());
                        }
                      });
            });
  }

  private List<LuckyDipMapping> getAllByBrandAndActiveTrue(LuckyDipMapping luckyDipMapping) {
    List<LuckyDipMapping> allByBrandAndActiveTrue =
        luckyDipMappingRepository.findByBrandAndActiveTrueOrderBySortOrderAsc(
            luckyDipMapping.getBrand());
    if (luckyDipMapping.getId() != null) {
      allByBrandAndActiveTrue =
          allByBrandAndActiveTrue.stream()
              .filter(ldMapping -> !ldMapping.getId().equals(luckyDipMapping.getId()))
              .collect(Collectors.toList());
    }
    return allByBrandAndActiveTrue;
  }

  private Set<String> getExistingCategoryIds(List<LuckyDipMapping> allByBrandAndActiveTrue) {
    return allByBrandAndActiveTrue.stream()
        .map(LuckyDipMapping::getCategoryId)
        .collect(Collectors.toSet());
  }

  public List<LuckyDipMapping> getAllLuckyDipMappingsByBrand(String brand) {
    return luckyDipMappingRepository.findByBrandAndActiveTrueOrderBySortOrderAsc(brand);
  }
}
