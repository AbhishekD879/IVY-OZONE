package com.ladbrokescoral.aggregation.model;

import java.awt.image.BufferedImage;
import java.util.Optional;
import lombok.Builder;
import lombok.Data;

@Builder
@Data
public class ImageData {

  private String imageId;
  private Optional<BufferedImage> imageContent;
  private Throwable throwable;
}
