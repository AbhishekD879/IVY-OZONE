package com.ladbrokescoral.oxygen.cms.api.controller.private_api

import com.ladbrokescoral.oxygen.cms.api.archival.repository.SportCategoryArchivalRepository
import com.ladbrokescoral.oxygen.cms.api.entity.HomeInplaySport
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException
import com.ladbrokescoral.oxygen.cms.api.repository.HomeInplaySportRepository
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor
import com.ladbrokescoral.oxygen.cms.api.service.CompetitionService
import com.ladbrokescoral.oxygen.cms.api.service.SegmentService
import com.ladbrokescoral.oxygen.cms.api.service.SportCategoryService
import com.ladbrokescoral.oxygen.cms.api.service.SportModuleService
import com.ladbrokescoral.oxygen.cms.api.service.TierCategoriesCache
import com.ladbrokescoral.oxygen.cms.api.service.UserService
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabService
import com.ladbrokescoral.oxygen.cms.configuration.ImageConfig
import org.modelmapper.ModelMapper
import spock.lang.Specification

class SportCategoryControllerSpec extends Specification {

  SportCategoryService sportCategoryService
  SiteServeService siteServeService
  SportCategories controller
  SportTabService sportTabService
  ScheduledTaskExecutor scheduledTaskExecutorMock
  SportModuleService sportModuleService
  SportCategoryRepository sportCategoryRepository
  SportCategoryArchivalRepository sportCategoryArchivalRepository
  SegmentService segmentService
  ModelMapper modelMapper =new ModelMapper()
  HomeInplaySportRepository homeInplaySportRepository
  CompetitionService competitionService

  def setup() {
    String imageSize = "1x1"
    sportCategoryRepository = Mock(SportCategoryRepository)
    sportCategoryRepository.save(_ as SportCategory) >> new SportCategory()
    sportTabService = Mock()
    siteServeService = Mock(SiteServeService)
    scheduledTaskExecutorMock = Mock()
    sportModuleService = Mock()
    sportCategoryArchivalRepository=Mock()
    segmentService=Mock()
    homeInplaySportRepository=Mock()
    competitionService = Mock()
    sportCategoryService = new SportCategoryService(sportCategoryRepository,
        sportTabService, sportModuleService,
        null, null, null,
        siteServeService,
        scheduledTaskExecutorMock
        ,
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
    controller = new SportCategories(sportCategoryService, Mock(TierCategoriesCache),competitionService)

    UserService userServiceMock = Mock(UserService)
    userServiceMock.findOne(_ as String) >> Optional.empty()
    controller.setUserService(userServiceMock)
  }

  def "hasEvents field should be set before sportCategory is saved" () {
    given:
    SportCategory sportCategory = createSportCategory(16)
    sportCategoryRepository.findByBrandAndCategoryId(*_) >> []
    def  homeInplay =createHomeInplay("12121","mongo",16)
    homeInplaySportRepository.findByCategoryIdAndBrand(*_) >> homeInplay
    when:
    controller.create(sportCategory)

    then:
    1 * sportTabService.areThereEventsInCategoryBasedOnSportTabs(sportCategory) >> true
  }

  def "test cannot create new sport category with duplicate categoryId" () {
    given:
    def newSportCategory = createSportCategory(16)
    sportCategoryRepository.findByBrandAndCategoryId(newSportCategory.getBrand(), newSportCategory.getCategoryId()) >> [
      createSportCategory(UUID.randomUUID().toString(), "Test", 16)
    ]

    when:
    controller.create(newSportCategory)

    then:
    thrown ValidationException
  }

  def "test possibility to create new sport category with null categoryId" () {
    given:
    def newSportCategory = createSportCategory(null)
    def  homeInplay =createHomeInplay("12121","mongo",16)
    homeInplaySportRepository.findByCategoryIdAndBrand(*_) >> homeInplay

    when:
    controller.create(newSportCategory)

    then:
    0 * sportCategoryRepository.findByBrandAndCategoryId(newSportCategory.getBrand(), newSportCategory.getCategoryId())
    1 * sportCategoryRepository.save(newSportCategory) >> newSportCategory
  }

  def "test possibility to update sport category" () {
    given:
    def updatedCategory = createSportCategory("123", "C1", 16)
    def existingCategory = createSportCategory(updatedCategory.getId(), "C2-Mongo", 16)
    def  homeInplay =createHomeInplay("12121","mongo",16)
    homeInplaySportRepository.findByCategoryIdAndBrand(*_) >> homeInplay

    when:
    controller.update(updatedCategory.getId(), updatedCategory)
    then:
    1 * sportCategoryRepository.findById(updatedCategory.getId()) >> Optional.ofNullable(existingCategory)
    1 * sportCategoryRepository.findByBrandAndCategoryId(updatedCategory.getBrand(), updatedCategory.getCategoryId()) >> [existingCategory]
    1 * sportCategoryRepository.save(updatedCategory) >> updatedCategory
  }

  private static SportCategory createSportCategory(String id, String alt,  Integer categoryId) {
    SportCategory sport = new SportCategory()
    sport.setId(id)
    sport.setBrand("bma")
    sport.setCategoryId(categoryId)
    sport.setAlt(alt)
    sport.setTargetUri("test")
    sport.setSsCategoryCode(categoryId == null ? null : categoryId.toString())
    return sport
  }

  private static List<HomeInplaySport> createHomeInplay(String id,String name, Integer categoryId) {

    List<HomeInplaySport> sports=new ArrayList<>()
    HomeInplaySport sport = new HomeInplaySport()
    sport.setId(id)
    sport.setBrand("bma")
    sport.setCategoryId(String.valueOf(categoryId))
    sport.setSportName(name)
    sports.add(sport)
    return sports
  }
  private static SportCategory createSportCategory(Integer categoryId) {
    return createSportCategory(UUID.randomUUID().toString(), "Test Sport", categoryId)
  }
}
