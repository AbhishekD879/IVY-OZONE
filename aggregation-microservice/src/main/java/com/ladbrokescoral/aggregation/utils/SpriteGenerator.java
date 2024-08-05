package com.ladbrokescoral.aggregation.utils;

import java.awt.image.BufferedImage;
import java.util.List;
import java.util.Optional;

public interface SpriteGenerator<T> {
  Optional<T> generate(List<Optional<T>> images, BufferedImage defaultImg);

  Optional<T> generate(List<Optional<T>> images);

  boolean isImageWithExpectedSize(BufferedImage image);
}
