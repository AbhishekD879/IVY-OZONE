package com.ladbrokescoral.oxygen.cms.api.controller.private_api

import com.ladbrokescoral.oxygen.cms.api.TestUtil
import com.ladbrokescoral.oxygen.cms.api.dto.SportNameDto
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SportCategoryArchivalRepository
import com.ladbrokescoral.oxygen.cms.api.entity.HomeInplaySport
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier
import com.ladbrokescoral.oxygen.cms.api.entity.User
import com.ladbrokescoral.oxygen.cms.api.repository.HomeInplaySportRepository
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor
import com.ladbrokescoral.oxygen.cms.api.service.*
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabService
import com.ladbrokescoral.oxygen.cms.configuration.ImageConfig
import org.modelmapper.ModelMapper
import spock.lang.Specification

class SportCategoriesSpec extends Specification {
  def "Return items by id"() {
    given:
    CompetitionService competitionService = Mock()
    SportCategoryRepository repository = Mock()
    SiteServeService siteServeService = Mock()
    SportTabService sportTabService = Mock()
    ScheduledTaskExecutor scheduledTaskExecutorMock = Mock()
    SportModuleService sportModuleService = Mock()
    SportCategoryArchivalRepository sportCategoryArchivalRepository=Mock()
    SegmentService segmentService=Mock()
    HomeInplaySportRepository homeInplaySportRepository=Mock();
    SportCategory category =
        TestUtil.deserializeWithJackson("service/sport_category_service/55018df1044f8ee43ff7a4a8.json", SportCategory.class)
    repository.findById("55018df1044f8ee43ff7a4a8") >> Optional.of(category)

    ImageEntityService<SportCategory> imageEntityService = Mock()
    IconEntityService<SportCategory> iconEntityService = Mock()
    SvgEntityService<SportCategory> svgEntityService = Mock()

    ModelMapper modelMapper =new ModelMapper()
    String smallMenusPath = ""
    String mediumMenusPath = ""
    String largeMenusPath = ""
    String smallMenuSize = "100x100"
    String mediumMenuSize = "200x200"
    String largeMenuSize = "400x400"
    String smallIconsPat = ""
    String mediumIconsPath = ""
    String largeIconsPath = ""
    String smallIconSize = "10x10"
    String mediumIconSize = "20x20"
    String largeIconSize = "40x40"
    String svgMenuPath = ""
    SportCategoryService sportCategoryService = new SportCategoryService(repository,
        sportTabService, sportModuleService,
        imageEntityService,
        iconEntityService,
        svgEntityService,
        siteServeService,
        scheduledTaskExecutorMock,
        ImageConfig.ImagePath.builder()
        .svgMenuPath(svgMenuPath)
        .smallPath(smallMenusPath)
        .mediumPath(mediumMenusPath)
        .largePath(largeMenusPath)
        .smallSize(new ImageServiceImpl.Size(smallMenuSize))
        .mediumSize(new ImageServiceImpl.Size(mediumMenuSize))
        .largeSize(new ImageServiceImpl.Size(largeMenuSize))
        .build(),
        ImageConfig.ImagePath.builder()
        .smallPath(smallIconsPat)
        .mediumPath(mediumIconsPath)
        .largePath(largeIconsPath)
        .smallSize(new ImageServiceImpl.Size(smallIconSize))
        .mediumSize(new ImageServiceImpl.Size(mediumIconSize))
        .largeSize(new ImageServiceImpl.Size(largeIconSize))
        .build(),sportCategoryArchivalRepository,segmentService,new ModelMapper(),homeInplaySportRepository)

    SportCategories sportCategories = new SportCategories(sportCategoryService, Mock(TierCategoriesCache),competitionService)
    UserService userService = Mock()
    User user = new User()
    user.setId("54905d04a49acf605d645271")
    user.setEmail("lin@gmail.com")
    user.setPassword("123445566")
    userService.findOne("54905d04a49acf605d645271") >> Optional.of(user)
    sportCategories.setUserService(userService)
    when:
    SportCategory sportCategory = sportCategories.read("55018df1044f8ee43ff7a4a8")

    then:
    !sportCategory.isDisabled()
    sportCategory.isInplayEnabled()
  }



