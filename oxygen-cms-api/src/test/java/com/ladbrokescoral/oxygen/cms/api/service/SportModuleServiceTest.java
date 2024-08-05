package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.SportModuleArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.HomeInplaySportsTest;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.SportModuleTest;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeInplayConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier;
import com.ladbrokescoral.oxygen.cms.api.entity.VirtualRacingCarouselModuleConfig;
import com.ladbrokescoral.oxygen.cms.api.exception.DependencyDeleteException;
import com.ladbrokescoral.oxygen.cms.api.exception.RacingModuleConfigNotUniqException;
import com.ladbrokescoral.oxygen.cms.api.repository.SportModuleRepository;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.Collections;
import java.util.EnumSet;
import java.util.List;
import java.util.Optional;
import java.util.Random;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import javax.validation.ConstraintViolation;
import javax.validation.Validation;
import javax.validation.Validator;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.AdditionalAnswers;
import org.mockito.ArgumentCaptor;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;
import org.mockito.junit.MockitoJUnitRunner;
import org.modelmapper.ModelMapper;
import org.springframework.context.annotation.Import;

@RunWith(MockitoJUnitRunner.class)
@Import(ModelMapperConfig.class)
public class SportModuleServiceTest extends BDDMockito {
  private static final String CORAL_BRAND = "bma";

  @Mock private SportModuleRepository repository;
  @Spy private ModelMapper modelMapper;
  @Mock private DeleteEntityService deleteEntityService;
  @Mock private HomeInplaySportService homeInplaySportService;
  @Mock private SportModuleArchivalRepository sportModuleArchivalRepository;

  @InjectMocks private SportModuleService service;
  private final String expected_title = "test sort order";

