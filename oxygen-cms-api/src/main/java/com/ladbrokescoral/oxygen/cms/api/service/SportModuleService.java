package com.ladbrokescoral.oxygen.cms.api.service;

import com.fortify.annotations.FortifyXSSValidate;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SportModuleArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.entity.SportModuleArchive;
import com.ladbrokescoral.oxygen.cms.api.entity.AemBannersConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeInplayConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeInplaySport;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.RpgConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.exception.DependencyDeleteException;
import com.ladbrokescoral.oxygen.cms.api.exception.RacingModuleConfigNotUniqException;
import com.ladbrokescoral.oxygen.cms.api.repository.SportModuleRepository;
import java.time.Instant;
import java.util.Collections;
import java.util.EnumSet;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.text.WordUtils;
import org.bson.types.ObjectId;
import org.modelmapper.ModelMapper;
import org.owasp.html.HtmlPolicyBuilder;
import org.owasp.html.PolicyFactory;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;
import org.springframework.util.StringUtils;

@Slf4j
@Service
public class SportModuleService extends SortableService<SportModule> {
  private final SportModuleRepository moduleRepository;
  private DeleteEntityService deleteEntityService;
  private HomeInplaySportService homeInplaySportService;
  private final SportModuleArchivalRepository sportModuleArchivalRepository;

  private ModelMapper modelMapper;

  public SportModuleService(
      SportModuleRepository repository,
      DeleteEntityService entityService,
      HomeInplaySportService homeInplaySportService,
      ModelMapper modelMapper,
      SportModuleArchivalRepository sportModuleArchivalRepository) {
    super(repository);
    this.moduleRepository = repository;
    this.deleteEntityService = entityService;
    this.homeInplaySportService = homeInplaySportService;
    this.modelMapper = modelMapper;
    this.sportModuleArchivalRepository = sportModuleArchivalRepository;
  }

  public List<SportModule> findAllActive(String brand) {
    return moduleRepository.findAllByBrandAndDisabledAndModuleTypeInOrderBySortOrderAsc(
        brand, false, EnumSet.allOf(SportModuleType.class));
  }

  public List<SportModule> findAll(String brand, PageType pageType, String pageId) {
    return moduleRepository.findAllByBrandAndPageTypeAndPageIdAndModuleTypeInOrderBySortOrderAsc(
        brand, pageType, pageId, EnumSet.allOf(SportModuleType.class));
  }

  public List<SportModule> findAll(String brand, SportModuleType moduleType) {
    List<SportModule> sportModules =
        moduleRepository.findAllByBrandAndModuleTypeOrderBySortOrderAsc(brand, moduleType);
    return updateInplayModule(sportModules, brand);
  }

  private List<SportModule> updateInplayModule(List<SportModule> sportModules, String brand) {
    sportModules.stream()
        .filter(this::isInPlayModuleAndHomePage)
        .forEach(sportModule -> updateHomeInplayModule(sportModule, brand));

    return sportModules;
  }

  public List<SportModule> findAllActive(String brand, SportModuleType moduleType) {
    return moduleRepository.findAllByBrandAndModuleTypeAndDisabledFalseOrderBySortOrderAsc(
        brand, moduleType);
  }

  public Optional<SportModule> findOne(
      String brand, PageType pageType, String sportId, SportModuleType moduleType) {
    return moduleRepository.findAllByBrandAndPageTypeAndPageIdAndModuleType(
        brand, pageType, sportId, moduleType);
  }

  @Override
  public SportModule save(SportModule entity) {
    sanitizeRpgConfig(entity);
    validateRacingModulesAreUniq(entity);
    if (!StringUtils.hasText(entity.getArchivalId()))
      entity.setArchivalId(ObjectId.get().toHexString());
    if (entity.getInplayConfig() != null)
      entity.getInplayConfig().setHomeInplaySports(Collections.emptyList());
    SportModule module = super.save(entity);
    saveArhcival(module, false);
    return module;
  }

