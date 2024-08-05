package com.ladbrokescoral.oxygen.cms.api.controller.private_api

import com.ladbrokescoral.oxygen.cms.api.TestUtil
import com.ladbrokescoral.oxygen.cms.api.entity.HomeInplaySport
import com.ladbrokescoral.oxygen.cms.api.entity.Homepage
import com.ladbrokescoral.oxygen.cms.api.entity.User
import com.ladbrokescoral.oxygen.cms.api.repository.HomepagesRepository
import com.ladbrokescoral.oxygen.cms.api.service.HomepageService
import com.ladbrokescoral.oxygen.cms.api.service.UserService
import spock.lang.Specification

class HomepageSpec extends Specification {
  def "Return item by id"() {
    given:
    HomepagesRepository repository = Mock()
    HomepageService crudService = new HomepageService(repository)
    Homepages homePages = new Homepages(crudService)
    Homepage homepage =
        TestUtil.deserializeWithJackson("service/homepage/inplayModule.json", Homepage.class);
    repository.findById("12345678") >> Optional.of(homepage)

    UserService userService = Mock()
    User user = new User()
    user.setId("54905d04a49acf605d645271")
    user.setEmail("lin@gmail.com")
    user.setPassword("123445566")
    userService.findOne("54905d04a49acf605d645271") >> Optional.of(user)
    homePages.setUserService(userService)

    when:
    Homepage result = homePages.read("12345678")

    then:
    result.getEnabled()
    result.getId() == "12345678"
    result.getHomeInplayConfig().getMaxEventCount() == 10
    List<HomeInplaySport> sports = result.getHomeInplayConfig().getHomeInplaySports()
    sports.get(0).getSportNumber() == 1
    sports.get(0).getEventCount() == 6
    sports.get(1).getSportNumber() == 2
    sports.get(1).getEventCount() == 2
    sports.get(2).getSportNumber() == 3
    sports.get(2).getEventCount() == 2
  }
}
