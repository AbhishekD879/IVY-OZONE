package com.ladbrokescoral.oxygen.cms.api.service;

import static com.ladbrokescoral.oxygen.cms.api.entity.DeviceType.DESKTOP;
import static com.ladbrokescoral.oxygen.cms.api.entity.SvgSprite.FEATURED;
import static com.ladbrokescoral.oxygen.cms.api.entity.SvgSprite.INITIAL;

import com.ladbrokescoral.oxygen.cms.api.dto.InitialDataCFDto;
import com.ladbrokescoral.oxygen.cms.api.dto.InitialDataDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OddsBoostConfigDTO;
import com.ladbrokescoral.oxygen.cms.api.entity.DeviceType;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.*;
import java.util.Arrays;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@Slf4j
@RequiredArgsConstructor
public class InitialDataService {

  private final SportCategoryPublicService sportCategoryService;
  private final ModularContentPublicService modularContentService;
  private final SeoPagePublicService seoPageService;
  private final FooterMenuPublicService footerMenuService;
  private final SportPublicService sportService;
  private final InitSignpostingPublicService initSignpostingService;
  private final StructurePublicService structureService;
  private final NavigationPointService navigationPointService;
  private final ExtraNavigationPointPublicService extraNavigationPointPublicService;
  private final ConnectMenuPublicService connectMenuPublicService;
  private final OddsBoostConfigurationService oddsBoostConfigurationService;
  private final QuizPopupSettingPublicService quizPopupSettingService;
  private final VirtualSportPublicService virtualSportPublicService;
  private final SvgImagePublicService svgImagePublicService;
  private final TimelineConfigPublicService timelineConfigService;
  private final SeoAutoPagePublicService seoAutoPagePublicService;
  private final SegmentService segmentService;
  private final LuckyDipV2ConfigService luckyDipV2ConfigService;

  public InitialDataDto fetchInitialData(String brand, String deviceType, String segmentName) {
    InitialDataDto dto = new InitialDataDto();
    fillNonSegmentedModulesData(dto, brand, deviceType);
    fillSegmentedModulesData(dto, brand, deviceType, segmentName);
    return dto;
  }

  public InitialDataCFDto fetchCFInitialData(String brand, String deviceType) {
    InitialDataCFDto dto = new InitialDataCFDto();
    fillNonSegmentedModulesData(dto, brand, deviceType);
    fillSegmentedCollections(dto, brand);
    return dto;
  }

  private void fillNonSegmentedModulesData(InitialDataDto dto, String brand, String deviceType) {

    dto.setSystemConfiguration(structureService.getInitialDataConfiguration(brand));
    dto.setSports(sportService.findInitialData(brand));
    dto.setSeoPages(seoPageService.find(brand));
    dto.setInitSignposting(initSignpostingService.find(brand));
    dto.setConnectMenu(connectMenuPublicService.findByBrand(brand));
    dto.setExtraNavigationPoints(
        extraNavigationPointPublicService.findAllActiveExtraNavPointsByBrand(brand));
    dto.setLuckyDipConfigs(luckyDipV2ConfigService.getInitData(brand));
    quizPopupSettingService.findGeneralSettingsByBrand(brand).ifPresent(dto::setQuizPopupSetting);
    dto.setVsAliases(virtualSportPublicService.findAliases(brand));
    timelineConfigService.findGeneralConfigByBrand(brand).ifPresent(dto::setTimelineConfig);
    dto.setSeoAutoPages(seoAutoPagePublicService.find(brand));
    String svgSpriteContent;
    if (DESKTOP.getValue().equalsIgnoreCase(deviceType)) {
      svgSpriteContent =
          svgImagePublicService
              .getSvgSprites(
                  brand, Arrays.asList(INITIAL.getSpriteName(), FEATURED.getSpriteName()))
              .getContent();
    } else {
      svgSpriteContent =
          svgImagePublicService.getSvgSprite(brand, INITIAL.getSpriteName()).getContent();
    }
    dto.setSvgSpriteContent(svgSpriteContent);

    final OddsBoostConfigDTO oddsBoostConfigDTO = oddsBoostConfigurationService.getPublicDTO(brand);

    if (oddsBoostConfigDTO.isEnabled()) {
      dto.setOddsBoost(oddsBoostConfigDTO);
    }
  }

  private void fillSegmentedModulesData(
      InitialDataDto dto, String brand, String deviceType, String segmentName) {
    DeviceType device = DeviceType.fromString(deviceType).orElse(null);
    dto.setFooterMenu(footerMenuService.findInitialData(brand, deviceType, segmentName));
    dto.setNavigationPoints(
        navigationPointService.getNavigationPointByBrandEnabled(brand, segmentName, device));
    dto.setModularContent(
        modularContentService.prepareSegmentedInitialDataModularContent(
            brand, segmentName, device));
    dto.setSportCategories(sportCategoryService.findSportCategoriesInitialData(brand, segmentName));
  }

  private void fillSegmentedCollections(InitialDataCFDto dto, String brand) {
    dto.setFooterMenuCollection(footerMenuService.findAllActiveByBrand(brand));
    dto.setNavigationPointsCollection(navigationPointService.findAllActiveByBrand(brand));
    dto.setModularContentCollection(modularContentService.preparesModularContentCollection(brand));
    dto.setModularContentUniversal(
        modularContentService.prepareSegmentedInitialDataModularContent(
            brand, SegmentConstants.UNIVERSAL, DeviceType.MOBILE));
    dto.setSportCategoryCollection(sportCategoryService.findAllActiveByBrand(brand));
    dto.setSegmentCollection(segmentService.getSegmentsForSegmentedViews(brand));
  }
}
