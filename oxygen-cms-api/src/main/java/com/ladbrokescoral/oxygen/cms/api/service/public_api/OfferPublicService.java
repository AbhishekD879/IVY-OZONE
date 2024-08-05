package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OfferDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OfferModuleDto;
import com.ladbrokescoral.oxygen.cms.api.entity.OfferModule;
import com.ladbrokescoral.oxygen.cms.api.mapping.OfferMapper;
import com.ladbrokescoral.oxygen.cms.api.service.OfferModuleService;
import com.ladbrokescoral.oxygen.cms.api.service.OfferService;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;
import org.bson.types.ObjectId;
import org.springframework.data.util.Pair;
import org.springframework.stereotype.Service;

@Service
public class OfferPublicService {

  private final OfferService service;
  private final OfferModuleService moduleService;

  public OfferPublicService(OfferService service, OfferModuleService moduleService) {
    this.service = service;
    this.moduleService = moduleService;
  }

  public List<OfferModuleDto> findByBrand(String brand, String deviceType) {

    List<OfferModule> offerModuleList =
        new ArrayList<>(moduleService.findByBrandAndDeviceType(brand, deviceType));

    Map<String, Double> sortCodesForOfferModules =
        offerModuleList.stream()
            .collect(Collectors.toMap(OfferModule::getId, OfferModule::getSortOrder));

    // collect pairs of module id & module name
    List<Pair<String, String>> moduleIdNamePairs =
        offerModuleList.stream()
            .map(value -> Pair.of(value.getId(), value.getName()))
            .collect(Collectors.toList());

    Map<String, List<OfferDto>> offerModulesMap =
        moduleIdNamePairs.stream()
            .map(Pair::getFirst)
            .collect(Collectors.toMap(Function.identity(), value -> new ArrayList<>()));

    // popluate <offer module id, list of offerDto`s> map
    service
        .findOffers(
            brand,
            deviceType,
            moduleIdNamePairs.stream()
                .map(Pair::getFirst)
                .map(ObjectId::new)
                .collect(Collectors.toList()))
        .stream()
        .map(OfferMapper.INSTANCE::toDto)
        .filter(offerDto -> offerModulesMap.containsKey(offerDto.getModule()))
        .forEach(offerDto -> offerModulesMap.get(offerDto.getModule()).add(offerDto));

    // prepare offer modules list omitting empty offer lists
    List<OfferModuleDto> result =
        moduleIdNamePairs.stream()
            .filter(value -> !offerModulesMap.get(value.getFirst()).isEmpty())
            .map(
                value ->
                    new OfferModuleDto(
                        value.getSecond(),
                        offerModulesMap.get(value.getFirst()),
                        sortCodesForOfferModules.get(value.getFirst())))
            .collect(Collectors.toList());
    return result.stream()
        .sorted(Comparator.comparingDouble(OfferModuleDto::getSortCode))
        .collect(Collectors.toList());
  }
}
