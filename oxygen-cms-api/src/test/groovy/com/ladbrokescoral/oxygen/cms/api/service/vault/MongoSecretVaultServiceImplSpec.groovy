package com.ladbrokescoral.oxygen.cms.api.service.vault

import com.ladbrokescoral.oxygen.cms.api.entity.SecretVault
import com.ladbrokescoral.oxygen.cms.api.repository.SecretVaultRepository
import spock.lang.Specification

class MongoSecretVaultServiceImplSpec extends Specification {

  SecretVaultService vaultService
  SecretVaultRepository vaultRepository

  def setup() {
    vaultRepository = Mock(SecretVaultRepository)
    vaultService = new MongoSecretVaultServiceImpl(vaultRepository)
  }

  def "Save"() {
    when:
    vaultService.save("key", "value")

    then:
    1 * vaultRepository.save(_)
  }

  def "Save Failed"() {
    given:
    vaultRepository.save(_ as SecretVault) >> { args -> throw new RuntimeException("any")}

    when:
    vaultService.save("key", "value")

    then:
    thrown VaultException
  }

  def "GetValue exists"() {
    given:
    def secretKey = "key"
    def vault = new SecretVault()
    vault.setKey(secretKey)
    vault.setValue("val")

    when:
    def result = vaultService.getValue(secretKey)

    then:
    1 * vaultRepository.findById(secretKey) >> Optional.of(vault)
    result == vault.getValue()
  }

  def "GetValue not present"() {
    given:
    def secretKey = "key"

    when:
    def result = vaultService.getValue(secretKey)

    then:
    1 * vaultRepository.findById(secretKey) >> Optional.empty()
    result == null
  }

  def "GetValues"() {
    given:
    def secretKey = "key"
    def secretValue = "val"
    def vault = new SecretVault()
    vault.setKey(secretKey)
    vault.setValue(secretValue)

    when:
    def result = vaultService.getValues([secretKey, "key2", "key3"])

    then:
    1 * vaultRepository.findAllById(_ as List) >> [vault]
    result.size() == 1
    result[secretKey] == secretValue
  }

  def "GetValues empty"() {
    when:
    def result = vaultService.getValues([])

    then:
    0 * vaultRepository.findAll(_ as List)
    result.isEmpty()
  }

  def "Remove"() {
    given:
    String secretKey = "key"

    when:
    vaultService.remove(secretKey)

    then:
    1 * vaultRepository.deleteById(secretKey)
  }
}