  @Before
  public void setUp() {
    service =
        new SportModuleService(
            repository,
            deleteEntityService,
            homeInplaySportService,
            modelMapper,
            sportModuleArchivalRepository);
    given(repository.save(any(SportModule.class))).will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void testSortOrder() {
    assertNotNull(capture().getValue().getSortOrder());
  }

  @Test
  public void testPublishedDevices() {
    assertNotNull(capture().getValue().getPublishedDevices());
  }

  @Test
  public void testTitle() {
    assertEquals(expected_title, capture().getValue().getTitle());
  }

  @Test
  public void shouldCreateModulesOnRenew() {
    SportCategory sport = new SportCategory();
    Integer sportId = 16;
    sport.setCategoryId(sportId);
    sport.setBrand(CORAL_BRAND);
    sport.setTier(SportTier.TIER_1);

    List<SportModule> existingSportModules = Collections.emptyList();

    when(repository.findAllByBrandAndPageTypeAndPageIdAndModuleTypeInOrderBySortOrderAsc(
            CORAL_BRAND, PageType.sport, sportId.toString(), EnumSet.allOf(SportModuleType.class)))
        .thenReturn(existingSportModules);

    // when:
    service.renewModules(sport);

    // then:
    ArgumentCaptor<List> newModulesArg = ArgumentCaptor.forClass(List.class);
    verify(repository).saveAll(newModulesArg.capture());
    List<SportModule> newModules = newModulesArg.getValue();
    assertFalse(newModules.isEmpty());
    assertExistsOfEachType(newModules);
    assertInPlayConfig(
        findByType(newModules, SportModuleType.INPLAY).orElseThrow(RuntimeException::new),
        sport.getTier());
  }

  @Test
  public void shouldNotRenewForInvalidSport() {
    SportCategory sport = new SportCategory();
    sport.setCategoryId(null);

    // when:
    service.renewModules(sport);

    // then:
    verify(repository, never()).save(any(SportModule.class));
    verify(repository, never()).saveAll(anyList());
  }

  @Test(expected = RacingModuleConfigNotUniqException.class)
  public void shouldNotCreateDuplicateRacingModuleConfig() {
    SportModule sportModule = sportModule(21, SportModuleType.RACING_MODULE);
    sportModule.setId(null);
    sportModule.setRacingConfig(new VirtualRacingCarouselModuleConfig());

    when(repository.findAllByBrandAndPageTypeAndPageIdAndModuleTypeInOrderBySortOrderAsc(
            CORAL_BRAND,
            PageType.sport,
            sportModule.getPageId(),
            EnumSet.allOf(SportModuleType.class)))
        .thenReturn(Collections.singletonList(sportModule));

    service.save(sportModule);
  }

  @Test
  public void shouldPassValidationOnDuplicateRacingModuleConfigs() {
    given(repository.save(any(SportModule.class))).will(AdditionalAnswers.returnsFirstArg());

    SportModule sportModule = sportModule(21, SportModuleType.RACING_MODULE);
    sportModule.setId(null);
    sportModule.setRacingConfig(new VirtualRacingCarouselModuleConfig());

    when(repository.findAllByBrandAndPageTypeAndPageIdAndModuleTypeInOrderBySortOrderAsc(
            CORAL_BRAND,
            PageType.sport,
            sportModule.getPageId(),
            EnumSet.allOf(SportModuleType.class)))
        .thenReturn(Collections.emptyList());

    service.save(sportModule);

    verify(repository).save(any(SportModule.class));
  }

  @Test
  public void shouldPassInplayModuleConfigs() {
    given(repository.save(any(SportModule.class))).will(AdditionalAnswers.returnsFirstArg());

    SportModule sportModule = sportModule(0, SportModuleType.INPLAY);
    sportModule.setId(null);
    sportModule.setInplayConfig(new HomeInplayConfig());

    when(homeInplaySportService.findByBrand("bma"))
        .thenReturn(HomeInplaySportsTest.findAllEntites());

    service.save(sportModule);

    verify(repository).save(any(SportModule.class));
  }

  @Test
  public void shouldPassUpdateInplayModuleConfigs() {
    given(repository.save(any(SportModule.class))).will(AdditionalAnswers.returnsFirstArg());

    SportModule sportModule = sportModule(0, SportModuleType.INPLAY);
    sportModule.setId("12121212121");
    sportModule.setArchivalId("21212121");
    sportModule.setInplayConfig(new HomeInplayConfig());
    when(homeInplaySportService.findByBrand("bma"))
        .thenReturn(HomeInplaySportsTest.findAllEntites());

    service.save(sportModule);

    verify(repository).save(any(SportModule.class));
  }

  @Test
  public void shouldPassUpdateNullInplayModuleConfigs() {
    given(repository.save(any(SportModule.class))).will(AdditionalAnswers.returnsFirstArg());

    SportModule sportModule = sportModule(0, SportModuleType.INPLAY);
    sportModule.setId("12121212121");
    sportModule.setArchivalId("21212121");
    sportModule.setInplayConfig(null);
    service.save(sportModule);

    verify(repository).save(any(SportModule.class));
  }

  @Test
  public void racingModuleConfigValidations() {
    Set<ConstraintViolation<VirtualRacingCarouselModuleConfig>> violations;
    Validator validator = Validation.buildDefaultValidatorFactory().getValidator();

    VirtualRacingCarouselModuleConfig racingModuleConfig = new VirtualRacingCarouselModuleConfig();
    racingModuleConfig.setClassId(1);
    racingModuleConfig.setExcludeTypeIds("1");
    violations = validator.validate(racingModuleConfig);
    assertTrue(violations.isEmpty());

    racingModuleConfig.setExcludeTypeIds("1,2");
    violations = validator.validate(racingModuleConfig);
    assertTrue(violations.isEmpty());

    racingModuleConfig.setExcludeTypeIds("1, 2");
    violations = validator.validate(racingModuleConfig);
    assertTrue(violations.isEmpty());

    racingModuleConfig.setExcludeTypeIds("111, 222");
    violations = validator.validate(racingModuleConfig);
    assertTrue(violations.isEmpty());

    racingModuleConfig.setExcludeTypeIds("1,ab");
    violations = validator.validate(racingModuleConfig);
    assertFalse(violations.isEmpty());

    racingModuleConfig.setExcludeTypeIds("1");
    racingModuleConfig.setLimit(0);
    violations = validator.validate(racingModuleConfig);
    assertFalse(violations.isEmpty());

    racingModuleConfig.setClassId(-1);
    violations = validator.validate(racingModuleConfig);
    assertFalse(violations.isEmpty());
  }

  private void assertInPlayConfig(SportModule inplayModule, SportTier tier) {
    assertEquals(SportModuleType.INPLAY, inplayModule.getModuleType());
    assertEquals(10, inplayModule.getInplayConfig().getMaxEventCount());
    if (tier == SportTier.UNTIED) {
      assertTrue(inplayModule.isDisabled());
    } else {
      assertFalse(inplayModule.isDisabled());
    }
  }

  @Test
  public void shouldDeleteModulesBySport() throws Exception {
    int sportId = 10;
    List<SportModule> existingModules = sportModules(sportId);
    when(repository.findAllByBrandAndSportId(CORAL_BRAND, sportId)).thenReturn(existingModules);
    // when:
    service.deleteBySportId(CORAL_BRAND, sportId);
    // then:
    for (SportModule module : existingModules) {
      verify(deleteEntityService)
          .delete(
              module.getPageId(), module.getBrand(), module.getPageType(), module.getModuleType());
      verify(repository).delete(module);
    }
  }

  @Test
  public void shouldContinueDeleteModulesOnException() throws Exception {
    int sportId = 10;
    List<SportModule> existingModules = sportModules(sportId);
    when(repository.findAllByBrandAndSportId(CORAL_BRAND, sportId)).thenReturn(existingModules);
    // throw exception on one module
    SportModuleType brokenModuleType = SportModuleType.HIGHLIGHTS_CAROUSEL;
    doThrow(DependencyDeleteException.class)
        .when(deleteEntityService)
        .delete(String.valueOf(sportId), CORAL_BRAND, PageType.sport, brokenModuleType);
    // when:
    service.deleteBySportId(CORAL_BRAND, sportId);

    // then:
    for (SportModule module : existingModules) {
      verify(deleteEntityService)
          .delete(
              module.getPageId(), module.getBrand(), module.getPageType(), module.getModuleType());
      if (module.getModuleType() != brokenModuleType) {
        verify(repository).delete(module);
      } else {
        verify(repository, never()).delete(module);
      }
    }
  }

  @Test
  public void testFindAllByBrandAndSportModuleType() {

    when(repository.findAllByBrandAndModuleTypeOrderBySortOrderAsc("bma", SportModuleType.INPLAY))
        .thenReturn(SportModuleTest.createINplayModules());
    when(homeInplaySportService.findByBrand("bma"))
        .thenReturn(HomeInplaySportsTest.findAllEntites());

    List<SportModule> sportModules = service.findAll("bma", SportModuleType.INPLAY);
    Assert.assertEquals(3, sportModules.size());
  }

  private List<SportModule> sportModules(int sportId) {
    return Stream.of(SportModuleType.values())
        .map(type -> sportModule(sportId, type))
        .collect(Collectors.toList());
  }

  private void assertExistsOfEachType(List<SportModule> modules) {
    Stream.of(SportModuleType.values())
        .filter(type -> !SportModuleType.AEM_BANNERS.equals(type))
        .filter(type -> !SportModuleType.UNGROUPED_FEATURED.equals(type))
        .filter(type -> !SportModuleType.VIRTUAL_NEXT_EVENTS.equals(type))
        .filter(type -> !SportModuleType.POPULAR_BETS.equals(type))
        .filter(t -> !SportModuleType.BYB_WIDGET.equals(t))
        .filter(type -> !SportModuleType.POPULAR_ACCA.equals(type))
        .forEach(type -> assertTrue(findByType(modules, type).isPresent()));
  }

  private Optional<SportModule> findByType(List<SportModule> modules, SportModuleType type) {
    return modules.stream().filter(sportModule -> type == sportModule.getModuleType()).findAny();
  }

  private ArgumentCaptor<SportModule> capture() {
    service.save(sportModule());
    ArgumentCaptor<SportModule> argument = ArgumentCaptor.forClass(SportModule.class);
    verify(repository).save(argument.capture());

    return argument;
  }

  private SportModule sportModule(Integer sportId, SportModuleType moduleType) {
    SportModule module = sportModule();
    module.setSportId(sportId);
    module.setPageId(String.valueOf(sportId));
    module.setModuleType(moduleType);
    module.setId(String.valueOf(sportId) + new Random().nextInt());
    module.setPageType(PageType.sport);
    return module;
  }

  private SportModule sportModule() {
    SportModule module = new SportModule();
    module.setTitle(expected_title);
    module.setBrand(CORAL_BRAND);
    return module;
  }
}
