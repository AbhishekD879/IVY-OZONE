package com.ladbrokescoral.oxygen.cms.api.service.public_api

import com.ladbrokescoral.oxygen.cms.api.TestUtil
import com.ladbrokescoral.oxygen.cms.api.dto.InplaySportCategoryDto
import com.ladbrokescoral.oxygen.cms.api.entity.Sport
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository
import com.ladbrokescoral.oxygen.cms.api.repository.SportRepository
import spock.lang.Specification

import java.util.stream.Collectors

class InplayDataPublicServiceSpec extends Specification {

  private static final BRAND = 'ladbrokes'
  SportCategoryRepository sportCategoryRepository
  SportRepository sportRepository

  InplayDataPublicService service
  VirtualSportPublicService virtualSportPublicService

  def setup() {
    sportCategoryRepository = Mock(SportCategoryRepository)
    sportRepository = Mock(SportRepository)
    virtualSportPublicService = Mock(VirtualSportPublicService)
    service = new InplayDataPublicService(sportCategoryRepository, sportRepository,virtualSportPublicService)
  }

  def "Check categories & sports merging for InplayDataDto"() {
    given:
    List<SportCategory> sportCategories = TestUtil
        .deserializeListWithJackson("service/public_api/ladbrokes_sportCategory.json", SportCategory.class)
    and: 'disable sportCategory 34 (tier 1)'
    sportCategories.stream().filter({ category -> category.getCategoryId() == 34 })
    .findFirst().ifPresent({ category -> category.setDisabled(true) })
    and: 'unset showInplay fot sportCategory 13 (tier 2)'
    sportCategories.stream().filter({ category -> category.getCategoryId() == 13 })
    .findFirst().ifPresent({ category -> category.setShowInPlay(false) })
    and:
    List<Sport> sports = TestUtil
        .deserializeListWithJackson("service/public_api/ladbrokes_sport.json", Sport.class)
    and: 'disable sport 9 (tier 2)'
    sports.stream().filter({ sport -> sport.getCategoryId() == 9 })
    .findFirst().ifPresent({ sport -> sport.setDisabled(true) })

    and:
    sportCategoryRepository.findAllByBrandOrderBySortOrderAsc(BRAND) >> sportCategories
    sportRepository.findAllByBrandOrderBySortOrderAsc(BRAND) >> sports

    when:
    def data = service.getInplayData(BRAND)
    then:
    data != null
    and: 'check active inplay sports availability:'
    List<Integer> activeInplaySportsCategoryId = data.getActiveSportCategories()
        .stream().map({ sport -> sport.getCategoryId() }).collect(Collectors.toList())
    activeInplaySportsCategoryId.contains(16)
    activeInplaySportsCategoryId.contains(32)
    !activeInplaySportsCategoryId.contains(34)
    !activeInplaySportsCategoryId.contains(13)
    activeInplaySportsCategoryId.contains(9)
    !activeInplaySportsCategoryId.contains(7)
    !activeInplaySportsCategoryId.contains(19)
    activeInplaySportsCategoryId.contains(6)

    and:
    Map<Integer, InplaySportCategoryDto> sportMap = data.getSportMap()
    sportMap.containsKey(13)
    sportMap.containsKey(34)
    //check if All Sports is inside
    sportMap.containsKey(0)
  }
}
