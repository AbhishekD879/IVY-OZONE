package com.ladbrokescoral.oxygen.cms.api.service

import com.ladbrokescoral.oxygen.cms.api.entity.HomeInplaySport
import com.ladbrokescoral.oxygen.cms.api.repository.HomeInplaySportRepository
import org.modelmapper.ModelMapper

import com.ladbrokescoral.oxygen.cms.api.archival.repository.SportCategoryArchivalRepository
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier
import com.ladbrokescoral.oxygen.cms.api.exception.UnknownBrandException
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabService
import com.ladbrokescoral.oxygen.cms.configuration.ImageConfig
import spock.lang.Specification

class SportCategoryServiceSpec extends Specification {
  private static final String TEST_ID = "123456789"

  SportCategoryRepository repository
  SportTabService sportTabService
  SportModuleService sportModuleService
  SportCategoryService sportCategoryService
  ScheduledTaskExecutor scheduledTaskExecutorMock
  SiteServeService siteServeServiceMock
  SportCategoryArchivalRepository sportCategoryArchivalRepository
  SegmentService segmentService
  ModelMapper modelMapper =new ModelMapper()
  HomeInplaySportRepository homeInplaySportRepository
  def setup() {
    String imageSize = "1x1"
    repository = Mock(SportCategoryRepository)
    sportTabService = Mock()
    sportModuleService = Mock()
    scheduledTaskExecutorMock = Mock(ScheduledTaskExecutor)
    siteServeServiceMock = Mock(SiteServeService)
    sportCategoryArchivalRepository=Mock()
    segmentService=Mock()
    homeInplaySportRepository=Mock();
    sportCategoryService = new SportCategoryService(
        repository,
        sportTabService,
        sportModuleService,
        null, null, null,
        siteServeServiceMock,
        scheduledTaskExecutorMock,
        ImageConfig.ImagePath.builder()
        .svgMenuPath(imageSize)
        .smallPath(imageSize)
        .mediumPath(imageSize)
        .largePath(imageSize)
        .smallSize(new ImageServiceImpl.Size(imageSize))
        .mediumSize(new ImageServiceImpl.Size(imageSize))
        .largeSize(new ImageServiceImpl.Size(imageSize))
        .build(), ImageConfig.ImagePath.builder()
        .smallPath(imageSize)
        .mediumPath(imageSize)
        .largePath(imageSize)
        .smallSize(new ImageServiceImpl.Size(imageSize))
        .mediumSize(new ImageServiceImpl.Size(imageSize))
        .largeSize(new ImageServiceImpl.Size(imageSize))
        .build(),sportCategoryArchivalRepository,segmentService,modelMapper,homeInplaySportRepository)

    scheduledTaskExecutorMock.execute(_ as Runnable) >> { args ->
      args[0].run()
    }
  }

  def "updateHasEventsField cron job should save only sportCategories with changed hasEvents field" () {
    given:
    def sportWithoutEvents = sportCategory(16, SportTier.TIER_1)
    sportTabService.areThereEventsInCategoryBasedOnSportTabs(sportWithoutEvents) >> false

    def sportWithEvents = sportCategory(10, SportTier.TIER_2)
    sportTabService.areThereEventsInCategoryBasedOnSportTabs(sportWithEvents) >> true

    repository.findAllByDisabledFalse() >> Arrays.asList(sportWithoutEvents, sportWithEvents)

    def expectedToSaveSport = sportCategory(10, SportTier.TIER_2)
    expectedToSaveSport.setHasEvents(true)

    when:
    sportCategoryService.updateHasEventsField()

    then: "sportCategoryRepository saves only one entity, as 'hasEvents' field has changed only for sportCategory with categoryId=10"
    1 * repository.save(expectedToSaveSport)
  }

  def "test second sportCategory updated after the first one fails" () {
    given:
    def first = sportCategory(16, SportTier.TIER_1)
    def second = sportCategory(10, SportTier.TIER_2)

    repository.findAllByDisabledFalse() >> Arrays.asList(first, second)
    sportTabService.areThereEventsInCategoryBasedOnSportTabs(first) >> {throw new UnknownBrandException()}

    repository.findAllByDisabledFalse() >> Arrays.asList(first, second)
    sportTabService.areThereEventsInCategoryBasedOnSportTabs(second) >> true

    def expectedToSaveSport = sportCategory(10, SportTier.TIER_2)
    expectedToSaveSport.setHasEvents(true)

    when:
    sportCategoryService.updateHasEventsField()

    then: "sportCategoryRepository saves only one entity, as 'hasEvents' field has changed only for sportCategory with categoryId=10"
    1 * repository.save(expectedToSaveSport)
  }

