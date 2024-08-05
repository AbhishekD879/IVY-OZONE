package com.ladbrokescoral.oxygen.seo.cms.service;

import com.ladbrokescoral.oxygen.seo.configuration.CmsReactiveClient;
import com.ladbrokescoral.oxygen.seo.dto.*;
import com.ladbrokescoral.oxygen.seo.siteserver.service.SeoSiteServerService;
import com.ladbrokescoral.oxygen.seo.util.SeoConstants;
import com.ladbrokescoral.oxygen.seo.util.SeoUtil;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.ClientResponse;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Service
@Slf4j
@SuppressWarnings("java:S2142")
public class CmsReactiveServiceImpl implements CmsReactiveService {

  private CmsReactiveClient cmsReactiveClient;
  private SeoSiteServerService seoSiteServerService;
  private static final String UNDERSCORE = "_";
  private static final String DASH = "-";

  private static final String SLASH = "/";

  @Autowired
  public CmsReactiveServiceImpl(
      CmsReactiveClient cmsReactiveClient, SeoSiteServerService seoSiteServerService) {
    this.cmsReactiveClient = cmsReactiveClient;
    this.seoSiteServerService = seoSiteServerService;
  }

  @Override
  public Mono<Boolean> isVirtualSport(
      String brand, String sportTitle, String reqTrackTitle, String eventId) {
    return getVirtualSports(getBrandName(brand))
        .flatMap(
            (List<VirtualSportDto> sportDto) -> {
              Boolean flag = false;
              Optional<VirtualSportDto> sport =
                  sportDto.stream()
                      .filter(
                          virtualSportDto ->
                              SeoUtil.formatEventData(virtualSportDto.getTitle())
                                  .equalsIgnoreCase(sportTitle))
                      .findFirst();
              if (sport.isPresent()) {
                flag =
                    sport.get().getTracks().stream()
                        .anyMatch(
                            trackTitle ->
                                SeoUtil.formatEventData(trackTitle.getTitle())
                                    .equalsIgnoreCase(reqTrackTitle));
              }
              if (StringUtils.isNotBlank(eventId)) {
                try {
                  flag = seoSiteServerService.getEvent(eventId).toFuture().get();
                } catch (Exception e) {
                  log.error("Error in while hitting ss call");
                }
              }
              return Mono.just(flag);
            });
  }

  private Mono<List<VirtualSportDto>> getVirtualSports(String brand) {
    return cmsReactiveClient
        .getCMSWebClient()
        .get()
        .uri(uriBuilder -> uriBuilder.path("{brand}/virtual-sports").build(brand))
        .accept(MediaType.APPLICATION_JSON)
        .exchangeToMono(
            (ClientResponse clientResponse) -> {
              if (clientResponse.statusCode().isError()) {
                log.error("CMS virtual-sports API Failed");
                return clientResponse.createException().flatMap(Mono::error);
              } else {
                return clientResponse.bodyToMono(
                    new ParameterizedTypeReference<List<VirtualSportDto>>() {});
              }
            });
  }

  @Override
  public Mono<Boolean> isFanzone(String brand, String teamName, String tabName) {
    List<String> tabList = Arrays.asList("now-next", "club", "stats");
    return getFanzones(getBrandName(brand))
        .flatMap(
            (List<Fanzone> fanzones) -> {
              Boolean flag = false;
              flag =
                  fanzones.stream()
                      .anyMatch(
                          fanzone ->
                              fanzone.getName().equalsIgnoreCase(teamName)
                                  && tabList.stream().anyMatch(s -> s.equalsIgnoreCase(tabName)));
              return Mono.just(flag);
            });
  }

  private Mono<List<Fanzone>> getFanzones(String brand) {
    return cmsReactiveClient
        .getCMSWebClient()
        .get()
        .uri(uriBuilder -> uriBuilder.path("{brand}/fanzone").build(brand))
        .accept(MediaType.APPLICATION_JSON)
        .exchangeToMono(
            (ClientResponse clientResponse) -> {
              if (clientResponse.statusCode().isError()) {
                log.error("CMS fanzone API Failed");
                return clientResponse.createException().flatMap(Mono::error);
              } else {
                return clientResponse.bodyToMono(
                    new ParameterizedTypeReference<List<Fanzone>>() {});
              }
            });
  }

  @Override
  public Mono<Boolean> isEventHubData(String brand, String deviceType, Integer hubIndex) {
    return getEventHubDataResp(getBrandName(brand), getDeviceType(deviceType))
        .flatMap(
            (InitialDataDto initialDataDto) -> {
              Boolean flag =
                  initialDataDto.getModularContent().stream()
                      .filter(modularContentDto -> modularContentDto.getHubIndex() != null)
                      .anyMatch(
                          modularContentDto -> modularContentDto.getHubIndex().equals(hubIndex));
              return Mono.just(flag);
            });
  }

