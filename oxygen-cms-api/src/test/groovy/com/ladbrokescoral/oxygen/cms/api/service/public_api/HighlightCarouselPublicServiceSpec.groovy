package com.ladbrokescoral.oxygen.cms.api.service.public_api

import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference

import java.time.Instant

import com.ladbrokescoral.oxygen.cms.api.entity.HighlightCarousel
import com.ladbrokescoral.oxygen.cms.api.entity.segment.Segment
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants
import com.ladbrokescoral.oxygen.cms.api.repository.HighlightCarouselRepository
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentRepository

import spock.lang.Specification

class HighlightCarouselPublicServiceSpec extends Specification {

  HighlightCarouselRepository repository
  HighlightCarouselPublicService service
  SegmentRepository segmentRepository

  def setup() {
    repository = Mock(HighlightCarouselRepository)
    segmentRepository = Mock(SegmentRepository)
    service = new HighlightCarouselPublicService(repository,segmentRepository)
  }

  def "findActiveByBrand returns dto from partly initialized entity"() {
    given:
    def brand = 'connect'

    def entity = new HighlightCarousel()
    entity.sportId = 0

    repository.findByBrandAndDisplayFromIsBeforeAndDisplayToIsAfterAndDisabledIsFalseOrderBySortOrderAsc(brand, _, _) >> [entity]



    def segments = Segment.builder().segmentName(SegmentConstants.UNIVERSAL).brand("connect").build();

    segmentRepository.findByBrand("connect") >> [segments]


    when:
    def list = service.findActiveByBrand(brand)

    then:
    list.size() == 1

    def dto = list.get 0
    dto.id == null
    dto.sportId == entity.sportId
    dto.title == null
    dto.displayOrder == null
    dto.displayFrom == null
    dto.displayTo == null
    dto.svg == null
    dto.limit == null
    dto.inPlay
    dto.typeId == null
    dto.events == null
  }

  def "findActiveByBrand returns dto from empty entity"() {
    given:
    def brand = 'retail'

    def entity = new HighlightCarousel()
    entity.id = ''
    entity.sportId = 0
    entity.title = ''
    entity.sortOrder = 0.0
    entity.displayTo = Instant.MIN
    entity.displayFrom = Instant.MAX
    entity.svg = ''
    entity.limit = 0
    entity.inPlay = false
    entity.typeId = 0
    entity.events = []

    repository.findByBrandAndDisplayFromIsBeforeAndDisplayToIsAfterAndDisabledIsFalseOrderBySortOrderAsc(brand, _, _) >> [entity]

    def segments = Segment.builder().segmentName(SegmentConstants.UNIVERSAL).brand("retail").build();

    segmentRepository.findByBrand("retail") >> [segments]

    when:
    def list = service.findActiveByBrand(brand)

    then:
    list.size() == 1

    def dto = list.get 0
    dto.id == entity.id
    dto.sportId == entity.sportId
    dto.title == entity.title
    dto.displayOrder == entity.sortOrder
    dto.displayFrom == entity.displayFrom
    dto.displayTo == entity.displayTo
    dto.svg == entity.svg
    dto.limit == entity.limit
    dto.inPlay == entity.inPlay
    dto.typeId == entity.typeId
    dto.events == entity.events
  }

