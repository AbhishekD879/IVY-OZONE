package com.ladbrokescoral.oxygen.cms.api.service

import com.ladbrokescoral.oxygen.cms.api.entity.Filename
import com.ladbrokescoral.oxygen.cms.api.entity.OnBoardingGuide
import com.ladbrokescoral.oxygen.cms.api.entity.Svg
import com.ladbrokescoral.oxygen.cms.api.entity.SvgFilename
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException
import com.ladbrokescoral.oxygen.cms.api.repository.OnBoardingGuideRepository
import org.springframework.web.multipart.MultipartFile
import spock.lang.Specification

class OnBoardingGuideServiceSpec extends Specification {

  OnBoardingGuideRepository repository = Mock(OnBoardingGuideRepository)
  ImageService imageService = Mock(ImageService)
  MultipartFile file = Mock(MultipartFile)
  String path = "/path/test"
  String brand = "bma"

  OnBoardingGuideService service = new OnBoardingGuideService(repository, imageService, path)

  def "AttachSvgImage"() {
    OnBoardingGuide entity = new OnBoardingGuide()
    entity.setGuideName("testName")
    entity.setBrand(brand)
    Filename filename = new Filename()
    filename.setFilename("test.svg")
    filename.setSize("10")
    given:
    imageService.upload(brand, file, "/path/test") >> Optional.of(filename)

    when:
    service.attachSvgImage(entity, file)

    then:
    entity.getGuidePath() == "/path/test/test.svg"
    entity.getSvgFilename() != null
    entity.getSvgFilename().getFilename() == "test.svg"
  }

  def "AttachSvgImage - IllegalStateException"() {
    OnBoardingGuide entity = new OnBoardingGuide()
    entity.setBrand(brand)
    entity.setGuideName("testName")
    given:
    imageService.upload(brand, file, "/path/test") >> Optional.empty()
    when:
    service.attachSvgImage(entity, file)
    then:
    IllegalStateException exception = thrown()
    exception.getMessage().contains("An error occurred during image uploading")
  }

  def "RemoveSvgImage"() {
    OnBoardingGuide onBoardingGuide = new OnBoardingGuide()
    onBoardingGuide.setBrand(brand)
    SvgFilename svg = new SvgFilename()
    svg.setPath("/path/test/testName")
    svg.setFilename("test.png")
    onBoardingGuide.setSvgFilename(svg)
    onBoardingGuide.setGuidePath("/path/test/testName/test.png")
    given:
    imageService.removeImage(brand, "path/test/testName/test.png") >> Boolean.TRUE
    when:
    service.removeSvgImage(onBoardingGuide)
    then:
    onBoardingGuide.getSvgFilename() == null
    onBoardingGuide.getGuidePath() == null
  }
}
