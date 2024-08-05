package com.ladbrokescoral.oxygen.cms.api.service.impl;

import static com.ladbrokescoral.oxygen.cms.util.PathUtil.*;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.util.ImageUtil;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;
import javax.imageio.ImageIO;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.multipart.MultipartFile;

@Slf4j
public abstract class ImageServiceImpl implements ImageService {

  public abstract boolean uploadImage(
      String brand, InputStream imageStream, String imageName, String path);

  protected abstract String getRootUrl(String brand);

  /**
   * Upload image with randlomly generated name, fileName includes size suffix e.g.
   * c45fe41e-31f6-48ed-93f2-9009fda6844c-32x32.png
   *
   * @param image
   * @param path
   * @param size - if null, original size would be uploaded
   * @return
   */
  public Optional<Filename> upload(
      String brand, MultipartFile image, String path, ImageServiceImpl.Size size) {
    // randomize file name
    String randomizeFileName = UUID.randomUUID().toString();
    return upload(brand, image, path, randomizeFileName, size, true);
  }

  /**
   * Upload image with predefined name, fileName doesn't include size suffix e.g. Cricket.png
   *
   * @param image
   * @param path
   * @param fileName
   * @param size - if null, original size would be uploaded
   * @return
   */
  public Optional<Filename> upload(
      String brand,
      @NotNull MultipartFile image,
      @NotEmpty String path,
      @NotEmpty String fileName,
      ImageServiceImpl.Size size) {
    return upload(brand, image, path, fileName, size, false);
  }

  private Optional<Filename> upload(
      String brand,
      @NotNull MultipartFile image,
      @NotEmpty String path,
      @NotEmpty String fileName,
      ImageServiceImpl.Size size,
      boolean addSizeSuffix) {
    String extension = ImageUtil.getImageExtension(image.getOriginalFilename());
    String imageName;
    boolean isUploadSuccessful;

    try (ByteArrayInputStream byteStream = new ByteArrayInputStream(image.getBytes());
        InputStream imageStream =
            Objects.nonNull(size) ? resizeImage(byteStream, size, extension) : byteStream) {

      imageName = getImageName(fileName, size, extension, addSizeSuffix);
      isUploadSuccessful = uploadImage(brand, imageStream, imageName, path);
    } catch (IOException e) {
      log.error("Issue with uploading file: ", e);
      return Optional.empty();
    }

    if (isUploadSuccessful) {
      Filename filename = createFilenameEntity(getRootUrl(brand), image, imageName, path);
      return Optional.of(filename);
    }
    return Optional.empty();
  }

  private String getImageName(
      @NotEmpty String fileName,
      ImageServiceImpl.Size size,
      String extension,
      boolean addSizeSuffix) {
    fileName = fileName.replaceAll("\\s+", "");
    return (Objects.nonNull(size) && addSizeSuffix)
        ? createSizedFileName(fileName, size, extension)
        : createFileName(fileName, extension);
  }

  /**
   * Upload image with randomly generated name, in original size
   *
   * @param image
   * @param path
   * @return
   */
  public Optional<Filename> upload(String brand, MultipartFile image, String path) {
    return upload(brand, image, path, null);
  }

  private Filename createFilenameEntity(
      String rootPath, MultipartFile image, String imageName, String imagePath) {
    Filename fileName = new Filename();
    fileName.setFilename(imageName);
    fileName.setOriginalname(image.getOriginalFilename());
    fileName.setFiletype(image.getContentType());
    fileName.setPath(imagePath);
    fileName.setSize(String.valueOf(image.getSize()));
    fileName.setFullPath(concatPath(concatPath(rootPath, imagePath), imageName));
    return fileName;
  }

  private InputStream resizeImage(
      InputStream source, ImageServiceImpl.Size size, String extension) {
    try {
      BufferedImage originalImage = ImageIO.read(source);
      int type =
          originalImage.getType() == 0 ? BufferedImage.TYPE_INT_ARGB : originalImage.getType();
      BufferedImage resizedImage = resizeImage(originalImage, type, size);

      ByteArrayOutputStream os = new ByteArrayOutputStream();
      ImageIO.write(resizedImage, extension, os);
      return new ByteArrayInputStream(os.toByteArray());
    } catch (IOException e) {
      log.error("Error on resizing image : ", e);
    }
    return null;
  }

  private BufferedImage resizeImage(
      BufferedImage originalImage, int type, ImageServiceImpl.Size size) {
    BufferedImage resizedImage = new BufferedImage(size.getWidth(), size.getHeight(), type);
    Graphics2D g = resizedImage.createGraphics();
    g.drawImage(originalImage, 0, 0, size.getWidth(), size.getHeight(), null);
    g.dispose();

    return resizedImage;
  }

  private String createSizedFileName(
      String original, ImageServiceImpl.Size size, String extension) {
    return new StringBuilder(original)
        .append("-")
        .append(size.getWidth())
        .append("x")
        .append(size.getHeight())
        .append(".")
        .append(extension)
        .toString();
  }

  private String createFileName(String original, String extension) {
    return new StringBuilder(original).append(".").append(extension).toString();
  }

  public static class Size {
    private int height;
    private int width;

    public Size(int width, int height) {
      this.width = width;
      this.height = height;
    }

    public Size(String size) {
      String[] sizes = size.split("x");
      this.width = Integer.valueOf(sizes[0]);
      this.height = Integer.valueOf(sizes[1]);
    }

    public int getHeight() {
      return height;
    }

    public int getWidth() {
      return width;
    }

    @Override
    public String toString() {
      return String.format("%sx%s", width, height);
    }

    @Override
    public boolean equals(Object o) {
      if (this == o) return true;
      if (o == null || getClass() != o.getClass()) return false;
      ImageServiceImpl.Size size = (ImageServiceImpl.Size) o;
      return height == size.height && width == size.width;
    }

    @Override
    public int hashCode() {

      return Objects.hash(height, width);
    }
  }
}