  private void saveArhcival(SportModule module, boolean isdeleted) {

    SportModuleArchive archive = modelMapper.map(module, SportModuleArchive.class);
    archive.setId(null);
    archive.setDeleted(isdeleted);
    if (isInPlayModuleAndHomePage(module) && module.getInplayConfig() != null) {

      List<HomeInplaySport> homeInplaySports =
          homeInplaySportService.findByBrand(module.getBrand()).stream()
              .parallel()
              .filter(
                  inplay ->
                      inplay.isUniversalSegment()
                          || !CollectionUtils.isEmpty(inplay.getInclusionList()))
              .collect(Collectors.toList());
      archive.getInplayConfig().setHomeInplaySports(homeInplaySports);
    }
    sportModuleArchivalRepository.save(archive);
  }

  private void validateRacingModulesAreUniq(SportModule entity) {
    if (entity.isNew()
        && Objects.nonNull(entity.getModuleType())
        && entity.getModuleType().equals(SportModuleType.RACING_MODULE)
        && findAll(entity.getBrand(), entity.getPageType(), entity.getPageId()).stream()
            .filter(sm -> Objects.nonNull(sm.getRacingConfig()))
            .anyMatch(
                sm -> sm.getRacingConfig().getType().equals(entity.getRacingConfig().getType()))) {
      throw new RacingModuleConfigNotUniqException();
    }
  }

  private void sanitizeRpgConfig(SportModule entity) {
    RpgConfig rpgConfig = entity.getRpgConfig();
    if (rpgConfig != null) {
      PolicyFactory policy = new HtmlPolicyBuilder().allowStandardUrlProtocols().toFactory();

      rpgConfig.setTitle(policy.sanitize(rpgConfig.getTitle()));
      rpgConfig.setSeeMoreLink(policy.sanitize(rpgConfig.getSeeMoreLink()));
      // sanitize method returns "" instead of null, as the result the URL becomes
      // invalid
      if (rpgConfig.getBundleUrl() != null) {
        rpgConfig.setBundleUrl(policy.sanitize(rpgConfig.getBundleUrl()));
      }
      if (rpgConfig.getLoaderUrl() != null) {
        rpgConfig.setLoaderUrl(policy.sanitize(rpgConfig.getLoaderUrl()));
      }
    }
  }

  @Override
  public void delete(String id) {
    findOne(id).ifPresent(this::deleteDependencies);
  }

  private void deleteDependencies(SportModule module) {
    try {
      deleteEntityService.delete(
          module.getPageId(), module.getBrand(), module.getPageType(), module.getModuleType());
      moduleRepository.delete(module);
      saveArhcival(module, true);
    } catch (Exception e) {
      throw new DependencyDeleteException(e);
    }
  }

  @Override
  public List<SportModule> findByBrand(String brand) {
    return moduleRepository.findAllByBrandAndModuleTypeIn(
        brand, EnumSet.allOf(SportModuleType.class));
  }

  public void renewModules(SportCategory sportCategory) {
    if (Objects.isNull(sportCategory.getCategoryId())) {
      log.warn(
          "Sport category {} without siteserver categoryId, brand {}",
          sportCategory.getAlt(),
          sportCategory.getBrand());
      return;
    }
    List<SportModule> sportModules =
        findAll(sportCategory.getBrand(), PageType.sport, sportCategory.getCategoryId().toString());
    Set<SportModuleType> existingTypes =
        sportModules.stream().map(SportModule::getModuleType).collect(Collectors.toSet());

    List<SportModule> newModules =
        Stream.of(SportModuleType.values())
            .filter(t -> !existingTypes.contains(t))
            .filter(t -> !SportModuleType.AEM_BANNERS.equals(t))
            .filter(t -> !SportModuleType.UNGROUPED_FEATURED.equals(t))
            .filter(t -> !SportModuleType.VIRTUAL_NEXT_EVENTS.equals(t))
            .filter(t -> !SportModuleType.POPULAR_BETS.equals(t))
            .filter(t -> !SportModuleType.BYB_WIDGET.equals(t))
            .filter(t -> !SportModuleType.POPULAR_ACCA.equals(t))
            .map(t -> createSportModule(t, sportCategory))
            .collect(Collectors.toList());
    createAemBanners(newModules, sportCategory, existingTypes);
    super.save(newModules);
  }

