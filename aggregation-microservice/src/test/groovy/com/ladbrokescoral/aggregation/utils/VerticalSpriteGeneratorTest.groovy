package com.ladbrokescoral.aggregation.utils

import spock.lang.Specification

import javax.imageio.ImageIO
import java.awt.image.BufferedImage

class VerticalSpriteGeneratorTest extends Specification {
  def silk1Img = loadImage("silk1.gif")
  def silk2Img = loadImage("silk2.gif")
  def silk3Img = loadImage("silk3.gif")
  def notSilkImg = loadImage("notsilk.gif")
  def defaultImg = loadImage("defaultSilk.gif")
  def silkWidth = 40
  def silkHeight = 29
  def generator = new VerticalSpriteGenerator(silkWidth, silkHeight)

  def "If no images supplied then empty sprite is generated"() {
    when:
    def sprite = generator.generate([])
    def sprite2 = generator.generate([], defaultImg)
    then:
    !sprite.isPresent()
    !sprite2.isPresent()
  }

  def "If one image supplied then it is returned as it is"() {
    when:
    def sprite = generator.generate([Optional.of(silk1Img)]).get()
    then:
    compareImages(getImageAtIdx(sprite, 0), silk1Img)
  }

  def "Sprite is generated in order 1 2 3"() {
    when:
    def sprite = generator.generate([
      Optional.of(silk1Img),
      Optional.of(silk2Img),
      Optional.of(silk3Img)
    ]).get()
    then:
    saveFileToBuildFolder(sprite)
    compareImages(getImageAtIdx(sprite, 0), silk1Img)
    compareImages(getImageAtIdx(sprite, 1), silk2Img)
    compareImages(getImageAtIdx(sprite, 2), silk3Img)
  }

  def "Sprite generated in order 2 1 3"() {
    when:
    def sprite = generator.generate([
      Optional.of(silk2Img),
      Optional.of(silk1Img),
      Optional.of(silk3Img)
    ]).get()
    then:
    saveFileToBuildFolder(sprite)

    compareImages(getImageAtIdx(sprite, 1), silk1Img)
    compareImages(getImageAtIdx(sprite, 0), silk2Img)
    compareImages(getImageAtIdx(sprite, 2), silk3Img)
  }

  def "Image with incorrect size is replaced with default image in sprite"() {
    when:
    def sprite = generator.generate([
      Optional.of(silk1Img),
      Optional.of(silk2Img),
      Optional.of(notSilkImg),
      Optional.of(silk3Img)
    ], defaultImg).get()
    then:
    saveFileToBuildFolder(sprite)
    sprite.getHeight() == 4 * silkHeight
    sprite.getWidth() == silkWidth
    compareImages(getImageAtIdx(sprite, 0), silk1Img)
    compareImages(getImageAtIdx(sprite, 1), silk2Img)
    compareImages(getImageAtIdx(sprite, 2), defaultImg)
    compareImages(getImageAtIdx(sprite, 3), silk3Img)
  }

  def "Missing images replaced with default images"() {
    when:
    def sprite = generator.generate([
      Optional.of(silk1Img),
      Optional.of(silk2Img),
      Optional.empty(),
      Optional.empty()
    ], defaultImg).get()
    then:
    saveFileToBuildFolder(sprite)
    sprite.getHeight() == 4 * silkHeight
    sprite.getWidth() == silkWidth
    compareImages(getImageAtIdx(sprite, 0), silk1Img)
    compareImages(getImageAtIdx(sprite, 1), silk2Img)
    compareImages(getImageAtIdx(sprite, 2), defaultImg)
    compareImages(getImageAtIdx(sprite, 3), defaultImg)
  }

  def "Exception is thrown when missing image present but no default image supplied"() {
    when:
    def sprite = generator.generate([
      Optional.of(silk1Img),
      Optional.empty()
    ]).get()
    then:
    thrown(IllegalStateException)
  }

  def "Exception is thrown when invalid image present but no default image supplied"() {
    when:
    def sprite = generator.generate([
      Optional.of(silk1Img),
      Optional.of(notSilkImg)
    ]).get()
    then:
    thrown(IllegalStateException)
  }

  private void saveFileToBuildFolder(BufferedImage sprite) {
    try {
      def spriteFileResult = new File("images-output/${UUID.randomUUID()}.gif")
      ImageIO.write(sprite, "gif", spriteFileResult)
      println("Saved result sprite: ${spriteFileResult.getAbsolutePath()}")
    } catch (Exception e) {
      println("Didn't write resulted sprite")
    }
  }

  private BufferedImage getImageAtIdx(BufferedImage sprite, int index) {
    return sprite.getSubimage(0, index * silkHeight, silkWidth, silkHeight)
  }

  private BufferedImage loadImage(String imgName) {
    return ImageUtils.loadImage(this.getClass(), imgName)
  }

  //compares images by size and then by each pixel
  private static boolean compareImages(BufferedImage imgA, BufferedImage imgB) {
    if (imgA.getWidth() != imgB.getWidth() || imgA.getHeight() != imgB.getHeight()) {
      println("Size not equal")
      return false
    }

    int width = imgA.getWidth()
    int height = imgA.getHeight()

    // Loop over every pixel.
    for (int y = 0; y < height; y++) {
      for (int x = 0; x < width; x++) {
        // Compare the pixels for equality.
        if (imgA.getRGB(x, y) != imgB.getRGB(x, y)) {
          println("Pixels not equal")
          return false
        }
      }
    }

    return true
  }
}