  def "should create new sport category" () {
    given:
    SportCategory sportCategory = sportCategoryWithIdNull(10, SportTier.TIER_2)
    def  homeInplay =createHomeInplay("12121","mongo",16)
    homeInplaySportRepository.findByCategoryIdAndBrand(*_) >> homeInplay
    when:
    sportCategoryService.save(sportCategory)

    then:
    0 * repository.findByBrandAndCategoryId(sportCategory.getBrand(), sportCategory.getCategoryId())
    1 * repository.save(sportCategory) >> sportCategory
    1 * sportTabService.createTabs(sportCategory)
    1 * sportModuleService.renewModules(sportCategory)
  }

  def "should create new sport category with null categoryId" () {
    given:
    def untiedSportCategory = sportCategory(null, SportTier.UNTIED)
    def  homeInplay =createHomeInplay("12121","mongo1",16)
    homeInplaySportRepository.findByCategoryIdAndBrand(*_) >> homeInplay
    when:
    sportCategoryService.save(untiedSportCategory)

    then:
    0 * repository.findByBrandAndCategoryId(untiedSportCategory.getBrand(), untiedSportCategory.getCategoryId())
    1 * repository.save(untiedSportCategory) >> untiedSportCategory
    0 * sportTabService.createTabs(untiedSportCategory)
    0 * sportModuleService.renewModules(untiedSportCategory)
  }

  def "should delete sport category" () {
    given:
    SportCategory sportCategory = sportCategory(10, SportTier.TIER_2)
    sportCategory.setId(TEST_ID)
    repository.findById(TEST_ID) >> Optional.of(sportCategory)

    when:
    sportCategoryService.delete(TEST_ID)

    then:
    1 * repository.deleteById(TEST_ID)
    1 * sportTabService.deleteTabs(sportCategory)
  }

  def "should delete sport category with null categoryId" () {
    given:
    SportCategory untiedSportCategory = sportCategory(null, SportTier.UNTIED)
    untiedSportCategory.setId(TEST_ID)
    repository.findById(TEST_ID) >> Optional.of(untiedSportCategory)

    when:
    sportCategoryService.delete(TEST_ID)

    then:
    1 * repository.deleteById(TEST_ID)
    0 * sportTabService.deleteTabs(_ as SportCategory)
  }

  def "should not delete sport tabs and modules if there are more categories with categoryId" () {
    given:
    SportCategory untiedSportCategory = sportCategory(12, SportTier.UNTIED)
    untiedSportCategory.setId(TEST_ID)
    repository.findById(TEST_ID) >> Optional.of(untiedSportCategory)
    repository.existsByBrandAndCategoryId(untiedSportCategory.getBrand(), untiedSportCategory.getCategoryId()) >> true

    when:
    sportCategoryService.delete(TEST_ID)

    then:
    1 * repository.deleteById(TEST_ID)
    0 * sportTabService.deleteTabs(_ as SportCategory)
    0 * sportModuleService.deleteBySportId(*_)
  }

  def "should update SportCategory WITHOUT changing categoryId" () {
    given:
    def existingCategory = sportCategory(16, "111", "C2-Mongo")
    existingCategory.setHasEvents(true)
    def updatedCategory = sportCategory(16, existingCategory.getId(), "C1")
    def  homeInplay =createHomeInplay("12121","mongo",16)
    homeInplaySportRepository.findByCategoryIdAndBrand(*_) >> homeInplay
    and:
    repository.findByBrandAndCategoryId(updatedCategory.getBrand(), updatedCategory.getCategoryId()) >> [existingCategory]

    when:
    sportCategoryService.update(existingCategory, updatedCategory)

    then:
    1 * repository.save(updatedCategory) >> updatedCategory
    1 * sportModuleService.renewModules(updatedCategory)
    0 * sportTabService.deleteTabs(updatedCategory)
    0 * sportTabService.createTabs(updatedCategory)
  }

