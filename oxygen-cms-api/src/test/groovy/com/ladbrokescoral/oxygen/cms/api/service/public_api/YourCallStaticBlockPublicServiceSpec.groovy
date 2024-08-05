package com.ladbrokescoral.oxygen.cms.api.service.public_api

import com.ladbrokescoral.oxygen.cms.api.entity.YourCallStaticBlock
import com.ladbrokescoral.oxygen.cms.api.repository.YourCallStaticBlockRepository
import com.ladbrokescoral.oxygen.cms.api.service.YourCallStaticBlockService
import spock.lang.Specification

class YourCallStaticBlockPublicServiceSpec extends Specification {

  YourCallStaticBlockRepository repository
  YourCallStaticBlockPublicService service

  def setup() {
    repository = Mock(YourCallStaticBlockRepository)
    def ycStaticBlockService = new YourCallStaticBlockService(repository)
    service = new YourCallStaticBlockPublicService(ycStaticBlockService)
  }

  def "test dto mapping"() {
    given:
    def brand = 'bma'
    def entity = new YourCallStaticBlock()
    entity.setBrand(brand)
    entity.setEnabled(Boolean.TRUE)
    entity.setHtmlMarkup('<html>Hello<html>')
    entity.setTitle('hello-5a')
    repository.findAllByBrandAndEnabledAndFiveASide(brand, Boolean.TRUE, Boolean.TRUE) >> [entity]

    when:
    def list = service.findByBrandAnd5A(brand)

    then:
    list.size() == 1
    def dto = list.get 0
    dto.title == 'hello-5a'
    dto.htmlMarkup == '<html>Hello<html>'

    and: 'check if disabled by default'
    entity.fiveASide == Boolean.FALSE
  }
}
