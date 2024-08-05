package com.ladbrokescoral.aggregation.service.impl

import com.ladbrokescoral.aggregation.configuration.SilksProperties
import com.ladbrokescoral.aggregation.repository.impl.CachePathRepository
import com.ladbrokescoral.aggregation.service.AggregationService
import com.ladbrokescoral.aggregation.service.SilkUrlProviderService
import com.ladbrokescoral.aggregation.utils.SpriteGenerator
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.data.redis.core.ReactiveRedisTemplate
import org.springframework.test.annotation.DirtiesContext
import org.springframework.test.context.ActiveProfiles
import spock.lang.Ignore
import spock.lang.Specification

import java.awt.image.BufferedImage
import java.time.Duration

@SpringBootTest
@ActiveProfiles("UNIT")
@Ignore
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
class AggregationServiceCacheTest extends Specification {
  @Autowired
  ReactiveRedisTemplate<String, byte[]> reactiveRedisTemplate
  @Autowired
  SilksProperties silksProperties
  @Autowired
  SpriteGenerator<BufferedImage> spriteGenerator
  @Autowired
  SilkUrlProviderService silkUrlProvider

  def "test image cache"() {
    given:
    CachePathRepository cachePathRepository = new CachePathRepository(reactiveRedisTemplate, Duration.ofSeconds(10))
    ImageProviderImpl provider = Mock()
    AggregationService aggregationService = new AggregationServiceImpl(spriteGenerator, silksProperties, provider, silkUrlProvider, cachePathRepository)
    when:
    aggregationService.imageAggregationByBrand( Arrays.asList("testId"), "teamtalk-coral", "uuid").subscribe()
    then:
    noExceptionThrown()
  }
}
