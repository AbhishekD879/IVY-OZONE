package com.ladbrokescoral.aggregation.repository.impl

import com.ladbrokescoral.aggregation.config.EmbededRedis

import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.data.redis.core.ReactiveRedisTemplate
import org.springframework.test.annotation.DirtiesContext
import org.springframework.test.context.ActiveProfiles
import spock.lang.Specification

import java.time.Duration

@SpringBootTest(classes = EmbededRedis)
@ActiveProfiles("UNIT")
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
class CachePathRepositoryTest extends Specification {
  @Autowired
  ReactiveRedisTemplate<String, byte[]> reactiveRedisTemplate
  private Duration redisOperationTimeout = Duration.ofSeconds(2L)
  private Duration seconds = Duration.ofSeconds(100)

  def "Save Racing Post Image"() {
    given:
    CacheImageRepository imageRepository = new CacheImageRepository(reactiveRedisTemplate, seconds)
    byte[] image = "Any image".getBytes();

    when:
    byte[] savedImage = imageRepository.save("testImage1", image).block(redisOperationTimeout)

    then:
    image == savedImage
  }

  def "Test get Racing Post at Redis"() {
    given:
    CachePathRepository imageRepository = new CachePathRepository(reactiveRedisTemplate, seconds)
    byte[] image = "Any image".getBytes();
    imageRepository.save("testImage2", image).block(redisOperationTimeout)

    when:
    byte[] resultImage = imageRepository.get("testImage2").block(redisOperationTimeout)
    then:
    image == resultImage
  }

  def "Test multi get Racing Post at Redis"() {
    given:
    CachePathRepository imageRepository = new CachePathRepository(reactiveRedisTemplate, seconds)
    byte[] image1 = "Any image1".getBytes();
    byte[] image2 = "Any image2".getBytes();

    imageRepository.save("testImage3", image1).block(redisOperationTimeout)
    imageRepository.save("testImage4", image2).block(redisOperationTimeout)

    when:
    List<byte[]> resultPrice = imageRepository.multiGet(Arrays.asList("testImage3", "testImage4"))
        .block(redisOperationTimeout)
    then:
    (resultPrice.get(0) == image1 && resultPrice.get(1) == image2) || (resultPrice.get(0) == image2 && resultPrice.get(1) == image1)
  }

  def "Test remove from Redis"() {
    given:
    CachePathRepository imageRepository = new CachePathRepository(reactiveRedisTemplate, seconds)
    byte[] image = "Any image".getBytes();
    imageRepository.save("testImage5", image).block(redisOperationTimeout)

    when:
    Boolean resultPrice = imageRepository.delete("testImage5").block(redisOperationTimeout)
    then:
    resultPrice
  }
}
