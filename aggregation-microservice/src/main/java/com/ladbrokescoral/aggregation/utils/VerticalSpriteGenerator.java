package com.ladbrokescoral.aggregation.utils;

import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.util.CollectionUtils;

@RequiredArgsConstructor
@Slf4j
public class VerticalSpriteGenerator implements SpriteGenerator<BufferedImage> {

  private final int expectedWidth;
  private final int expectedHeight;

  /**
   * Generates vertical sprite from images where order of images in list is the same as order of
   * images in sprite from top to bottom
   *
   * <p>If width or height of image isn't correct, substitutes it with defaultImage
   */
  @Override
  public Optional<BufferedImage> generate(
      List<Optional<BufferedImage>> images, BufferedImage defaultImg) {
    if (CollectionUtils.isEmpty(images)) {
      log.warn("Nothing to generate sprite from!");
      return Optional.empty();
    } else {
      return Optional.of(generateVerticalSprite(images, defaultImg));
    }
  }

  /**
   * Just like #{@link this#generate(List, BufferedImage)}, generates vertical sprite. But, if
   * missing or invalid image present it raises exception instead of substituting is with default
   * image
   */
  @Override
  public Optional<BufferedImage> generate(List<Optional<BufferedImage>> images) {
    return generate(images, null);
  }

  private BufferedImage generateVerticalSprite(
      List<Optional<BufferedImage>> images, BufferedImage defaultImg) {
    BufferedImage verticalSprite =
        new BufferedImage(
            expectedWidth, expectedHeight * images.size(), BufferedImage.TYPE_INT_ARGB);

    Graphics2D spriteGraphics = verticalSprite.createGraphics();

    int currentHeight = 0;
    for (BufferedImage image : withReplacedInvalidImagesOrMissingImages(images, defaultImg)) {
      spriteGraphics.drawImage(image, 0, currentHeight, null);
      currentHeight += image.getHeight();
    }
    spriteGraphics.dispose();
    return verticalSprite;
  }

  private List<BufferedImage> withReplacedInvalidImagesOrMissingImages(
      List<Optional<BufferedImage>> images, BufferedImage defaultImg) {
    return images.stream()
        .map(
            maybeImg -> {
              if (maybeImg.isPresent() && isImageWithExpectedSize(maybeImg.get())) {
                return maybeImg.get();
              } else if (defaultImg != null) {
                return defaultImg;
              } else {
                throw new IllegalStateException(
                    "Invalid image detected during sprite generation and there is not default image supplied!");
              }
            })
        .collect(Collectors.toList());
  }

  public boolean isImageWithExpectedSize(BufferedImage image) {
    return image.getHeight() == expectedHeight && image.getWidth() == expectedWidth;
  }
}
