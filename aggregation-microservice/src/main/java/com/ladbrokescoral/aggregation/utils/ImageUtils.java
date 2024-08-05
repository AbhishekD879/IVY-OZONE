package com.ladbrokescoral.aggregation.utils;

import com.ladbrokescoral.aggregation.exception.InitializationException;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import javax.imageio.ImageIO;
import lombok.extern.slf4j.Slf4j;
import reactor.core.publisher.Mono;

@Slf4j
public final class ImageUtils {

  private ImageUtils() {}

  public static Mono<byte[]> toByteArray(Mono<BufferedImage> image) {
    return image.map(ImageUtils::toByteArray);
  }

  public static byte[] toByteArray(BufferedImage image) {
    try {
      ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
      ImageIO.write(image, "png", outputStream);
      outputStream.flush();
      final byte[] byteArray = outputStream.toByteArray();
      outputStream.close();
      return byteArray;
    } catch (IOException exception) {
      log.error("Can't convert image to byte array", exception);
      // TODO: create dummy silk with default images (how to identify provider type and images for
      // replacement?)
      return new byte[] {};
    }
  }

  /** Loads image from resource folder */
  public static BufferedImage loadImage(Class clazz, String imgFileName) {
    ClassLoader classLoader = clazz.getClassLoader();

    if (classLoader != null) {
      try (InputStream resourceAsStream = classLoader.getResourceAsStream(imgFileName); ) {
        if (resourceAsStream == null) {
          throw new IllegalArgumentException("Couldn't find image=" + imgFileName);
        }

        return ImageIO.read(resourceAsStream);
      } catch (IOException iOException) {
        log.error("Couldn't read image from file", iOException);
        throw new InitializationException(
            "Couldn't read image from file=" + imgFileName, iOException);
      }
    }
    return null;
  }

  public static BufferedImage toBufferedImage(byte[] byteArray) {
    try (ByteArrayInputStream bis = new ByteArrayInputStream(byteArray)) {
      return ImageIO.read(bis);
    } catch (IOException exception) {
      log.error("Can't convert byte array to buffered image", exception);
      throw new RuntimeException("Can't convert byte array to buffered image ", exception);
    }
  }
}