  def "Return SportName by brand"() {
    given:
    SportCategoryRepository repository = Mock()
    SiteServeService siteServeService = Mock()
    CompetitionService competitionService = Mock()
    SportTabService sportTabService = Mock()
    ScheduledTaskExecutor scheduledTaskExecutorMock = Mock()
    SportModuleService sportModuleService = Mock()
    SportCategoryArchivalRepository sportCategoryArchivalRepository=Mock()
    SegmentService segmentService=Mock()
    HomeInplaySportRepository homeInplaySportRepository=Mock();

    List<SportCategory> categories = createSportCategories()
    List<HomeInplaySport> InplaySports=createInplayCategories()
    repository.findByBrandAndCategoryIdNotNullAndIsActiveAndInTier("bma") >> categories
    homeInplaySportRepository.findByBrand("bma")>>InplaySports
    ImageEntityService<SportCategory> imageEntityService = Mock()
    IconEntityService<SportCategory> iconEntityService = Mock()
    SvgEntityService<SportCategory> svgEntityService = Mock()
    String smallMenusPath = ""
    String mediumMenusPath = ""
    String largeMenusPath = ""
    String smallMenuSize = "100x100"
    String mediumMenuSize = "200x200"
    String largeMenuSize = "400x400"
    String smallIconsPat = ""
    String mediumIconsPath = ""
    String largeIconsPath = ""
    String smallIconSize = "10x10"
    String mediumIconSize = "20x20"
    String largeIconSize = "40x40"
    String svgMenuPath = ""
    SportCategoryService sportCategoryService = new SportCategoryService(repository,
        sportTabService, sportModuleService,
        imageEntityService,
        iconEntityService,
        svgEntityService,
        siteServeService,
        scheduledTaskExecutorMock,
        ImageConfig.ImagePath.builder()
        .svgMenuPath(svgMenuPath)
        .smallPath(smallMenusPath)
        .mediumPath(mediumMenusPath)
        .largePath(largeMenusPath)
        .smallSize(new ImageServiceImpl.Size(smallMenuSize))
        .mediumSize(new ImageServiceImpl.Size(mediumMenuSize))
        .largeSize(new ImageServiceImpl.Size(largeMenuSize))
        .build(),
        ImageConfig.ImagePath.builder()
        .smallPath(smallIconsPat)
        .mediumPath(mediumIconsPath)
        .largePath(largeIconsPath)
        .smallSize(new ImageServiceImpl.Size(smallIconSize))
        .mediumSize(new ImageServiceImpl.Size(mediumIconSize))
        .largeSize(new ImageServiceImpl.Size(largeIconSize))
        .build(),sportCategoryArchivalRepository,segmentService,new ModelMapper(),homeInplaySportRepository)

    SportCategories sportCategories = new SportCategories(sportCategoryService, Mock(TierCategoriesCache),competitionService)
    UserService userService = Mock()
    User user = new User()
    user.setId("54905d04a49acf605d645271")
    user.setEmail("lin@gmail.com")
    user.setPassword("123445566")
    userService.findOne("54905d04a49acf605d645271") >> Optional.of(user)
    sportCategories.setUserService(userService)
    when:
    List<SportNameDto> sportCategory = sportCategories.readSportNameByBrand("bma")

    then:
    !sportCategory.isEmpty()
  }

  private List<SportCategory> createSportCategories() {
    List<SportCategory> categories = new ArrayList<>();

    categories.add(createSportCategory(16, "FootBall",SportTier.TIER_1));
    categories.add(createSportCategory(2, "cricket",SportTier.TIER_1));
    categories.add(createSportCategory(21, "horse race",SportTier.TIER_1));
    categories.add(createSportCategory(null, "horse race",SportTier.TIER_1));

    return categories;
  }


  private List<SportCategory> createInplayCategories() {
    List<HomeInplaySport> categories = new ArrayList<>();
    HomeInplaySport inplay=new HomeInplaySport()
    inplay.setBrand("bma")
    inplay.setSportName("test")
    inplay.setCategoryId("16")
    categories.add(inplay)

    HomeInplaySport inplay1=new HomeInplaySport()
    inplay.setBrand("bma")
    inplay.setSportName("FootBall")
    categories.add(inplay1)

    HomeInplaySport inplay2=new HomeInplaySport()
    inplay2.setBrand("bma")
    inplay2.setSportName("FootBall1")
    inplay2.setCategoryId("45")
    inplay2.setUniversalSegment(false)
    inplay2.setInclusionList(new ArrayList<>())
    categories.add(inplay2)

    HomeInplaySport inplay3=new HomeInplaySport()
    inplay3.setBrand("bma")
    inplay3.setSportName("FootBall2")
    inplay3.setCategoryId("47")
    inplay3.setUniversalSegment(true)
    inplay3.setInclusionList(Arrays.asList("s1"))
    categories.add(inplay3)

    return categories;
  }

  private SportCategory createSportCategory(Integer catId, String sportName,SportTier s) {

    SportCategory category = new SportCategory();
    category.setBrand("bma");
    category.setCategoryId(catId);
    category.setImageTitle(sportName);
    category.setTier(s);
    return category;
  }
}
