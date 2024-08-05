package com.ladbrokescoral.oxygen.cms.api.service.public_api

import com.ladbrokescoral.oxygen.cms.api.entity.Feature
import com.ladbrokescoral.oxygen.cms.api.entity.Filename
import com.ladbrokescoral.oxygen.cms.api.repository.FeatureExtendedRepository
import com.ladbrokescoral.oxygen.cms.api.service.FeatureService
import com.ladbrokescoral.oxygen.cms.api.service.StructureService

import java.time.Instant
import java.time.LocalDateTime
import java.time.Month
import java.time.ZoneOffset

import spock.lang.Specification

class FeaturePublicServiceSpec extends Specification {

  final FEATURES = 'Features'
  final EXPANDED_AMOUNT = 'expandedAmount'

  FeatureExtendedRepository featureRepository
  StructureService structureService
  FeaturePublicService service

  def setup() {
    featureRepository = Mock(FeatureExtendedRepository)
    def featureService = new FeatureService(null, featureRepository, null, null, null, "24x24")
    structureService = Mock(StructureService)
    service = new FeaturePublicService(featureService, structureService)
  }

  def "findContainerByBrand returns dto from partly initialized entities"() {
    given:
    def brand = 'rcomb'

    def featureEntity = new Feature()
    featureEntity.showToCustomer = ''

    featureRepository.findFeatures(brand) >> [featureEntity]
    structureService
        .findByBrandAndConfigName(brand, FEATURES) >> Optional.empty()

    when:
    def containerDto = service.findContainerByBrand(brand)

    then:
    containerDto != null
    containerDto.expandedAmount == 2
    containerDto.features.size() == 1

    def featureDto = containerDto.features.get 0
    featureDto.id == null
    featureDto.title == null
    featureDto.shortDescription == null
    featureDto.description == null
    featureDto.validityPeriodStart == null
    featureDto.validityPeriodEnd == null
    featureDto.uriMedium == ''
    featureDto.widthMedium == null
    featureDto.heightMedium == null
    featureDto.disabled == null
    featureDto.showToCustomer.size() == 1
    featureDto.showToCustomer.get(0) == featureEntity.showToCustomer
    featureDto.filename == null
  }

  def "findContainerByBrand returns dto from empty entity"() {
    given:
    def brand = 'ladbrokes'

    def featureEntity = new Feature()
    featureEntity.id = ''
    featureEntity.title = ''
    featureEntity.shortDescription = ''
    featureEntity.description = ''
    featureEntity.validityPeriodStart = Instant.EPOCH
    featureEntity.validityPeriodEnd = Instant.EPOCH
    featureEntity.uriMedium = ''
    featureEntity.widthMedium = 0
    featureEntity.heightMedium = 0
    featureEntity.disabled = false
    featureEntity.showToCustomer = ''
    featureEntity.filename = new Filename()

    def featuresMap = new HashMap<String, Object>()
    featuresMap[EXPANDED_AMOUNT] = 0

    featureRepository.findFeatures(brand) >> [featureEntity]
    structureService
        .findByBrandAndConfigName(brand, FEATURES) >> Optional.of(featuresMap)

    when:
    def containerDto = service.findContainerByBrand(brand)

    then:
    containerDto != null
    containerDto.expandedAmount == featuresMap[EXPANDED_AMOUNT]
    containerDto.features.size() == 1

    def featureDto = containerDto.features.get 0
    featureDto.id == featureEntity.id
    featureDto.title == featureEntity.title
    featureDto.shortDescription == featureEntity.shortDescription
    featureDto.description == featureEntity.description
    featureDto.validityPeriodStart == '1970-01-01T00:00:00.000Z'
    featureDto.validityPeriodEnd == '1970-01-01T00:00:00.000Z'
    featureDto.uriMedium == featureEntity.uriMedium
    featureDto.widthMedium == featureEntity.widthMedium
    featureDto.heightMedium == featureEntity.heightMedium
    featureDto.disabled == featureEntity.disabled
    featureDto.showToCustomer.size() == 1
    featureDto.showToCustomer.get(0) == featureEntity.showToCustomer
    featureDto.filename == null
  }

  def "findContainerByBrand"() {
    given:
    def brand = 'connect'

    def firstFeatureEntity = new Feature()
    firstFeatureEntity.id = 'ID'
    firstFeatureEntity.title = 'title'
    firstFeatureEntity.shortDescription = 'short description'
    firstFeatureEntity.description = 'description'
    firstFeatureEntity.validityPeriodStart = LocalDateTime.of(2018, Month.DECEMBER, 31, 23, 59, 59).toInstant(ZoneOffset.UTC)
    firstFeatureEntity.validityPeriodEnd = LocalDateTime.of(2019, Month.JANUARY, 1, 0, 0, 0).toInstant(ZoneOffset.UTC)
    firstFeatureEntity.uriMedium = '/medium'
    firstFeatureEntity.widthMedium = 20
    firstFeatureEntity.heightMedium = 30
    firstFeatureEntity.disabled = true
    firstFeatureEntity.showToCustomer = 'both'
    firstFeatureEntity.filename = new Filename()
    firstFeatureEntity.filename.filename = 'test.txt'

    def secondFeatureEntity = new Feature()
    secondFeatureEntity.uriMedium = 'public/uri-medium'
    secondFeatureEntity.showToCustomer = 'all'

    def featuresMap = new HashMap<String, Object>()
    featuresMap[EXPANDED_AMOUNT] = 5

    featureRepository.findFeatures(brand) >> [
      firstFeatureEntity,
      secondFeatureEntity
    ]
    structureService
        .findByBrandAndConfigName(brand, FEATURES) >> Optional.of(featuresMap)

    when:
    def containerDto = service.findContainerByBrand(brand)

    then:
    containerDto != null
    containerDto.expandedAmount == featuresMap[EXPANDED_AMOUNT]
    containerDto.features.size() == 2

    def firstFeatureDto = containerDto.features.get 0
    firstFeatureDto.id == firstFeatureEntity.id
    firstFeatureDto.title == firstFeatureEntity.title
    firstFeatureDto.shortDescription == firstFeatureEntity.shortDescription
    firstFeatureDto.description == firstFeatureEntity.description
    firstFeatureDto.validityPeriodStart == '2018-12-31T23:59:59.000Z'
    firstFeatureDto.validityPeriodEnd == '2019-01-01T00:00:00.000Z'
    firstFeatureDto.uriMedium == firstFeatureEntity.uriMedium
    firstFeatureDto.widthMedium == firstFeatureEntity.widthMedium
    firstFeatureDto.heightMedium == firstFeatureEntity.heightMedium
    firstFeatureDto.disabled == firstFeatureEntity.disabled
    firstFeatureDto.showToCustomer.size() == 2
    firstFeatureDto.showToCustomer == ['logged-in', 'logged-out']
    firstFeatureDto.filename == firstFeatureEntity.filename.filename

    def secondFeatureDto = containerDto.features.get 1
    secondFeatureDto.uriMedium == '/uri-medium'
  }
}
