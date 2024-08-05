package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.OfferDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OfferModuleDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Offer;
import com.ladbrokescoral.oxygen.cms.api.entity.OfferModule;
import com.ladbrokescoral.oxygen.cms.api.mapping.OfferMapper;
import com.ladbrokescoral.oxygen.cms.api.service.OfferModuleService;
import com.ladbrokescoral.oxygen.cms.api.service.OfferService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;
import org.bson.types.ObjectId;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.data.util.Pair;
import org.springframework.stereotype.Component;

@Component
public class OfferAfterSaveListener extends BasicMongoEventListener<Offer> {
  private final OfferService service;
  private final OfferModuleService moduleService;
  private static final String PATH_TEMPLATE = "api/v2/{0}/offers";

  public OfferAfterSaveListener(
      final OfferService service,
      final OfferModuleService moduleService,
      final DeliveryNetworkService context) {
    super(context);
    this.service = service;
    this.moduleService = moduleService;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<Offer> event) {
    List<String> deviceTypeList =
        event.getSource().getShowOfferOn().equals("both")
            ? Arrays.asList("tablet", "desktop")
            : Arrays.asList(event.getSource().getShowOfferOn());

    for (String deviceType : deviceTypeList) {
      String brand = event.getSource().getBrand();
      List<OfferModuleDto> content = getContent(brand, deviceType);
      uploadCollection(brand, PATH_TEMPLATE, deviceType, content);
    }
  }

  private List<OfferModuleDto> getContent(String brand, String deviceType) {
    // collect pairs of module id & module name
    List<OfferModule> offerModuleList =
        moduleService.findByBrandAndDeviceType(brand, deviceType).stream()
            .collect(Collectors.toList());

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