  @Override
  public Mono<Boolean> isSportName(String brand, String sportName, String deviceType) {

    return getEventHubDataResp(getBrandName(brand), getDeviceType(deviceType))
        .flatMap(
            (InitialDataDto initialDataDto) -> {
              Boolean flag =
                  initialDataDto.getSportCategories().stream()
                      .filter(Objects::nonNull)
                      .anyMatch(
                          initialDataSportCategoryDto ->
                              initialDataSportCategoryDto
                                  .getTargetUri()
                                  .equalsIgnoreCase("sport/" + sportName));
              return Mono.just(flag);
            });
  }

  private Mono<InitialDataDto> getEventHubDataResp(String brand, String deviceType) {
    return cmsReactiveClient
        .getCMSWebClient()
        .get()
        .uri(
            uriBuilder ->
                uriBuilder.path("{brand}/initial-data/{deviceType}").build(brand, deviceType))
        .accept(MediaType.APPLICATION_JSON)
        .exchangeToMono(
            (ClientResponse clientResponse) -> {
              if (clientResponse.statusCode().isError()) {
                log.error("CMS initial-data API Failed");
                return clientResponse.createException().flatMap(Mono::error);
              } else {
                return clientResponse.bodyToMono(
                    new ParameterizedTypeReference<InitialDataDto>() {});
              }
            });
  }

  @Override
  public Mono<Boolean> isPromotion(String brand, String promoKey) {
    return getPromotionResp(getBrandName(brand))
        .flatMap(
            (PromotionWithSectionContainerDto promotionWithSectionContainerDto) -> {
              Boolean flag = false;
              flag =
                  promotionWithSectionContainerDto.getPromotionsBySection().stream()
                      .anyMatch(
                          publicPromotionSectionDto ->
                              publicPromotionSectionDto.getPromotions().stream()
                                  .anyMatch(
                                      promotionDto ->
                                          promotionDto.getPromoKey().equalsIgnoreCase(promoKey)));
              return Mono.just(flag);
            });
  }

  private Mono<PromotionWithSectionContainerDto> getPromotionResp(String brand) {
    return cmsReactiveClient
        .getCMSWebClient()
        .get()
        .uri(uriBuilder -> uriBuilder.path("{brand}/grouped-promotions").build(brand))
        .accept(MediaType.APPLICATION_JSON)
        .exchangeToMono(
            (ClientResponse clientResponse) -> {
              if (clientResponse.statusCode().isError()) {
                log.error("CMS promotions API Failed");
                return clientResponse.createException().flatMap(Mono::error);
              } else {
                return clientResponse.bodyToMono(
                    new ParameterizedTypeReference<PromotionWithSectionContainerDto>() {});
              }
            });
  }

  @Override
  public Mono<Boolean> isSportTab(
      String brand, String categoryName, String tabName, String subTabName, String deviceType) {
    Optional<Integer> categoryId = getCategoryId(brand, deviceType, categoryName);
    log.info("getSportTab categoryId from CMS API: {}", categoryId);
    if (!categoryId.isPresent()) return Mono.just(false);
    String sport = "/sport";
    List<String> subTabList = Arrays.asList("today", "tomorrow", "future");
    return getSportTabResp(getBrandName(brand), categoryId.get().toString())
        .flatMap(
            (SportTabConfigListDto sportTabConfigListDto) -> {
              Boolean flag = false;
              Boolean subTabFlag = false;
              flag =
                  sportTabConfigListDto.getTabs().stream()
                      .filter(Objects::nonNull)
                      .anyMatch(
                          sportTabConfigDto ->
                              sportTabConfigDto
                                  .getUrl()
                                  .equalsIgnoreCase(sport + "/" + categoryName + "/" + tabName));
              if (StringUtils.isNotBlank(subTabName)) {
                subTabFlag = subTabList.stream().anyMatch(s -> s.equalsIgnoreCase(subTabName));
                log.info("sporttab>>>>> {} {} ", flag, subTabFlag);
                flag = flag && subTabFlag;
              }
              return Mono.just(flag);
            });
  }

  public Mono<SportTabConfigListDto> getSportTabResp(String brand, String categoryId) {
    return cmsReactiveClient
        .getCMSWebClient()
        .get()
        .uri(
            uriBuilder ->
                uriBuilder.path("{brand}/sport-tabs/{categoryId}").build(brand, categoryId))
        .accept(MediaType.APPLICATION_JSON)
        .exchangeToMono(
            (ClientResponse clientResponse) -> {
              if (clientResponse.statusCode().isError()) {
                log.error("CMS sport-tab API Failed");
                return clientResponse.createException().flatMap(Mono::error);
              } else {
                return clientResponse.bodyToMono(
                    new ParameterizedTypeReference<SportTabConfigListDto>() {});
              }
            });
  }