  def "should update SportCategory WITH changing categoryId" () {
    given:
    def existingCategory = sportCategory(16, SportTier.TIER_1)
    def updatedCategory = sportCategory(17, SportTier.TIER_1)
    def  homeInplay =createHomeInplay("12121","mongo",16)
    homeInplaySportRepository.findByCategoryIdAndBrand(*_) >> homeInplay
    and:
    repository.findByBrandAndCategoryId(updatedCategory.getBrand(), updatedCategory.getCategoryId()) >> [existingCategory]

    when:
    sportCategoryService.update(existingCategory, updatedCategory)

    then:
    1 * repository.save(updatedCategory) >> updatedCategory
    1 * sportModuleService.renewModules(updatedCategory)
    0 * sportTabService.deleteTabs(updatedCategory)
    0 * sportTabService.createTabs(updatedCategory)
  }

  def "should change sport categoryId TO null" () {
    given:
    def existingCategory = sportCategory(10, SportTier.TIER_2)
    def updatedCategory = sportCategory(null, SportTier.TIER_2)
    def  homeInplay =createHomeInplay("12121","mongo",16)
    homeInplaySportRepository.findByCategoryIdAndBrand(*_) >> homeInplay
    and:
    repository.findByBrandAndCategoryId(updatedCategory.getBrand(), updatedCategory.getCategoryId()) >> [existingCategory]

    when:
    sportCategoryService.update(existingCategory, updatedCategory)

    then:
    1 * repository.save(updatedCategory) >> updatedCategory
    1 * sportModuleService.renewModules(updatedCategory)
    1 * sportTabService.deleteTabs(existingCategory)
    0 * sportTabService.createTabs(updatedCategory)
  }

  def "should change sport categoryId FROM null" () {
    given:
    def existingCategory = sportCategory(null, SportTier.TIER_2)
    def updatedCategory = sportCategory(10, SportTier.TIER_2)
    def  homeInplay =createHomeInplay("12121","mongo",16)
    homeInplaySportRepository.findByCategoryIdAndBrand(*_) >> homeInplay
    and:
    repository.findByBrandAndCategoryId(updatedCategory.getBrand(), updatedCategory.getCategoryId()) >> [existingCategory]

    when:
    sportCategoryService.update(existingCategory, updatedCategory)

    then:
    1 * repository.save(updatedCategory) >> updatedCategory
    1 * sportModuleService.renewModules(updatedCategory)
    0 * sportTabService.deleteTabs(updatedCategory)
    1 * sportTabService.createTabs(updatedCategory)
  }

  def "should NOT change tier on update sport category" () {
    given:
    def existingCategory = sportCategory(16, SportTier.TIER_1)
    def newCategory = sportCategory(16, SportTier.TIER_2)
    def updatedCategory = existingCategory
    def  homeInplay =createHomeInplay("12121","mongo",16)
    homeInplaySportRepository.findByCategoryIdAndBrand(*_) >> homeInplay
    and:
    repository.findByBrandAndCategoryId(updatedCategory.getBrand(), updatedCategory.getCategoryId()) >> [existingCategory]
    when:
    sportCategoryService.update(existingCategory, newCategory)

    then:
    1 * repository.save(newCategory) >> newCategory
  }

  private static SportCategory sportCategory(Integer categoryId, SportTier tier) {
    SportCategory sport = new SportCategory()
    sport.setCategoryId(categoryId)
    sport.setTier(tier)
    sport.setBrand("bma")
    sport.setId(TEST_ID)
    return sport
  }
  private static SportCategory sportCategoryWithIdNull(Integer categoryId, SportTier tier) {
    SportCategory sport = new SportCategory()
    sport.setCategoryId(categoryId)
    sport.setTier(tier)
    sport.setBrand("bma")
    sport.setImageTitle("mongo")
    return sport
  }

  private static SportCategory sportCategory(Integer categoryId, String id, String alt) {
    def sport = sportCategory(categoryId, null)
    sport.setId(id)
    sport.setAlt(alt)
    return sport
  }

  def "should retrieve one sport category by categoryId" () {
    def cricketCategory = sportCategory(10, SportTier.UNTIED)
    given:
    repository.findByBrandAndCategoryId("bma", 10) >> Arrays.asList(cricketCategory)
    when:
    def actualCategory = sportCategoryService.findOneByCategoryId("bma", 10)
    then:
    actualCategory.isPresent()
    actualCategory.get() == cricketCategory
  }


  private static List<HomeInplaySport> createHomeInplay(String id, String name, Integer categoryId) {
    List<HomeInplaySport> sports=new ArrayList<>()
    HomeInplaySport sport = new HomeInplaySport()
    sport.setId(id)
    sport.setBrand("bma")
    sport.setCategoryId(String.valueOf(categoryId))
    sport.setSportName(name)
    sports.add(sport)
    return sports
  }
}
