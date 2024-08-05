package com.ladbrokescoral.oxygen.cms.api.service

import com.ladbrokescoral.oxygen.cms.api.entity.ExternalLink
import com.ladbrokescoral.oxygen.cms.api.entity.TargetWindow
import com.ladbrokescoral.oxygen.cms.api.exception.ElementAlreadyExistException
import com.ladbrokescoral.oxygen.cms.api.repository.ExternalLinkRepository
import spock.lang.Shared
import spock.lang.Specification

class ExternalLinkServiceSpec extends Specification {

  @Shared
  ExternalLinkService externalLinkService

  @Shared
  ExternalLinkRepository externalLinkRepository

  def setup() {
    externalLinkRepository = Mock(ExternalLinkRepository.class)
    externalLinkService = new ExternalLinkService(externalLinkRepository)
  }

  def "prepareModelBeforeSave when creating new existing element should throw exception"() {
    given: "new element with fields but without id"
    ExternalLink externalLink = ExternalLink.builder()
        .brand("bma")
        .url("http:url")
        .target(TargetWindow.NEW)
        .build()

    and: "repo returns the same element"
    ExternalLink externalLinkInDb = ExternalLink.builder().id("csjn8jsdcnsucnc").build()

    externalLinkRepository.findAllByUrlAndBrand("http:url", "bma") >> Collections.singletonList(externalLinkInDb)

    when:
    externalLinkService.prepareModelBeforeSave(externalLink)

    then: "Element already exist exception should be thrown"
    final ElementAlreadyExistException exception = thrown()
  }

  def "prepareModelBeforeSave when creating brand new element should not throw exception"() {
    given: "new element with fields but without id"
    ExternalLink externalLink = ExternalLink.builder()
        .brand("bma")
        .url("http:url")
        .target(TargetWindow.NEW)
        .build()

    and: "repo returns empty list"
    externalLinkRepository.findAllByUrlAndBrand("http:url", "bma") >> Collections.emptyList()

    when:
    externalLinkService.prepareModelBeforeSave(externalLink)

    then: "Element already exist exception should not be thrown"
    noExceptionThrown()
  }

  def "prepareModelBeforeSave when updating existing element should not throw exception"() {
    given: "new element with fields but without id"
    ExternalLink externalLink = ExternalLink.builder()
        .id("csjn8jsdcnsucnc")
        .brand("bma")
        .url("http:url")
        .target(TargetWindow.NEW)
        .build()

    and: "repo returns the same element"
    ExternalLink externalLinkInDb = ExternalLink.builder().id("csjn8jsdcnsucnc").build()

    externalLinkRepository.findAllByUrlAndBrand("http:url", "bma") >> Collections.singletonList(externalLinkInDb)

    when:
    externalLinkService.prepareModelBeforeSave(externalLink)

    then: "Element already exist exception should not be thrown"
    noExceptionThrown()
  }
}
