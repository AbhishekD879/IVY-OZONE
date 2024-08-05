package com.ladbrokescoral.aggregation.service.impl

import com.ladbrokescoral.aggregation.configuration.SilksProperties
import com.ladbrokescoral.aggregation.model.ImageData
import com.ladbrokescoral.aggregation.model.SilkUrl
import com.ladbrokescoral.aggregation.service.ImageProviderService
import com.ladbrokescoral.aggregation.service.SilkUrlProviderService
import com.ladbrokescoral.aggregation.utils.ImageUtils
import com.ladbrokescoral.aggregation.utils.VerticalSpriteGenerator
import reactor.core.publisher.Mono
import spock.lang.Specification

import java.awt.image.BufferedImage

class AggregationServiceImplTest extends Specification {
  def imageProvider = Mock(ImageProviderService)
  def silkUrlProvider = Mock(SilkUrlProviderService)
  def spriteGenerator = Mock(VerticalSpriteGenerator)
  def silksProperties = Mock(SilksProperties)
  def defaultSilk = new BufferedImage(5, 5, 1)

  def service

  void setup() {
    service = new AggregationServiceImpl(spriteGenerator, silksProperties, imageProvider, silkUrlProvider)
  }

  def "aggregate image with provider"() {
    given:
    silksProperties.getImageProvider("racingpost-coral") >> Optional.of(imageProvider())
    silksProperties.getExpectedExtension() >> "gif"
    List<String> inputSilkIds = generateIdsSequence(2)
    mockImageProvider(inputSilkIds)

    spriteGenerator.generate(_ as List) >> Optional.of(new BufferedImage(20, 20, 1))
    spriteGenerator.generate(_ as List, defaultSilk) >> Optional.of(new BufferedImage(111, 222, 1))

    when:
    def provider = service.imageAggregationByProvider(inputSilkIds, "racingpost-coral", "987")
    def block = provider.block()

    then:
    block != null
    block.length > 0
    noExceptionThrown()
  }

  def mockImageProvider(List<String> inputSilkIds) {
    for (String id : inputSilkIds) {
      imageProvider.getImage(silkUrl(id)) >> Mono.just(imageData(id))
    }
  }

  def "aggregate images in requested order"() {
    given:
    silksProperties.getImageProvider("racingpost-coral") >> Optional.of(imageProvider())
    silksProperties.getExpectedExtension() >> "gif"
    spriteGenerator.generate(_ as List) >> Optional.of(new BufferedImage(20, 20, 1))
    def inputSilkIds = generateIdsSequence(10)
    def imageDataMap = generateImageDataMap(inputSilkIds)

    and: "images are retrieving in invalid order"
    def wrongOrderedImages = []
    for (int i = inputSilkIds.size() - 1; i >= 0; i--) {
      wrongOrderedImages.add(Mono.just(imageDataMap.get(i.toString())))
    }
    imageProvider.getImage(_ as SilkUrl) >>> wrongOrderedImages

    and: "spriteGenerator accepts silks in order of inputSilkIds"
    def silkImages = new ArrayList<Optional>()
    for (def silkId : inputSilkIds) {
      silkImages.add(imageDataMap.get(silkId).getImageContent())
    }
    def expectedImageWidth = 111
    def expectedImageHeigth = 222
    def aggregatedImage = new BufferedImage(expectedImageWidth, expectedImageHeigth, 1)
    spriteGenerator.generate(
        silkImages,
        defaultSilk) >> Optional.of(aggregatedImage)

    when:
    def provider = service.imageAggregationByProvider(inputSilkIds, "racingpost-coral", "987")
    byte[] block = provider.block()

    then:
    block != null
    block.length > 0
    noExceptionThrown()
    def actualImage = ImageUtils.toBufferedImage(block)
    actualImage.getWidth() == expectedImageWidth
    actualImage.getHeight() == expectedImageHeigth
  }

  def "aggregate image with provider - error"() {
    given:
    silksProperties.getImageProvider("racingpost-coral") >> Optional.of(imageProvider())
    silksProperties.getExpectedExtension() >> "gif"
    List<String> inputSilkIds = generateIdsSequence(2)
    mockImageProvider(inputSilkIds)
    spriteGenerator.generate(_ as List) >> Optional.empty()

    when:
    service.imageAggregationByProvider(inputSilkIds, "racingpost-coral", "987")

    then:
    RuntimeException ex = thrown()
  }

  def imageProvider() {
    SilksProperties.ImageProvider imageProvider = new SilksProperties.ImageProvider()
    imageProvider.endpoint = "https://silk"
    imageProvider.defaultSilk = defaultSilk
    return imageProvider
  }

  def silkUrl(String silkId) {
    return SilkUrl.builder().endpoint("https://silk/" + silkId + ".gif").silkId(silkId).build()
  }

  def imageData(String imageId) {
    BufferedImage image = imageForId(imageId)
    return ImageData.builder().imageContent(Optional.ofNullable(image)).imageId(imageId).build()
  }

  def imageForId(String imageId) {
    def k = Integer.valueOf(imageId)
    if (k == null || k < 1) {
      return null
    }
    return new BufferedImage(k * 10, k * 10, 1)
  }

  def generateIdsSequence(int number) {
    List<String> ids = new ArrayList<>(number)
    for (int i = 0; i < number; i++) {
      ids.add(i.toString())
    }
    return ids
  }

  def generateImageDataMap(List<String> ids) {
    def imageDataMap = new HashMap<String, ImageData>()
    for (String id : ids) {
      def imageData = imageData(id)
      imageDataMap.put(id, imageData)
    }
    return imageDataMap
  }

  def "aggregate image without provider"() {
    def eventIds = Arrays.asList("123", "456")
    given:
    List<SilkUrl> silkUrls = new ArrayList<>()
    List<String> ids = generateIdsSequence(2)
    for (String id : ids) {
      imageProvider.getImage(silkUrl(id)) >> Mono.just(imageData(id))
      silkUrls.add(silkUrl(id))
    }
    silkUrlProvider.getSilksUrlsByEventIds("coral", eventIds) >> Mono.just(silkUrls)
    silksProperties.getImageProvider("coral") >> Optional.of(imageProvider())
    silksProperties.getExpectedExtension() >> "gif"


    spriteGenerator.generate(_ as List) >> Optional.of(new BufferedImage(20, 20, 1))
    spriteGenerator.generate(_ as List, defaultSilk) >> Optional.of(new BufferedImage(111, 222, 1))

    when:
    def provider = service.imageAggregationByBrand(eventIds, "coral", "987")
    def block = provider.block()

    then:
    block != null
    block.length > 0
    noExceptionThrown()
  }

  def "test extension removing"() {
    given:
    def eventIds = Arrays.asList("123.gif", "456.png", "678")
    when:
    def ids = service.cleanSilkIds(eventIds)

    then:
    ids.get(0) == "123"
    ids.get(1) == "456"
    ids.get(2) == "678"
  }
}
