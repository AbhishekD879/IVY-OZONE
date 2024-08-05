package com.ladbrokescoral.oxygen.cms.api.service

import com.google.common.collect.ImmutableMap
import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfigProperty
import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfiguration
import com.ladbrokescoral.oxygen.cms.api.repository.SystemConfigurationRepository
import spock.lang.Specification

import static com.ladbrokescoral.oxygen.cms.api.entity.SystemConfigPropertyType.*

class ConfigsServiceSpec extends Specification {

  SystemConfigurationRepository configurationRepository
  ConfigsService configsService

  void setup() {
    configurationRepository = Mock()
    configsService = new ConfigsService(configurationRepository)
  }

  def "FindElementByBrandAndName"() {
    given:
    def brand = "brand1"
    def configName = "Config1"

    when:
    configsService.findElementByBrandAndName(brand, configName)

    then:
    1* configurationRepository.findOneByBrandAndName(brand, configName)
  }

  def "DeleteAllByBrand"() {
    given:
    def brand = "brand1"

    when:
    configsService.deleteAllByBrand(brand)

    then:
    1* configurationRepository.deleteAllByBrand(brand)
  }

  def "PrepareModelBeforeSave with empty properties"() {
    given:
    def config = new SystemConfiguration()
    config.setProperties(Collections.emptyList())

    when:
    config = configsService.prepareModelBeforeSave(config)

    then:
    config.getProperties().isEmpty()
  }

  def "PrepareModelBeforeSave with not default structure"() {
    given:
    def config = new SystemConfiguration()
    def configName = "name"
    def configDefaultValue = "default"
    def structureValue = "structure"
    config.setProperties(Collections.singletonList(createConfigProperty(configName, INPUT.getName(), configDefaultValue, structureValue)))

    when:
    config = configsService.prepareModelBeforeSave(config)

    then:
    !config.getProperties().isEmpty()
    config.getProperty(configName).orElseThrow(IllegalArgumentException.&new).getStructureValue() == structureValue
    config.getProperty(configName).orElseThrow(IllegalArgumentException.&new).getStructureValueOrDefault() == structureValue
  }

  def "PrepareModelBeforeSave with null structure"() {
    given:
    def config = new SystemConfiguration()
    def configName = "name"
    def configDefaultValue = "default"
    config.setProperties(Collections.singletonList(createConfigProperty(configName, INPUT.getName(), configDefaultValue, null)))

    when:
    config = configsService.prepareModelBeforeSave(config)

    then:
    !config.getProperties().isEmpty()
    config.getProperty(configName).orElseThrow(IllegalArgumentException.&new).getStructureValue() == configDefaultValue
    config.getProperty(configName).orElseThrow(IllegalArgumentException.&new).getStructureValueOrDefault() == configDefaultValue
  }

  def "PrepareModelBeforeSave with select property type"() {
    given:
    def config = new SystemConfiguration()
    def configName = "name"
    def configDefaultValue = [2, 3, 4, 5, 1]
    config.setProperties(Collections.singletonList(createConfigProperty(configName, SELECT.getName(), configDefaultValue, null)))

    when:
    config = configsService.prepareModelBeforeSave(config)

    then:
    !config.getProperties().isEmpty()
    config.getProperty(configName).orElseThrow(IllegalArgumentException.&new).getStructureValue() == configDefaultValue[0]
    config.getProperty(configName).orElseThrow(IllegalArgumentException.&new).getStructureValueOrDefault() == configDefaultValue[0]
  }

  def "PrepareModelBeforeSave with multiselect property type"() {
    given:
    def config = new SystemConfiguration()
    def configName = "name"
    def configDefaultValue = [2, 3, 4, 5, 1]
    config.setProperties(Collections.singletonList(createConfigProperty(configName, MULTISELECT.getName(), configDefaultValue, null)))

    when:
    config = configsService.prepareModelBeforeSave(config)

    then:
    !config.getProperties().isEmpty()
    def readyConfig = config.getProperty(configName).orElseThrow(IllegalArgumentException.&new)
    List.class.isInstance(readyConfig.getStructureValue())
    (readyConfig.getStructureValue() as List).size() == 1
    (readyConfig.getStructureValue() as List)[0] == configDefaultValue[0]
    readyConfig.getStructureValueOrDefault() == readyConfig.getStructureValue()
  }

  def "PrepareModelBeforeSave with daterange property type"() {
    given:
    def config = new SystemConfiguration()
    def configName = "name"
    config.setProperties(Collections.singletonList(createConfigProperty(configName, DATERANGE.getName(), "any", null)))

    when:
    config = configsService.prepareModelBeforeSave(config)

    then:
    !config.getProperties().isEmpty()
    def readyConfig = config.getProperty(configName).orElseThrow(IllegalArgumentException.&new)
    Map.class.isInstance(readyConfig.getStructureValue())
    (readyConfig.getStructureValue() as Map).size() == 2
    (readyConfig.getStructureValue() as Map).containsKey("from")
    (readyConfig.getStructureValue() as Map).containsKey("to")
  }

