package com.ladbrokescoral.oxygen.cms.api.service.interceptors


import java.util.concurrent.ExecutorService

import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent

import com.ladbrokescoral.oxygen.cms.api.dto.InitialDataCFDto
import com.ladbrokescoral.oxygen.cms.api.dto.InitialDataDto
import com.ladbrokescoral.oxygen.cms.api.dto.SvgSpriteDto
import com.ladbrokescoral.oxygen.cms.api.entity.SvgImage
import com.ladbrokescoral.oxygen.cms.api.entity.SvgSprite
import com.ladbrokescoral.oxygen.cms.api.repository.SvgImageRepository
import com.ladbrokescoral.oxygen.cms.api.service.InitialDataService
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SvgImagePublicService
import com.ladbrokescoral.oxygen.cms.util.CustomExecutors

import spock.lang.Specification

class SvgImageAfterSaveListenerSpec extends Specification {

  SvgImagePublicService svgImagePublicService
  DeliveryNetworkService deliveryService
  InitialDataService initialDataService
  AfterSaveEvent<SvgImage> afterSaveEvent

  SvgImageAfterSaveListener listener

  void setup() {

    SvgImageRepository svgImageRepository = Mock(SvgImageRepository)
    svgImageRepository.findAllByBrandAndSprite(_ as String, _ as String) >> Collections.emptyList()
    svgImageRepository.findByBrand(_ as String) >> Collections.emptyList()
    svgImagePublicService = new SvgImagePublicService(svgImageRepository)
    deliveryService = Mock(DeliveryNetworkService)
    initialDataService = Mock(InitialDataService)
    initialDataService.fetchInitialData(*_) >> new InitialDataDto()
    initialDataService.fetchCFInitialData(*_) >> new InitialDataCFDto()
    afterSaveEvent = Mock()

    // executor stubing

    CustomExecutors customExecutors = Mock()
    ExecutorService executorService = Mock()

    customExecutors.getSingleThreadLastTaskExecutor(_ as String) >> executorService
    executorService.execute(_) >> {it[0].run()}

    listener = new SvgImageAfterSaveListener(svgImagePublicService, this.initialDataService, deliveryService)
    listener.customExecutors = customExecutors

  }

  def "on after save sprite svg"() {
    given:
    afterSaveEvent.getSource() >> createImage(SvgSprite.ADDITIONAL.getSpriteName())

    when:
    listener.onAfterSave(afterSaveEvent)

    then:
    5 * deliveryService.upload(
        'brand',
        'api/brand/svg-images/sprite',
        {
          [
            'featured',
            'additional',
            'initial',
            'timeline',
            'virtual'
          ].contains(it)},
        _ as SvgSpriteDto)
    3 * deliveryService.upload(
        'brand',
        'api/brand/initial-data',
        {
          [
            'mobile',
            'desktop',
            'tablet'
          ].contains(it)},
        _ as InitialDataDto)
  }

  private static SvgImage createImage(String spriteName) {
    def svg = new SvgImage()
    svg.setBrand("brand")
    svg.setSprite(spriteName)
    return svg
  }
}
