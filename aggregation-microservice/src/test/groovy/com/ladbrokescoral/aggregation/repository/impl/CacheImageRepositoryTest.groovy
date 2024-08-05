package com.ladbrokescoral.aggregation.repository.impl

import com.ladbrokescoral.aggregation.config.EmbededRedis

import com.ladbrokescoral.aggregation.utils.ImageUtils
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
class CacheImageRepositoryTest extends Specification {
  @Autowired
  ReactiveRedisTemplate<String, byte[]> reactiveRedisTemplate
  private Duration redisOperationTimeout = Duration.ofSeconds(2L)
  private Duration seconds = Duration.ofSeconds(100)

  def "Save Racing Post Image"() {
    given:
    CacheImageRepository imageRepository = new CacheImageRepository(reactiveRedisTemplate, seconds)
    def image = ImageUtils.loadImage(this.class, "silk1.gif")
    def byteArray = ImageUtils.toByteArray(image)

    when:
    byte[] savedImage = imageRepository.save("testImage1", byteArray).block(redisOperationTimeout)

    then:
    byteArray == savedImage
  }

  def "Test get Racing Post at Redis"() {
    given:
    CacheImageRepository imageRepository = new CacheImageRepository(reactiveRedisTemplate, seconds)
    def image = ImageUtils.loadImage(this.class, "silk1.gif")
    def byteArray = ImageUtils.toByteArray(image)
    imageRepository.save("testImage2", byteArray).block(redisOperationTimeout)

    when:
    byte[] resultImage = imageRepository.get("testImage2").block(redisOperationTimeout)
    then:
    byteArray == resultImage
  }

  def "Test multi get Racing Post at Redis"() {
    given:
    CacheImageRepository imageRepository = new CacheImageRepository(reactiveRedisTemplate, seconds)
    def image1 = ImageUtils.loadImage(this.class, "silk1.gif")
    def image2 = ImageUtils.loadImage(this.class, "silk1.gif")
    def byteArray1 = ImageUtils.toByteArray(image1)
    def byteArray2 = ImageUtils.toByteArray(image2)

    imageRepository.save("testImage3", byteArray1).block(redisOperationTimeout)
    imageRepository.save("testImage4", byteArray2).block(redisOperationTimeout)

    when:
    List<byte[]> resultPrice = imageRepository.multiGet(Arrays.asList("testImage3", "testImage4"))
        .block(redisOperationTimeout)
    then:
    (resultPrice.get(0) == byteArray1 && resultPrice.get(1) == byteArray2) || (resultPrice.get(0) == byteArray2 && resultPrice.get(1) == byteArray1)
  }

  def "Test remove from Redis"() {
    given:
    CacheImageRepository imageRepository = new CacheImageRepository(reactiveRedisTemplate, seconds)
    def image = ImageUtils.loadImage(this.class, "silk1.gif")
    def byteArray1 = ImageUtils.toByteArray(image)
    imageRepository.save("testImage5", byteArray1).block(redisOperationTimeout)

    when:
    Boolean resultPrice = imageRepository.delete("testImage5").block(redisOperationTimeout)
    then:
    resultPrice
  }
}