  def "findActiveByBrand"() {
    given:
    def brand = 'bma'
    def firstGroupSportId = 99
    def secondGroupSportId = 200

    def firstEntity = new HighlightCarousel()
    firstEntity.id = 'ID1'
    firstEntity.sportId = firstGroupSportId
    firstEntity.title = 'first title'
    firstEntity.sortOrder = 4.0
    firstEntity.displayTo = Instant.now()
    firstEntity.displayFrom = Instant.now()
    firstEntity.svg = '<svg/>'
    firstEntity.limit = 5
    firstEntity.inPlay = true
    firstEntity.typeId = 10
    firstEntity.events = ['event1', 'event2']

    def secondEntity = new HighlightCarousel()
    secondEntity.id = 'ID2'
    secondEntity.sportId = firstGroupSportId

    def thirdEntity = new HighlightCarousel()
    thirdEntity.id = 'ID3'
    thirdEntity.sportId = firstGroupSportId

    def forthEntity = new HighlightCarousel()
    forthEntity.id = 'ID4'
    forthEntity.sportId = secondGroupSportId

    repository.findByBrandAndDisplayFromIsBeforeAndDisplayToIsAfterAndDisabledIsFalseOrderBySortOrderAsc(brand, _, _) >> [
      firstEntity,
      secondEntity,
      thirdEntity,
      forthEntity
    ]


    def segments = Segment.builder().segmentName(SegmentConstants.UNIVERSAL).brand("bma").build();

    segmentRepository.findByBrand("bma") >> [segments]

    when:
    def list = service.findActiveByBrand(brand)

    then:
    list.size() == 4

    def firstDto = list.get 0
    firstDto.id == firstEntity.id
    firstDto.sportId == firstEntity.sportId
    firstDto.title == firstEntity.title
    firstDto.displayOrder == firstEntity.sortOrder
    firstDto.displayFrom == firstEntity.displayFrom
    firstDto.displayTo == firstEntity.displayTo
    firstDto.svg == firstEntity.svg
    firstDto.limit == firstEntity.limit
    firstDto.inPlay == firstEntity.inPlay
    firstDto.typeId == firstEntity.typeId
    firstDto.events == firstEntity.events

    def secondDto = list.get 1
    secondDto.id == secondEntity.id
    secondDto.sportId == secondEntity.sportId

    // Third entity is skipped as the carousel limit is set to 2 items per page (sport group)

    def forthDto = list.get 2
    forthDto.id == thirdEntity.id
    forthDto.sportId == thirdEntity.sportId
  }

  def "findActiveByBrandForNonUniversal"() {
    given:
    def brand = 'bma'
    def firstGroupSportId = 99
    def secondGroupSportId = 200

    def firstEntity = new HighlightCarousel()
    firstEntity.id = 'ID1'
    firstEntity.sportId = firstGroupSportId
    firstEntity.title = 'first title'
    firstEntity.sortOrder = 4.0
    firstEntity.displayTo = Instant.now()
    firstEntity.displayFrom = Instant.now()
    firstEntity.svg = '<svg/>'
    firstEntity.limit = 5
    firstEntity.inPlay = true
    firstEntity.typeId = 10
    firstEntity.events = ['event1', 'event2']

    def secondEntity = new HighlightCarousel()
    secondEntity.id = 'ID2'
    secondEntity.sportId = firstGroupSportId

    def thirdEntity = new HighlightCarousel()
    thirdEntity.id = 'ID3'
    thirdEntity.sportId = firstGroupSportId
    thirdEntity.universalSegment = false
    thirdEntity.segmentReferences = [
      SegmentReference.builder().segmentName("segment1").pageRefId("1").build()
    ]

    def forthEntity = new HighlightCarousel()
    forthEntity.id = 'ID4'
    forthEntity.sportId = secondGroupSportId
    forthEntity.universalSegment = true
    forthEntity.exclusionList = ["segment1"]

    repository.findByBrandAndDisplayFromIsBeforeAndDisplayToIsAfterAndDisabledIsFalseOrderBySortOrderAsc(brand, _, _) >> [
      firstEntity,
      secondEntity,
      thirdEntity,
      forthEntity
    ]


    def segments = Segment.builder().segmentName("segment1").brand("bma").build();
    def segment2 = Segment.builder().segmentName("segment2").brand("bma").build();

    segmentRepository.findByBrand("bma") >> [segments, segment2]

    when:
    def list = service.findActiveByBrand(brand)

    then:
    list.size() == 4

    def firstDto = list.get 0
    firstDto.id == firstEntity.id
    firstDto.sportId == firstEntity.sportId
    firstDto.title == firstEntity.title
    firstDto.displayOrder == firstEntity.sortOrder
    firstDto.displayFrom == firstEntity.displayFrom
    firstDto.displayTo == firstEntity.displayTo
    firstDto.svg == firstEntity.svg
    firstDto.limit == firstEntity.limit
    firstDto.inPlay == firstEntity.inPlay
    firstDto.typeId == firstEntity.typeId
    firstDto.events == firstEntity.events

    def secondDto = list.get 1
    secondDto.id == secondEntity.id
    secondDto.sportId == secondEntity.sportId

    // Third entity is skipped as the carousel limit is set to 2 items per page (sport group)

    def forthDto = list.get 2
    forthDto.id == thirdEntity.id
    forthDto.sportId == thirdEntity.sportId
  }
}
