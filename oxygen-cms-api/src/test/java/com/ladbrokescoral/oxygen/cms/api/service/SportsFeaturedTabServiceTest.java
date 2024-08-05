package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;

import com.ladbrokescoral.oxygen.cms.api.entity.SimpleModule;
import com.ladbrokescoral.oxygen.cms.api.entity.SportsFeaturedTab;
import com.ladbrokescoral.oxygen.cms.api.repository.SportsFeaturedTabRepository;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.AdditionalAnswers;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class SportsFeaturedTabServiceTest extends BDDMockito {

  @Mock private SportsFeaturedTabRepository repository;

  @InjectMocks private SportsFeaturedTabService service;

  @Before
  public void init() throws Exception {
    given(repository.save(any(SportsFeaturedTab.class))).will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void testAddModuleToEmptyFeatureTab() {
    String featureTabId = "123";
    when(repository.findById(featureTabId)).thenReturn(Optional.ofNullable(testFeatureTabEntity()));

    Optional<SportsFeaturedTab> featuredTab =
        service.addNewModule(
            featureTabId, SimpleModule.builder().displayOrder(1).originalName("Mod1").build());

    assertTrue(featuredTab.isPresent());
    assertEquals(1, featuredTab.get().getModules().size());
    SimpleModule module = featuredTab.get().getModules().get(0);
    assertNotNull(module.getId());
    assertEquals("Mod1", module.getOriginalName());
    assertEquals(1, (int) module.getDisplayOrder());
    assertFalse(module.isDisabled());
  }

  @Test
  public void testUpdateExistingModule() {
    String featureTabId = "123";
    SportsFeaturedTab sportsFeaturedTab = testFeatureTabEntity();
    SimpleModule existingModule =
        SimpleModule.builder()
            .id("321")
            .displayOrder(-1)
            .originalName("Mod1")
            .disabled(false)
            .description("Mod one")
            .build();
    sportsFeaturedTab.getModules().add(existingModule);
    when(repository.findById(featureTabId)).thenReturn(Optional.ofNullable(sportsFeaturedTab));

    SimpleModule updatedModule =
        SimpleModule.builder()
            .id("321")
            .originalName("Mod1m")
            .disabled(true)
            .description("Mode one modified")
            .displayOrder(100)
            .build();
    Optional<SportsFeaturedTab> updatedFeatureTab = service.updateModule("123", updatedModule);

    assertTrue(updatedFeatureTab.isPresent());
    assertEquals(1, updatedFeatureTab.get().getModules().size());
    SimpleModule simpleModule = updatedFeatureTab.get().getModules().get(0);
    assertEquals("321", simpleModule.getId());
    assertEquals("Mod1m", simpleModule.getOriginalName());
    assertEquals(100, (int) simpleModule.getDisplayOrder());
    assertTrue(simpleModule.isDisabled());
  }

  @Test
  public void testUpdateUnexistingModule() {
    when(repository.findById("123")).thenReturn(Optional.ofNullable(testFeatureTabEntity()));

    SimpleModule module =
        SimpleModule.builder().id("321").originalName("Test").displayOrder(1).build();
    Optional<SportsFeaturedTab> featuredTab = service.updateModule("123", module);
    assertFalse(featuredTab.isPresent());
  }

  @Test
  public void testDeleteModule() {
    SportsFeaturedTab featureTab = testFeatureTabEntity();
    SimpleModule module = SimpleModule.builder().id("312").originalName("Test1").build();
    featureTab.getModules().add(module);

    when(repository.findById("123")).thenReturn(Optional.ofNullable(featureTab));

    Optional<SportsFeaturedTab> featuredTab = service.removeModule("123", "312");
    assertTrue(featuredTab.isPresent());
    assertEquals(0, featuredTab.get().getModules().size());
  }

  @Test
  public void testModulesWithNullDisplayOrderAreInTheEndOfCollection() {
    List<SimpleModule> modules = new ArrayList<>();
    modules.add(SimpleModule.builder().originalName("Test5").displayOrder(null).build());
    modules.add(SimpleModule.builder().originalName("Test4").displayOrder(null).build());
    modules.add(SimpleModule.builder().originalName("Test2").displayOrder(0).build());
    modules.add(SimpleModule.builder().originalName("Test3").displayOrder(-1).build());
    modules.add(SimpleModule.builder().originalName("Test1").displayOrder(1).build());

    SportsFeaturedTab sportsFeaturedTab = testFeatureTabEntity();
    sportsFeaturedTab.setModules(modules);
    when(repository.findByBrandIgnoreCaseAndPathIgnoreCaseAndDisabledIsFalse(
            anyString(), anyString()))
        .thenReturn(sportsFeaturedTab);

    Optional<SportsFeaturedTab> enabledByBrandAndPath =
        service.findEnabledByBrandAndPath("brand", "path");
    assertTrue(enabledByBrandAndPath.isPresent());
    List<SimpleModule> modulesFound = enabledByBrandAndPath.get().getModules();
    assertEquals(5, modulesFound.size());
    assertEquals("Test3", modulesFound.get(0).getOriginalName());
    assertEquals("Test2", modulesFound.get(1).getOriginalName());
    assertEquals("Test1", modulesFound.get(2).getOriginalName());
    assertEquals("Test5", modulesFound.get(3).getOriginalName());
    assertEquals("Test4", modulesFound.get(4).getOriginalName());
  }

  private static SportsFeaturedTab testFeatureTabEntity() {
    SportsFeaturedTab sportsFeaturedTab = new SportsFeaturedTab();
    sportsFeaturedTab.setId("123");
    sportsFeaturedTab.setName("Test");
    sportsFeaturedTab.setCategoryId("32");
    sportsFeaturedTab.setPath("/test");
    return sportsFeaturedTab;
  }
}