  public Mono<Boolean> isInplaySport(String brand, String categoryName) {
    return getCmsInplaySportResp(getBrandName(brand))
        .flatMap(
            (InplayDataDto inplayDataDto) -> {
              Boolean flag =
                  inplayDataDto.getActiveSportCategories().stream()
                      .anyMatch(
                          inplaySportCategoryDto ->
                              inplaySportCategoryDto.isShowInPlay()
                                  && getSportName(inplaySportCategoryDto.getSsCategoryCode())
                                      .equalsIgnoreCase(categoryName));
              return Mono.just(flag);
            });
  }

  private Mono<InplayDataDto> getCmsInplaySportResp(String brand) {
    return cmsReactiveClient
        .getCMSWebClient()
        .get()
        .uri(uriBuilder -> uriBuilder.path("{brand}/inplay-data").build(brand))
        .accept(MediaType.APPLICATION_JSON)
        .exchangeToMono(
            (ClientResponse clientResponse) -> {
              if (clientResponse.statusCode().isError()) {
                log.error("CMS inplay-data API Failed");
                return clientResponse.createException().flatMap(Mono::error);
              } else {
                return clientResponse.bodyToMono(
                    new ParameterizedTypeReference<InplayDataDto>() {});
              }
            });
  }

  public static String getBrandName(String brand) {
    return SeoConstants.CR_BRAND.equalsIgnoreCase(brand)
        ? SeoConstants.BMA
        : SeoConstants.LAD_BRAND;
  }

  public static String getDeviceType(String deviceType) {
    switch (deviceType) {
      case SeoConstants.DEVICE_D:
        return SeoConstants.DEVICE_D;
      case SeoConstants.DEVICE_T:
        return SeoConstants.DEVICE_T;
      default:
        return SeoConstants.DEVICE_M;
    }
  }

  private static String getSportName(String name) {
    log.info("in-play categoryName {} ", name);

    return name.replace(UNDERSCORE, DASH);
  }

  public Optional<Integer> getCategoryId(String brand, String deviceType, String sportName) {
    return getInitialDataApiResp(getBrandName(brand), getDeviceType(deviceType))
        .flatMap(
            (InitialDataDto initialDataDto) -> {
              Optional<InitialDataSportCategoryDto> initialDataSportCategoryDto =
                  initialDataDto.getSportCategories().stream()
                      .filter(
                          sportCategoryDto ->
                              sportCategoryDto
                                  .getSportConfig()
                                  .getConfig()
                                  .getPath()
                                  .equalsIgnoreCase(sportName))
                      .findFirst();
              return initialDataSportCategoryDto
                  .map(initialDto -> Mono.just(initialDto.getCategoryId()))
                  .orElse(Mono.empty());
            })
        .blockOptional();
  }

  public Mono<InitialDataDto> getInitialDataApiResp(String brand, String deviceType) {
    return cmsReactiveClient
        .getCMSWebClient()
        .get()
        .uri(
            uriBuilder ->
                uriBuilder.path("{brand}/initial-data/{deviceType}").build(brand, deviceType))
        .accept(MediaType.APPLICATION_JSON)
        .exchangeToMono(
            (ClientResponse clientResponse) -> {
              if (clientResponse.statusCode().isError()) {
                log.error("CMS initial-data API Failed");
                return clientResponse.createException().flatMap(Mono::error);
              }
              return clientResponse.bodyToMono(new ParameterizedTypeReference<InitialDataDto>() {});
            });
  }

  @Override
  public Mono<Boolean> isCompetition(String brand, String competitionName, String uri) {
    log.info("getCompetitionsReactive competitionName {} uri {} ", competitionName, uri);
    return getCompetitions(getBrandName(brand))
        .filter(
            competition ->
                competition.getCompetitionTabs().stream()
                    .anyMatch(
                        competitionTab ->
                            competitionTab
                                .getPath()
                                .equalsIgnoreCase(SLASH + competitionName + SLASH + uri)))
        .hasElements();
  }

  private Flux<Competition> getCompetitions(String brand) {
    return cmsReactiveClient
        .getCMSWebClient()
        .get()
        .uri(uriBuilder -> uriBuilder.path("{brand}/competition").build(brand))
        .accept(MediaType.APPLICATION_JSON)
        .exchangeToFlux(
            (ClientResponse clientResponse) -> {
              if (clientResponse.statusCode().isError()) {
                log.error("CMS Competition API Failed");
                return clientResponse.createException().flatMapMany(Mono::error);
              }
              return clientResponse.bodyToFlux(Competition.class);
            })
        .log();
  }
}
