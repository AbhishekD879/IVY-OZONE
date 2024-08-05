package com.ladbrokescoral.oxygen.cms.api.service

import com.ladbrokescoral.oxygen.cms.api.entity.Secret
import com.ladbrokescoral.oxygen.cms.api.entity.SecretItem
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException
import com.ladbrokescoral.oxygen.cms.api.repository.SecretRepository
import com.ladbrokescoral.oxygen.cms.api.service.vault.SecretVaultService
import spock.lang.Specification

class SecretServiceSpec extends Specification {

  SecretService secretService
  SecretRepository secretRepository
  SecretVaultService vaultService

  def setup(){
    secretRepository = Mock()
    vaultService = Mock()
    secretService = new SecretService(secretRepository, vaultService, "md.hash", "md")
  }

  def "Prepare new Secret"() {
    given:
    Secret secret = createSecret(null, "uri", [
      new SecretItem("key1", "1"),
      new SecretItem("key2", "2")
    ])

    when:
    def prepared = secretService.prepareModelBeforeSave(secret)

    then:
    Objects.nonNull(prepared)
    Objects.nonNull(prepared.getId())
    prepared.getItems().stream()
        .allMatch({i -> ("key1" == i.getKey() && "1" != i.getValue()) || ("key2" == i.getKey() && "2" != i.getValue())})
    2 * vaultService.save(_, _)
  }

  def "Prepare existed Secret"() {
    given:
    Secret secret = createSecret("not-null", "uri",
        [
          new SecretItem("key1", "1"),
          new SecretItem("key2", "2")
        ])

    when:
    def prepared = secretService.prepareModelBeforeSave(secret)

    then:
    Objects.nonNull(prepared)
    prepared == secret
    0 * vaultService.save(_, _)
  }

  def "Prepare duplicate items Secret"() {
    given:
    Secret secret = createSecret("not-null", "uri",
        [
          new SecretItem("key1", "1"),
          new SecretItem("key2", "2"),
          new SecretItem("key2", "3")
        ])

    when:
    secretService.prepareModelBeforeSave(secret)

    then:
    def ex = thrown(ValidationException)
    ex.message == "Validation failed with reason: Unsupported duplicated key key2"
  }

  def "Update"() {
    given:
    Secret existing = createSecret("non-null", "uri",
        [
          new SecretItem("key1", "1"),
          new SecretItem("key2", "2")
        ])
    Secret updated = createSecret("non-null", "uri1",
        [
          new SecretItem("key2", "1"),
          new SecretItem("key3", "2"),
          new SecretItem("key4", "2")
        ])
    secretRepository.save(_ as Secret) >> {arg -> return arg[0]}

    when:
    def result = secretService.update(existing, updated)

    then:
    Objects.nonNull(result)
    result.getId() == existing.getId()
    result.getUri() == updated.getUri()
    result.getItems().size() == 3

    3 * vaultService.save(_, _)
    1 * vaultService.remove(_)
  }

  def "ReadDecoded"() {
    given:
    String id = "id"
    Secret secret = createSecret(id, "uri",
        [
          new SecretItem("key1", "1"),
          new SecretItem("key2", "2")
        ])

    when:
    def result = secretService.readDecoded(id)

    then:
    Objects.nonNull(result)
    result == secret
    1 * secretRepository.findById(id) >> Optional.of(secret)
    1 * vaultService.getValues(_ as List) >> Collections.emptyMap()
  }

  def "ReadDecoded Not Found"() {
    given:
    String id = "id"

    when:
    secretService.readDecoded(id)

    then:
    1 * secretRepository.findById(id) >> Optional.empty()
    0 * vaultService.getValues(_ as List)
    thrown(NotFoundException)
  }

  def "ReadActiveByBrandAndUri"() {
    given:
    String uri = "uri"
    Secret secret = createSecret("id", uri,
        [
          new SecretItem("key1", "1"),
          new SecretItem("key2", "2")
        ])

    when:
    def result = secretService.readActiveByBrandAndUri("brand", uri)

    then:
    Objects.nonNull(result)
    result.isPresent()
    result.get() == secret
    1 * secretRepository.findByBrandAndUriAndEnabledIsTrue(_ as String,_ as String) >> Optional.of(secret)
    1 * vaultService.getValues(_ as List) >> Collections.emptyMap()
  }

  def "BeforeDelete"() {
    given:
    String id = "id"
    Secret secret = createSecret(id, "uri",
        [
          new SecretItem("key1", "1"),
          new SecretItem("key2", "2")
        ])

    when:
    def result = secretService.beforeDelete(id)

    then:
    Objects.nonNull(result)
    result.isPresent()
    result.get() == secret
    1 * secretRepository.findById(_ as String) >> Optional.of(secret)
    2 * vaultService.remove(_ as String)
  }

  private static Secret createSecret(String id, String uri, List<SecretItem> items) {
    Secret secret = new Secret()
    secret.setBrand("brand")
    secret.setId(id)
    secret.setName(uri)
    secret.setUri(uri)
    secret.setItems(items)
    secret
  }
}
