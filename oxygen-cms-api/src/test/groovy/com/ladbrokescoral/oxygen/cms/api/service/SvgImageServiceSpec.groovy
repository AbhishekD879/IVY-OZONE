package com.ladbrokescoral.oxygen.cms.api.service

import com.ladbrokescoral.oxygen.cms.api.entity.SvgFilename
import com.ladbrokescoral.oxygen.cms.api.entity.SvgImage
import com.ladbrokescoral.oxygen.cms.api.entity.SvgSprite
import com.ladbrokescoral.oxygen.cms.api.repository.SvgImageRepository
import org.springframework.web.multipart.MultipartFile
import spock.lang.Specification

import java.util.stream.Collectors
import java.util.stream.Stream

class SvgImageServiceSpec extends Specification {

  SvgImageService svgImageService
  SvgImageRepository svgImageRepository
  SvgEntityService<SvgImage> svgEntityService
  SvgImageParser svgImageParser

  def setup() {
    svgEntityService = Mock(SvgEntityService)
    svgImageRepository = Mock(SvgImageRepository)
    svgImageParser = Mock(SvgImageParser)
    svgImageService = new SvgImageService(svgImageRepository, svgEntityService, "images/svg", svgImageParser)
  }

  def "create svg image with no sprite"() {
    given:
    MultipartFile file = Mock()
    def fileName = "fileName"
    file.getOriginalFilename() >> fileName

    when:
    def image = svgImageService.createSvgImage(new SvgImage(), file)

    then:
    1 * svgEntityService.attachSvgImage(*_)
    image.getSprite() == SvgSprite.ADDITIONAL.getSpriteName()
  }

  def "search svgImages by search/active"() {
    given:
    svgImageRepository.findByBrand("bma") >> svgsForSearch()

    when:
    def images = svgImageService.searchByBrand("bma", "some text", true)

    then:
    images.size() == 3
  }

  def "find all by brand and sprite"() {
    given:
    svgImageRepository.findAllByBrandAndSprite("bma", "timeline") >> svgsForSearch()

    when:
    def images = svgImageService.findAllByBrandAndSprite("bma", "timeline")

    then:
    images.size() == 5
  }

  def "search svgImages by search/inactive"() {
    given:
    svgImageRepository.findByBrand("bma") >> svgsForSearch()

    when:
    def images = svgImageService.searchByBrand("bma", "some text", false)

    then:
    images.size() == 1
  }

  def "create svg image with sprite specified"() {
    given:
    MultipartFile file = Mock()
    file.getOriginalFilename() >> "fileName"

    def svgImage = new SvgImage()
    svgImage.setSprite(SvgSprite.INITIAL.getSpriteName())

    when:
    def image = svgImageService.createSvgImage(svgImage, file)

    then:
    1 * svgEntityService.attachSvgImage(*_)
    image.getSprite() == SvgSprite.INITIAL.getSpriteName()
  }

  def "update svg images"() {
    given:
    def existing = new SvgImage()
    existing.setSprite(SvgSprite.INITIAL.getSpriteName())
    existing.setSvgId("oldId")

    def updated = new SvgImage()
    updated.setSprite(SvgSprite.ADDITIONAL.getSpriteName())
    updated.setSvgId("newId")
    updated.setSvgFilename(new SvgFilename())
    svgImageRepository.save(_ as SvgImage) >> ({
      arg -> return arg[0]
    })

    when:
    def result = svgImageService.update(existing, updated)

    then:
    result.getSvgId() == updated.getSvgId()
    result.getSprite() == updated.getSprite()
  }

  def "attach svg image"() {
    given:
    MultipartFile file = Mock()

    def svgUpdate = new SvgImage()
    svgUpdate.setSvgId("changed-svg-idd")

    def svgImage = new SvgImage()
    svgImage.setId("id")
    svgImage.setSvgId("svg-idd")
    svgImage.setSprite(SvgSprite.INITIAL.getSpriteName())
    svgImage.setSvg("some svg content includes id=\"svg-idd\"")

    svgImageRepository.findById("id") >> Optional.of(svgImage)
    svgEntityService.removeSvgImage(*_) >> Optional.empty()
    svgEntityService.attachSvgImage(*_) >> ({
      arg -> return Optional.of(arg[0])
    })
    svgImageRepository.save(svgImage) >> ({
      arg -> return arg[0]
    })

    when:
    def image = svgImageService.replaceSvgImage("id", file, svgUpdate)

    then:
    image.getSprite() == SvgSprite.INITIAL.getSpriteName()
  }

  def "should not fail on update without file"() {
    given:
    def svgImage = new SvgImage()
    svgImage.setId("id")
    svgImage.setSprite(SvgSprite.INITIAL.getSpriteName())
    svgImageRepository.findById("id") >> Optional.of(svgImage)
    svgEntityService.removeSvgImage(*_) >> Optional.empty()
    svgImageRepository.save(svgImage) >> ({
      arg -> return arg[0]
    })

    when:
    def image = svgImageService.replaceSvgImage("id", null, new SvgImage())

    then:
    image.getSprite() == SvgSprite.INITIAL.getSpriteName()
  }

  def "RemoveSvgImage"() {
    given:
    def svgImage = new SvgImage()
    svgImage.setSprite(SvgSprite.INITIAL.getSpriteName())
    svgImageRepository.findById("id") >> Optional.of(svgImage)
    svgEntityService.removeSvgImage(*_) >> Optional.of(svgImage)
    svgImageRepository.save(svgImage) >> svgImage

    when:
    def image = svgImageService.removeSvgImage("id")

    then:
    image.isPresent()
    image.get().getSprite() == SvgSprite.INITIAL.getSpriteName()
  }

  def "get sprites list"() {

    when:
    def sprites = svgImageService.getSprites("brand")

    then:
    sprites.containsAll(Stream.of(SvgSprite.values()).map({s -> s.getSpriteName()}).collect(Collectors.toList()))
  }

  def svgsForSearch() {
    def bmaSvg = new SvgImage()
    bmaSvg.setBrand("bma")
    bmaSvg.setActive(false)
    bmaSvg.setSvgId("some text")

    def bmaSvg1 = new SvgImage()
    bmaSvg1.setBrand("bma")
    bmaSvg1.setSvgId("some text in the beginning")

    def bmaSvg2 = new SvgImage()
    bmaSvg2.setBrand("bma")
    bmaSvg2.setSvgId("in some text middle")

    def bmaSvg3 = new SvgImage()
    bmaSvg3.setBrand("bma")
    bmaSvg3.setSvgId("in the ending some text")

    def bmaSvg4 = new SvgImage()
    bmaSvg4.setBrand("bma")
    bmaSvg4.setSvgId("no search text in")

    return Arrays.asList(bmaSvg, bmaSvg1, bmaSvg2, bmaSvg3, bmaSvg4)
  }
}
