package com.ladbrokescoral.oxygen.cms.api.service

import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.egalacoral.spark.siteserver.model.Category
import com.ladbrokescoral.oxygen.cms.api.TestUtil
import com.ladbrokescoral.oxygen.cms.api.entity.Sport
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException
import com.ladbrokescoral.oxygen.cms.api.repository.SportRepository
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider
import spock.lang.Specification

class SportServiceSpec extends Specification {

  SiteServerApi siteServerApiMock = Mock(SiteServerApi)
  def sportService
  SiteServeApiProvider siteServeApiProvider = Mock(SiteServeApiProvider)

  def setup() {
    siteServeApiProvider.api("bma") >> siteServerApiMock
    SportsImageUploadComponent sportsImageUploadComponent = Mock(SportsImageUploadComponent)
    SportRepository repository = Mock(SportRepository)
    sportService = new SportService(repository, siteServeApiProvider, sportsImageUploadComponent)
  }

  def "save sport with OpenBet types from more than one category"() {
    given: "Sport with category 16 and types that belongs to category 16 and 5"
    Sport sport = new Sport()
    sport.setCategoryId(16)
    sport.setTypeIds("933,33")
    sport.setBrand("bma")

    and: "siteServe api returns two categories for 933,33 types"
    List<Category> categories =
        TestUtil.deserializeListWithJackson("service/sport_service/typesForTwoCategories.json", Category.class);
    siteServerApiMock.getClassToSubTypeForType(_, _) >> Optional.of(categories)
    when:
    sportService.save(sport)

    then:
    ValidationException exception = thrown()
    exception.getMessage() == "Validation failed with reason: Type ids: [933, 33] are from more than one category"
  }

  def "save sport with OpenBet types from different category"() {
    given: "Sport with category 16 and types that belongs to category 16 and 5"
    Sport sport = new Sport()
    sport.setCategoryId(16)
    sport.setTypeIds("6307,6309") //6307,6309 belongs to category 6 instead of 16
    sport.setBrand("bma")

    and: "siteServe api returns one category id = 6 for 6307,6309 types"
    List<Category> categories =
        TestUtil.deserializeListWithJackson("service/sport_service/typesForDiffCategory.json", Category.class);
    siteServerApiMock.getClassToSubTypeForType(_, _) >> Optional.of(categories)
    when:
    sportService.save(sport)

    then:
    ValidationException exception = thrown()
    exception.getMessage() == "Validation failed with reason: Type ids: [6307, 6309] are not from category with id=16"
  }

  def "save sport with 2 OpenBet types: one belongs to category 16, the second does not exist"() {
    given: "Sport with category 16 and types that belongs to category 16 and 5"
    Sport sport = new Sport()
    sport.setCategoryId(16)
    sport.setTypeIds("933,909090") //933  belongs to category 16,  909090 does not exist
    sport.setBrand("bma")

    and: "siteServe api returns one category id = 16"
    List<Category> categories =
        TestUtil.deserializeListWithJackson("service/sport_service/typesDoNotExist.json", Category.class);
    siteServerApiMock.getClassToSubTypeForType(_, _) >> Optional.of(categories)
    when:
    sportService.save(sport)

    then:
    ValidationException exception = thrown()
    exception.getMessage() == "Validation failed with reason: Type ids: [909090] do not exist"
  }

  def "save sport with 2 OpenBet invalid types"() {
    given: "Sport with category 16 and types that belongs to category 16 and 5"
    Sport sport = new Sport()
    sport.setCategoryId(16)
    sport.setTypeIds("909090,909091") //909090 and 909091 do not exist
    sport.setBrand("bma")

    and: "siteServe api returns no category"
    siteServerApiMock.getClassToSubTypeForType(_, _) >> Optional.of(Collections.emptyList())
    when:
    sportService.save(sport)

    then:
    ValidationException exception = thrown()
    exception.getMessage() == "Validation failed with reason: Type ids: [909090, 909091] do not exist"
  }

  def "save sport with 2 OpenBet valid types"() {
    given: "Sport with category 16 and types that belongs to category 16 and 5"
    Sport sport = new Sport()
    sport.setCategoryId(16)
    sport.setTypeIds("933,934") //valid types
    sport.setBrand("bma")

    and: "siteServe api returns category id = 16 with two types"
    List<Category> categories =
        TestUtil.deserializeListWithJackson("service/sport_service/typesForOneCategory.json", Category.class);
    siteServerApiMock.getClassToSubTypeForType(_, _) >> Optional.of(categories)
    when:
    sportService.save(sport)

    then: "No one exception should be thrown"
    notThrown(ValidationException.class)
  }
}
