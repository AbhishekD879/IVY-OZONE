package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.Sport;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.exception.SvgImageParseException;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl;
import java.util.Arrays;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.multipart.MultipartFile;

@Component
public class SportsImageUploadComponent {
  private ImageService imageService;
  private SvgImageParser svgImageParser;

  private final String smallImagesPath;
  private final String mediumImagesPath;
  private final String largeImagesPath;

  private final String smallImagesSize;
  private final String mediumImagesSize;
  private final String largeImagesSize;

  private final String smallIconsPath;
  private final String mediumIconsPath;
  private final String largeIconsPath;

  private final String smallIconsSize;
  private final String mediumIconsSize;
  private final String largeIconsSize;

  private String sportImagesCorePath;
  private String imagesCorePath;

  @Autowired
  public SportsImageUploadComponent(
      ImageService imageService,
      SvgImageParser svgImageParser,
      SportImagesProperties sportImagesProperties,
      @Value("${images.core}") String imagesCorePath) {

    this.imageService = imageService;
    this.svgImageParser = svgImageParser;
    this.imagesCorePath = imagesCorePath;

    sportImagesCorePath = sportImagesProperties.getPath();
    smallImagesPath = sportImagesProperties.getSmall().getPath();
    smallImagesSize = sportImagesProperties.getSmall().getSize();
    mediumImagesPath = sportImagesProperties.getMedium().getPath();
    mediumImagesSize = sportImagesProperties.getMedium().getSize();
    largeImagesPath = sportImagesProperties.getLarge().getPath();
    largeImagesSize = sportImagesProperties.getLarge().getSize();
    smallIconsPath = sportImagesProperties.getIcons().getSmall().getPath();
    smallIconsSize = sportImagesProperties.getIcons().getSmall().getSize();
    mediumIconsPath = sportImagesProperties.getIcons().getMedium().getPath();
    mediumIconsSize = sportImagesProperties.getIcons().getMedium().getSize();
    largeIconsPath = sportImagesProperties.getIcons().getLarge().getPath();
    largeIconsSize = sportImagesProperties.getIcons().getLarge().getSize();
  }

  public void setDefaultImageSizes(Sport entity) {
    ImageServiceImpl.Size smallImageSize = new ImageServiceImpl.Size(smallImagesSize);
    ImageServiceImpl.Size mediumImageSize = new ImageServiceImpl.Size(mediumImagesSize);
    ImageServiceImpl.Size largeImageSize = new ImageServiceImpl.Size(largeImagesSize);

    ImageServiceImpl.Size smallIconSize = new ImageServiceImpl.Size(smallIconsSize);
    ImageServiceImpl.Size mediumIconSize = new ImageServiceImpl.Size(mediumIconsSize);
    ImageServiceImpl.Size largeIconSize = new ImageServiceImpl.Size(largeIconsSize);

    entity.setWidthSmall(smallImageSize.getWidth());
    entity.setHeightSmall(smallImageSize.getHeight());
    entity.setWidthMedium(mediumImageSize.getWidth());
    entity.setHeightMedium(mediumImageSize.getHeight());
    entity.setWidthLarge(largeImageSize.getWidth());
    entity.setHeightLarge(largeImageSize.getHeight());

    entity.setWidthSmallIcon(smallIconSize.getWidth());
    entity.setHeightSmallIcon(smallIconSize.getHeight());
    entity.setWidthMediumIcon(mediumIconSize.getWidth());
    entity.setHeightMediumIcon(mediumIconSize.getHeight());
    entity.setWidthLargeIcon(largeIconSize.getWidth());
    entity.setHeightLargeIcon(largeIconSize.getHeight());
  }

  public Sport attachImages(
      Sport sport, MultipartFile imageFile, MultipartFile icon, MultipartFile svgIcon) {
    attachImage(sport, imageFile);
    attachIcon(sport, icon);
    attachSvg(sport, svgIcon);
    return sport;
  }

  private void attachImage(Sport sport, MultipartFile imageFile) {
    if (imageFile != null) {
      imageService
          .upload(sport.getBrand(), imageFile, imagesCorePath)
          .ifPresent(sport::setFilename);
      // upload resized images
      imageService
          .upload(
              sport.getBrand(),
              imageFile,
              smallImagesPath,
              new ImageServiceImpl.Size(smallImagesSize))
          .ifPresent(
              filename ->
                  sport.setUriSmall(smallImagesPath.concat("/").concat(filename.getFilename())));
      imageService
          .upload(
              sport.getBrand(),
              imageFile,
              mediumImagesPath,
              new ImageServiceImpl.Size(mediumImagesSize))
          .ifPresent(
              filename ->
                  sport.setUriMedium(mediumImagesPath.concat("/").concat(filename.getFilename())));
      imageService
          .upload(
              sport.getBrand(),
              imageFile,
              largeImagesPath,
              new ImageServiceImpl.Size(largeImagesSize))
          .ifPresent(
              filename ->
                  sport.setUriLarge(largeImagesPath.concat("/").concat(filename.getFilename())));
    }
  }

