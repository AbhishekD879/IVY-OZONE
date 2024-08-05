package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static java.util.Comparator.comparingInt;
import static java.util.stream.Collectors.collectingAndThen;
import static java.util.stream.Collectors.toCollection;

import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipMappingPublicDto;
import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipModuleDto;
import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipSportCategorySvgDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import com.ladbrokescoral.oxygen.cms.api.mapping.LuckyDipMapper;
import com.ladbrokescoral.oxygen.cms.api.mapping.LuckyDipSportCategorySvgMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository;
import com.ladbrokescoral.oxygen.cms.api.service.LuckyDipMappingPublicService;
import com.ladbrokescoral.oxygen.cms.api.service.SportModuleService;
import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class LuckyDipModuleService {

  private final SportModuleService sportModuleService;
  private final SportCategoryRepository sportCategoryRepository;
  private final LuckyDipMappingPublicService luckyDipMappingPublicService;

  public LuckyDipModuleService(
      SportModuleService sportModuleService,
      SportCategoryRepository sportCategoryRepository,
      LuckyDipMappingPublicService luckyDipMappingPublicService) {
    this.sportModuleService = sportModuleService;
    this.sportCategoryRepository = sportCategoryRepository;
    this.luckyDipMappingPublicService = luckyDipMappingPublicService;
  }

  public List<LuckyDipModuleDto> getLuckyDipModuleData(String brand) {
    Map<String, LuckyDipSportCategorySvgDto> categorySvgMap =
        sportCategoryRepository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE)
            .stream()
            .map(LuckyDipSportCategorySvgMapper.INSTANCE::sportToSvg)
            .filter(
                luckyDipSportCategorySvgDto ->
                    Objects.nonNull(luckyDipSportCategorySvgDto.getSvgId())
                        && Objects.nonNull(luckyDipSportCategorySvgDto.getCategoryId()))
            .collect(
                collectingAndThen(
                    toCollection(
                        () ->
                            new TreeSet<>(
                                comparingInt(LuckyDipSportCategorySvgDto::getCategoryId))),
                    ArrayList::new))
            .stream()
            .collect(
                Collectors.toMap(LuckyDipSportCategorySvgDto::getImageTitle, Function.identity()));

    List<LuckyDipMappingPublicDto> luckyDipMappingPublicDtos =
        luckyDipMappingPublicService.findAllActiveLuckyDipMappingsByBrand(brand).stream()
            .map(
                (LuckyDipMappingPublicDto luckyDipMappingPublicDto) -> {
                  LuckyDipSportCategorySvgDto luckyDipSportCategory =
                      categorySvgMap.get(luckyDipMappingPublicDto.getCategoryId());
                  if (Objects.nonNull(luckyDipSportCategory)) {
                    luckyDipMappingPublicDto.setSvgId(luckyDipSportCategory.getSvgId());
                    luckyDipMappingPublicDto.setCategory(luckyDipSportCategory.getCategoryId());
                  }
                  return luckyDipMappingPublicDto;
                })
            .collect(Collectors.toList());

    return sportModuleService.findAll(brand, SportModuleType.LUCKY_DIP).stream()
        .map(LuckyDipMapper.getInstance()::toDto)
        .map(
            (LuckyDipModuleDto luckyDipModuleDto) -> {
              luckyDipModuleDto.setLuckyDipMappings(luckyDipMappingPublicDtos);
              return luckyDipModuleDto;
            })
        .collect(Collectors.toList());
  }
}
