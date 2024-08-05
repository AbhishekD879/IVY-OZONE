package com.ladbrokescoral.cashout.repository

import com.ladbrokescoral.cashout.EmbededRedis
import com.ladbrokescoral.cashout.config.RedisConfig
import com.ladbrokescoral.cashout.model.context.SelectionPrice
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.autoconfigure.cache.CacheAutoConfiguration
import org.springframework.boot.test.autoconfigure.data.redis.DataRedisTest
import org.springframework.context.annotation.Import
import org.springframework.test.annotation.DirtiesContext
import org.springframework.test.context.ActiveProfiles
import spock.lang.Specification

import java.time.Duration

@Import([RedisConfig, EmbededRedis, SelectionPriceRepository])
@DataRedisTest(excludeAutoConfiguration = [CacheAutoConfiguration])
@ActiveProfiles("UNIT")
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
class SelectionPriceRepositoryTest extends Specification {

  @Autowired
  SelectionPriceRepository selectionPriceRepository
  private Duration redisOperationTimeout = Duration.ofSeconds(2L)

  def "Test save SelectionPrice at Redis"() {
    given:
    SelectionPrice selectionPrice = SelectionPrice.builder()
        .outcomeId("1111")
        .priceDen("1")
        .priceNum("2")
        .build()

    when:
    def isSaved = selectionPriceRepository.save("testKey1", selectionPrice).block(redisOperationTimeout)

    then:
    isSaved
  }

  def "Test get SelectionPrice at Redis"() {
    given:
    SelectionPrice selectionPrice = SelectionPrice.builder()
        .outcomeId("1112")
        .priceDen("1")
        .priceNum("2")
        .build()
    selectionPriceRepository.save("testKey2", selectionPrice).block(redisOperationTimeout)

    when:
    SelectionPrice resultPrice = selectionPriceRepository.get("testKey2").block(redisOperationTimeout)
    then:
    resultPrice == selectionPrice
  }

  def "Test multi get SelectionPrice at Redis"() {
    given:
    SelectionPrice selectionPrice1 = SelectionPrice.builder()
        .outcomeId("1113")
        .priceDen("1")
        .priceNum("2")
        .build()
    SelectionPrice selectionPrice2 = SelectionPrice.builder()
        .outcomeId("1114")
        .priceDen("1")
        .priceNum("2")
        .build()
    selectionPriceRepository.save("testKey3", selectionPrice1).block(redisOperationTimeout)
    selectionPriceRepository.save("testKey4", selectionPrice2).block(redisOperationTimeout)

    when:
    List<SelectionPrice> resultPrice = selectionPriceRepository.multiGet(Arrays.asList("testKey3", "testKey4"))
        .block(redisOperationTimeout)
    then:
    (resultPrice.get(0) == selectionPrice1 && resultPrice.get(1) == selectionPrice2) || (resultPrice.get(0) == selectionPrice2 && resultPrice.get(1) == selectionPrice1)
  }

  def "Test remove from Redis"() {
    given:
    SelectionPrice selectionPrice = SelectionPrice.builder()
        .outcomeId("1115")
        .priceDen("1")
        .priceNum("2")
        .build()
    selectionPriceRepository.save("testKey5", selectionPrice).block(redisOperationTimeout)

    when:
    Boolean resultPrice = selectionPriceRepository.delete("testKey5").block(redisOperationTimeout)
    then:
    resultPrice
  }
}
