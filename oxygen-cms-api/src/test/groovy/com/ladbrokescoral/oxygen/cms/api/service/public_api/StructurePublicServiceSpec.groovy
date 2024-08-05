package com.ladbrokescoral.oxygen.cms.api.service.public_api

import com.ladbrokescoral.oxygen.cms.api.dto.StructureDto
import com.ladbrokescoral.oxygen.cms.api.exception.EmptyConfigurationStructureException
import com.ladbrokescoral.oxygen.cms.api.service.StructureService
import spock.lang.Specification

class StructurePublicServiceSpec extends Specification {

  StructureService structureService
  StructurePublicService structurePublicService
  String brand = "brand"

  void setup() {
    structureService = Mock()
    structurePublicService = new StructurePublicService(structureService)
  }

  def "Find"() {
    when:
    structurePublicService.find(brand)

    then:
    1* structureService.findStructureByBrand(brand) >> Optional.empty()
  }

  def "FindElement"() {
    given:
    def configName = "Config Name"

    when:
    structurePublicService.findElement(brand, configName)

    then:
    1* structureService.findByBrandAndConfigName(brand, configName)
  }

  def "GetInitialDataConfiguration with empty structure"() {
    when:
    structurePublicService.getInitialDataConfiguration(brand)

    then:
    1* structureService.findInitialDataStructure(brand) >> Optional.empty()
    def ex = thrown(EmptyConfigurationStructureException)
    ex.message == "Cannot find structure for brand "+ brand
  }

  def "GetInitialDataConfiguration"() {
    given:
    def structure = new StructureDto()
    structure.setBrand(brand)
    structure.setStructure(Collections.singletonMap("config1", Collections.emptyMap()))

    when:
    def initialStructure = structurePublicService.getInitialDataConfiguration(brand)

    then:
    1* structureService.findInitialDataStructure(brand) >> Optional.of(structure)
    initialStructure == structure.getStructure()
  }
}