  public void deleteImages(SportsImage[] fileTypes, Sport sport) {
    for (SportsImage fileType : fileTypes) {
      switch (fileType) {
        case IMAGE:
          if (sport.getFilename() != null) {
            imageService.removeImage(sport.getBrand(), sport.getUriLarge());
            imageService.removeImage(sport.getBrand(), sport.getUriMedium());
            imageService.removeImage(sport.getBrand(), sport.getUriSmall());
            sport.clearImageFile();
          }
          break;
        case ICON:
          if (sport.getIcon() != null) {
            imageService.removeImage(sport.getBrand(), sport.getUriLargeIcon());
            imageService.removeImage(sport.getBrand(), sport.getUriMediumIcon());
            imageService.removeImage(sport.getBrand(), sport.getUriSmallIcon());
            sport.clearIcon();
          }
          break;
        case SVG_ICON:
          if (sport.getSvgFilename() != null) {
            Filename svgFilename = sport.getSvgFilename();
            imageService.removeImage(
                sport.getBrand(),
                svgFilename.getPath().concat("/").concat(svgFilename.getFilename()));
            sport.clearSvg();
          }
          break;
        default:
          throw new ValidationException(
              "Unsupported fileType: "
                  + fileType
                  + ". Should be one of the following: "
                  + SportsImage.printFileTypes());
      }
    }
  }

  private void attachSvg(Sport sport, MultipartFile svgIcon) {
    if (svgIcon != null) {
      // upload original images
      Optional<Svg> svg = svgImageParser.parse(svgIcon);
      if (!svg.isPresent()) {
        throw new SvgImageParseException();
      }
      svg.ifPresent(
          parsedSvg -> {
            sport.setSvg(parsedSvg.getSvg());
            sport.setSvgId(parsedSvg.getId());

            imageService
                .upload(sport.getBrand(), svgIcon, sportImagesCorePath)
                .ifPresent(
                    file -> {
                      sport.setSvgFilename(file);
                      sport.getSvgFilename().setPath(sportImagesCorePath);
                    });
          });
    }
  }

  private void attachIcon(Sport sport, MultipartFile iconFile) {
    if (iconFile != null) {
      imageService.upload(sport.getBrand(), iconFile, imagesCorePath).ifPresent(sport::setIcon);
      imageService
          .upload(
              sport.getBrand(), iconFile, smallIconsPath, new ImageServiceImpl.Size(smallIconsSize))
          .ifPresent(
              filename ->
                  sport.setUriSmallIcon(smallIconsPath.concat("/").concat(filename.getFilename())));
      imageService
          .upload(
              sport.getBrand(),
              iconFile,
              mediumIconsPath,
              new ImageServiceImpl.Size(mediumIconsSize))
          .ifPresent(
              filename ->
                  sport.setUriMediumIcon(
                      mediumIconsPath.concat("/").concat(filename.getFilename())));
      imageService
          .upload(
              sport.getBrand(), iconFile, largeIconsPath, new ImageServiceImpl.Size(largeIconsSize))
          .ifPresent(
              filename ->
                  sport.setUriLargeIcon(largeIconsPath.concat("/").concat(filename.getFilename())));
    }
  }

  public enum SportsImage {
    IMAGE("imageFile"),
    ICON("icon"),
    SVG_ICON("svgIcon"),
    UNKNOWN("UNKNOWN");

    private final String fileType;

    SportsImage(String fileType) {
      this.fileType = fileType;
    }

    public static SportsImage fromString(String fileType) {
      return Arrays.stream(values())
          .filter(e -> e.fileType.equalsIgnoreCase(fileType))
          .findAny()
          .orElse(UNKNOWN);
    }

    public static SportsImage[] validValues() {
      return new SportsImage[] {IMAGE, ICON, SVG_ICON};
    }

    public static String printFileTypes() {
      return String.format("%s, %s, %s", IMAGE.fileType, ICON.fileType, SVG_ICON.fileType);
    }
  }
}