  private void createAemBanners(
      List<SportModule> newModules,
      SportCategory sportCategory,
      Set<SportModuleType> existingTypes) {
    if (existingTypes.stream().anyMatch(SportModuleType.AEM_BANNERS::equals)) {
      return;
    }
    newModules.add(createAemBannerModule(sportCategory, 1));
    newModules.add(createAemBannerModule(sportCategory, 2));
    newModules.add(createAemBannerModule(sportCategory, 3));
    newModules.add(createAemBannerModule(sportCategory, 4));
  }

  private SportModule createAemBannerModule(SportCategory sportCategory, int index) {
    SportModule module = createSportModule(SportModuleType.AEM_BANNERS, sportCategory);
    module.setTitle("AEM banners carousel #" + index);
    module.setSortOrder((double) index);
    module.setModuleConfig(
        AemBannersConfig.builder()
            .maxOffers(7)
            .timePerSlide(7)
            .displayFrom(Instant.now())
            .displayTo(Instant.now().plusSeconds(10))
            .build());
    return module;
  }

  private SportModule createSportModule(SportModuleType moduleType, SportCategory sportCategory) {
    SportModule module = new SportModule();
    module.setBrand(sportCategory.getBrand());
    module.setModuleType(moduleType);
    module.setSportId(sportCategory.getCategoryId());
    module.setPageId(String.valueOf(sportCategory.getCategoryId()));
    module.setPageType(PageType.sport);
    module.setTitle(WordUtils.capitalizeFully(moduleType.name().replace("_", " ") + " Module"));
    module.setPublishedDevices(Collections.emptyList());
    module.setSortOrder(0.0);
    module.setDisabled(true);
    if (SportModuleType.INPLAY.equals(moduleType)) {
      module.setInplayConfig(new HomeInplayConfig());
      if (SportTier.UNTIED != sportCategory.getTier()) {
        module.setDisabled(false);
      }
    } else if (SportModuleType.RECENTLY_PLAYED_GAMES.equals(moduleType)) {
      module.setRpgConfig(new RpgConfig());
      sanitizeRpgConfig(module);
    }

    return module;
  }

  public void deleteBySportId(String brand, Integer categoryId) {
    moduleRepository
        .findAllByBrandAndSportId(brand, categoryId)
        .forEach(
            (SportModule module) -> {
              try {
                deleteDependencies(module);
              } catch (DependencyDeleteException e) {
                log.error(
                    "Cannot delete dependency for module {}. SportId {}",
                    module.getId(),
                    module.getSportId(),
                    e);
              }
            });
  }

  @FortifyXSSValidate("return")
  @Override
  public Optional<SportModule> findOne(String id) {
    Optional<SportModule> sportModule = repository.findById(id);
    return sportModule.isPresent()
        ? Optional.of(updateUniversalSportModule(sportModule.get()))
        : sportModule;
  }

  private SportModule updateUniversalSportModule(SportModule sportModule) {
    return isInPlayModuleAndHomePage(sportModule)
        ? updateUniversalHomeInpalyModule(sportModule)
        : sportModule;
  }

  private boolean isInPlayModuleAndHomePage(SportModule sportModule) {
    return SportModuleType.INPLAY.equals(sportModule.getModuleType())
        && "0".equals(sportModule.getPageId());
  }

  private SportModule updateUniversalHomeInpalyModule(SportModule sportModule) {

    List<HomeInplaySport> homeInplaySports =
        homeInplaySportService.findByBrandAndSegmentName(
            sportModule.getBrand(), SegmentConstants.UNIVERSAL);
    sportModule.getInplayConfig().setHomeInplaySports(homeInplaySports);
    return sportModule;
  }

  private SportModule updateHomeInplayModule(SportModule sportModule, String brand) {

    List<HomeInplaySport> homeInplaySports =
        homeInplaySportService.findByBrand(brand).stream()
            .parallel()
            .filter(
                inplay ->
                    inplay.isUniversalSegment()
                        || !CollectionUtils.isEmpty(inplay.getInclusionList()))
            .collect(Collectors.toList());
    sportModule.getInplayConfig().setHomeInplaySports(homeInplaySports);
    return sportModule;
  }
}
