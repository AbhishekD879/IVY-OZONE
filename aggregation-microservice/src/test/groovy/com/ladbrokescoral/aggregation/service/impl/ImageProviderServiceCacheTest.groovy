package com.ladbrokescoral.aggregation.service.impl

import com.ladbrokescoral.aggregation.config.EmbededRedis
import com.ladbrokescoral.aggregation.configuration.ApiProperties
import com.ladbrokescoral.aggregation.model.ImageData
import com.ladbrokescoral.aggregation.model.SilkUrl
import com.ladbrokescoral.aggregation.repository.impl.CacheImageRepository
import com.ladbrokescoral.aggregation.utils.SpriteGenerator
import com.ladbrokescoral.aggregation.utils.VerticalSpriteGenerator

import java.awt.image.BufferedImage
import java.time.Duration

import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.data.redis.core.ReactiveRedisTemplate
import org.springframework.test.annotation.DirtiesContext
import org.springframework.test.context.ActiveProfiles
import org.springframework.web.reactive.function.client.WebClient

import spock.lang.Specification

@SpringBootTest(classes = EmbededRedis)
@ActiveProfiles("UNIT")
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
class ImageProviderServiceCacheTest extends Specification {
  @Autowired
  ReactiveRedisTemplate<String, byte[]> reactiveRedisTemplate

  def "Testing image cache"() {
    given:
    WebClient webClient = WebClient.create();
    SpriteGenerator<BufferedImage> verticalSpriteGenerator = Mock()
    verticalSpriteGenerator.isImageWithExpectedSize(_) >> true
    CacheImageRepository cacheImageRepository = new CacheImageRepository(reactiveRedisTemplate, Duration.ofSeconds(100))
    ImageProviderImpl imageProvider = new ImageProviderImpl(webClient, cacheImageRepository, getProperties(), verticalSpriteGenerator)
    SilkUrl silkUrl = new SilkUrl.SilkUrlBuilder().endpoint("https://img.coral.co.uk/img/racing_post/", "testId", "").build()
    when:
    imageProvider.getImage(silkUrl).subscribe()
    then:
    noExceptionThrown()
  }

  def "When image size correct - image cached"() {
    given:
    WebClient webClient = WebClient.create();
    SpriteGenerator<BufferedImage> verticalSpriteGenerator = new VerticalSpriteGenerator(40,29)
    CacheImageRepository cacheImageRepository = new CacheImageRepository(reactiveRedisTemplate, Duration.ofSeconds(100))
    def spyCacheImageRepository = Spy(cacheImageRepository)
    ImageProviderImpl imageProvider = new ImageProviderImpl(webClient, spyCacheImageRepository, getProperties(), verticalSpriteGenerator)
    when:
    imageProvider.cacheImageData("id", "key", new ImageData("dsds", Optional.of(new BufferedImage(40, 29, 1)), null))
    then:
    1 * spyCacheImageRepository.save(_, _)
  }

  def "When image size incorrect - not cached"() {
    given:
    WebClient webClient = WebClient.create();
    SpriteGenerator<BufferedImage> verticalSpriteGenerator = new VerticalSpriteGenerator(40,29)
    CacheImageRepository cacheImageRepository = new CacheImageRepository(reactiveRedisTemplate, Duration.ofSeconds(100))
    def spyCacheImageRepository = Spy(cacheImageRepository)
    ImageProviderImpl imageProvider = new ImageProviderImpl(webClient, spyCacheImageRepository, getProperties(), verticalSpriteGenerator)
    when:
    imageProvider.cacheImageData("id", "key", new ImageData("dsds", Optional.of(new BufferedImage(40, 30, 1)), null))
    then:
    0 * spyCacheImageRepository.save(_, _)
  }

  def getProperties() {
    ApiProperties properties = new ApiProperties();
    ApiProperties.Image image = new ApiProperties.Image();
    image.setNumberOfRetries(3);
    properties.setImage(image);
    return properties;
  }
}