  def "Update with old structure preserved"() {
    given:
    configurationRepository.save(_ as SystemConfiguration) >> { args -> args[0] }

    def propertyName = "name"
    def existingConfig = new SystemConfiguration()
    existingConfig.setProperties(Collections.singletonList(createConfigProperty(propertyName, DATERANGE.getName(), "any", ImmutableMap.of("from", "2020-01-01", "to", "2021-12-31"))))

    def newConfig = new SystemConfiguration()
    newConfig.setProperties(Collections.singletonList(createConfigProperty(propertyName, DATERANGE.getName(), "any", null)))

    when:
    def updatedConfig = configsService.update(existingConfig, newConfig)

    then:
    updatedConfig != null
    updatedConfig.getProperty(propertyName).orElseThrow(IllegalArgumentException.&new).getStructureValue() == existingConfig.getProperty(propertyName).orElseThrow(IllegalArgumentException.&new).getStructureValue()
  }

  def "Update with config selection list changed structure preserved"() {
    given:
    configurationRepository.save(_ as SystemConfiguration) >> { args -> args[0] }
    def propertyName = "name"

    def existingConfig = new SystemConfiguration()
    existingConfig.setProperties(Collections.singletonList(createConfigProperty(propertyName, SELECT.getName(), [1, 2, 3, 4], 4)))

    def newConfig = new SystemConfiguration()
    newConfig.setProperties(Collections.singletonList(createConfigProperty(propertyName, SELECT.getName(), [7, 2, 3, 4, 8], null)))

    when:
    def updatedConfig = configsService.update(existingConfig, newConfig)

    then:
    updatedConfig != null
    updatedConfig.getProperty(propertyName).orElseThrow(IllegalArgumentException.&new).getStructureValue() == existingConfig.getProperty(propertyName).orElseThrow(IllegalArgumentException.&new).getStructureValue()
  }


  def "Update with config selection list changed structure reset"() {
    given:
    configurationRepository.save(_ as SystemConfiguration) >> { args -> args[0] }
    def propertyName = "name"

    def existingConfig = new SystemConfiguration()
    existingConfig.setProperties(Collections.singletonList(createConfigProperty(propertyName, SELECT.getName(), [1, 2, 3, 4], 4)))

    def newConfig = new SystemConfiguration()
    newConfig.setProperties(Collections.singletonList(createConfigProperty(propertyName, SELECT.getName(), [7, 2, 3, 5, 8], null)))

    when:
    def updatedConfig = configsService.update(existingConfig, newConfig)

    then:
    updatedConfig != null
    updatedConfig.getProperty(propertyName).orElseThrow(IllegalArgumentException.&new).getStructureValue() == (newConfig.getProperty(propertyName).orElseThrow(IllegalArgumentException.&new).getValue() as List)[0]
  }

  def "Update with config multiselect list changed structure preserved"() {
    given:
    configurationRepository.save(_ as SystemConfiguration) >> { args -> args[0] }
    def propertyName = "name"

    def existingConfig = new SystemConfiguration()
    existingConfig.setProperties(Collections.singletonList(createConfigProperty(propertyName, MULTISELECT.getName(), [1, 2, 3, 4], [1, 4])))

    def newConfig = new SystemConfiguration()
    newConfig.setProperties(Collections.singletonList(createConfigProperty(propertyName, MULTISELECT.getName(), [7, 2, 3, 5, 4], null)))

    when:
    def updatedConfig = configsService.update(existingConfig, newConfig)

    then:
    updatedConfig != null
    updatedConfig.getProperty(propertyName).orElseThrow(IllegalArgumentException.&new).getStructureValue() == [4]
  }

  def "Update with config multiselect list changed structure reset"() {
    given:
    configurationRepository.save(_ as SystemConfiguration) >> { args -> args[0] }
    def propertyName = "name"

    def existingConfig = new SystemConfiguration()
    existingConfig.setProperties(Collections.singletonList(createConfigProperty(propertyName, MULTISELECT.getName(), [1, 2, 3, 4], [1, 4])))

    def newConfig = new SystemConfiguration()
    newConfig.setProperties(Collections.singletonList(createConfigProperty(propertyName, MULTISELECT.getName(), [7, 2, 3, 5, 8], null)))

    when:
    def updatedConfig = configsService.update(existingConfig, newConfig)

    then:
    updatedConfig != null
    updatedConfig.getProperty(propertyName).orElseThrow(IllegalArgumentException.&new).getStructureValue() == [7]
  }

  private static SystemConfigProperty createConfigProperty(String name, String type, Object defaultValue, Object structureValue) {
    def property = new SystemConfigProperty()
    property.setName(name)
    property.setType(type)
    property.setValue(defaultValue)
    property.setStructureValue(structureValue)
    property
  }
}
