package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.*;

import com.egalacoral.spark.siteserver.model.Category;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Type;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.CompetitionRepository;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class CompetitionServiceTest {

  @Mock private CompetitionRepository repository;
  @Mock private CompetitionTabService competitionTabService;
  CompetitionService service;
  Competition competition;
  @Mock SiteServeService siteServeService;
  @Mock SportCategoryService sportCategoryService;

  @Before
  public void init() throws Exception {

    service =
        new CompetitionService(
            repository, competitionTabService, siteServeService, sportCategoryService);

    competition = TestUtil.deserializeWithJackson("test/competition.json", Competition.class);
    doReturn(Optional.of(competition)).when(repository).findById("competitionId");
    doReturn(competition).when(repository).save(competition);
  }

  @Test
  public void saveTest() {
    service.save(competition);
    verify(repository, times(1)).save(competition);
  }

  @Test
  public void findOneTest() {
    Competition result = service.getCompetitionByid("competitionId");
    verify(repository, times(1)).findById("competitionId");
    assertEquals(competition, result);
  }

  @Test
  public void findAllTest() {
    doReturn(Collections.singletonList(competition)).when(repository).findAll();
    List<Competition> banners = service.findAll();
    verify(repository, times(1)).findAll();
    assertTrue(banners.contains(competition));
  }

  @Test
  public void findByBrandTest() {
    String brand = "testBrand";
    doReturn(Collections.singletonList(competition))
        .when(repository)
        .findByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC);
    List<Competition> competitions = service.findByBrand(brand);
    verify(repository, times(1)).findByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC);
    assertTrue(competitions.contains(competition));
  }

  @Test
  public void getCompetitionByUriTest() {
    String testUri = "testUri";
    doReturn(Optional.ofNullable(competition))
        .when(repository)
        .findByBrandAndUri(competition.getBrand(), "/" + testUri);
    Optional<Competition> competitionOpt =
        service.getCompetitionByBrandAndUri(competition.getBrand(), testUri);
    verify(repository, times(1)).findByBrandAndUri(competition.getBrand(), "/" + testUri);
    assertEquals(competition, competitionOpt.get());
  }

  @Test
  public void getCompetitionTabTest() {
    CompetitionTab competitionTab =
        service.getCompetitionTab("id", "5aafd7edc9e77c000110zzzz", competition);
    assertEquals("5aafd7edc9e77c000110zzzz", competitionTab.getId());
  }

  @Test
  public void getCompetitionParticipantTest() {
    CompetitionParticipant competitionParticipant =
        service.getCompetitionParticipant("comPart1", competition);
    assertEquals("comPart1", competitionParticipant.getId());
  }

  @Test(expected = NotFoundException.class)
  public void getCompetitionParticipantTest_NotFoundException() {
    service.getCompetitionParticipant("NonExistingCPId", competition);
  }

  @Test
  public void getCompetitionTabModuleTest() {

    CompetitionTab competitionTab =
        service.getCompetitionTab("id", "5aafd7edc9e77c000110zzzz", competition);
    CompetitionModule competitionModule =
        service.getCompetitionTabModule("id", "competitionModule1", competitionTab);
    assertEquals("competitionModule1", competitionModule.getId());
  }

  @Test
  public void getCompetitionSubTabModuleTest() {

    CompetitionTab competitionTab =
        service.getCompetitionTab("id", "5aafd7edc9e77c000110zzzz", competition);
    CompetitionModule competitionModule =
        service.getCompetitionSubTabModule(
            "id", "competitionSubModule1", competitionTab.getCompetitionSubTabs().get(0));

    assertEquals("competitionSubModule1", competitionModule.getId());
  }

  @Test
  public void getCompetitionSubTabTest() {

    CompetitionTab competitionTab =
        service.getCompetitionTab("id", "5aafd7edc9e77c000110zzzz", competition);
    CompetitionSubTab competitionSubTab =
        service.getCompetitionSubTab("id", "competitionSubTab1", competitionTab);

    assertEquals("competitionSubTab1", competitionSubTab.getId());
  }

  @Test
  public void testUpdateCompetitionId() {
    SportCategory sportCategory = new SportCategory();
    sportCategory.setCategoryId(16);
    sportCategory.setBrand("bma");
    sportCategory.setImageTitle("world cup");
    Competition competition = new Competition();
    competition.setName("world cup");

    doReturn(Optional.of(competition)).when(repository).findByBrandAndName(any(), any());
    service.updateCompetitionSportId(sportCategory);
    verify(repository, times(1)).findByBrandAndName(any(), any());
  }

  @Test
  public void testUpdateEmptyCompetition() {
    SportCategory sportCategory = new SportCategory();
    sportCategory.setCategoryId(19);
    sportCategory.setBrand("bma");
    sportCategory.setImageTitle("Racing");

    doReturn(Optional.empty()).when(repository).findByBrandAndName(any(), any());

    service.updateCompetitionSportId(sportCategory);
    verify(repository, times(1)).findByBrandAndName(any(), any());
  }

  @Test
  public void testPopulateCategoryIdAndClassId()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    Category category = getCategory();
    Children children = getChildren();
    category.setChildren(Collections.singletonList(children));
    Competition competition = getCompetition();
    SportCategory sportCategory = new SportCategory();
    sportCategory.setId("44");
    sportCategory.setBrand("bma");
    sportCategory.setImageTitle("world cup");
    doReturn(Optional.of(Collections.singletonList(category)))
        .when(siteServeService)
        .getClassToSubTypeForType(any(), any());
    doReturn(Collections.singletonList(sportCategory))
        .when(sportCategoryService)
        .findSportCategoryByBrandAndImageTitle(any(), any());
    populateMethodInvocation(competition);
    verify(sportCategoryService, times(1)).findSportCategoryByBrandAndImageTitle(any(), any());
    verify(siteServeService, times(1)).getClassToSubTypeForType(any(), any());
  }

  @Test(expected = InvocationTargetException.class)
  public void testPopulateCategoryIdAndClassIdForEmptyCategory()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    Competition competition = getCompetition();
    doReturn(Optional.empty()).when(siteServeService).getClassToSubTypeForType(any(), any());
    populateMethodInvocation(competition);
    verify(siteServeService, times(1)).getClassToSubTypeForType(any(), any());
  }

  @Test(expected = InvocationTargetException.class)
  public void testPopulateCategoryIdAndClassIdForZeroCategory()
      throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
    Competition competition = getCompetition();
    competition.setTypeId(444);
    doReturn(Optional.of(Collections.emptyList()))
        .when(siteServeService)
        .getClassToSubTypeForType(any(), any());
    populateMethodInvocation(competition);
    verify(siteServeService, times(1)).getClassToSubTypeForType(any(), any());
  }

  @Test(expected = InvocationTargetException.class)
  public void testPopulateCategoryIdAndClassIdForDifferentTypeId()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    Competition competition = getCompetition();
    competition.setTypeId(444);
    Category category = getCategory();
    Children children = getChildren();
    category.setChildren(Collections.singletonList(children));
    doReturn(Optional.of(Collections.singletonList(category)))
        .when(siteServeService)
        .getClassToSubTypeForType(any(), any());
    populateMethodInvocation(competition);
    verify(siteServeService, times(1)).getClassToSubTypeForType(any(), any());
  }

  private Competition getCompetition() {
    Competition competition = new Competition();
    competition.setId("22");
    competition.setTypeId(442);
    competition.setName("world cup");
    competition.setBrand("bma");
    return competition;
  }

  private Category getCategory() {
    Category category = new Category();
    category.setId(11);
    category.setCategoryId(16);
    return category;
  }

  private Children getChildren() {
    Children children = new Children();
    Type type = new Type();
    type.setId(442);
    children.setType(type);
    return children;
  }

  private void populateMethodInvocation(Competition competition)
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    Method method =
        CompetitionService.class.getDeclaredMethod(
            "popolateCategoryIdAndClassId", Competition.class);
    method.setAccessible(true);
    method.invoke(service, competition);
  }
}
