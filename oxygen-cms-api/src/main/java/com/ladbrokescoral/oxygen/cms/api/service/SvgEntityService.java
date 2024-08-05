package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.SvgAbstractMenu;
import com.ladbrokescoral.oxygen.cms.util.ImageUtil;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

/**
 * this service provides methods for working with svg image
 *
 * @param <T>
 */
@Slf4j
@Service
public class SvgEntityService<T extends SvgAbstractMenu> {

  private final ImageService imageService;
  private final SvgImageParser svgImageParser;

  public SvgEntityService(ImageService imageService, SvgImageParser svgImageParser) {
    this.imageService = imageService;
    this.svgImageParser = svgImageParser;
  }

  public Optional<T> attachSvgImage(T menu, MultipartFile file, String svgMenuPath) {
    return attachSvgImage(menu, null, file, svgMenuPath, "#");
  }

  public Optional<T> attachSvgImage(
      T menu, MultipartFile file, String svgMenuPath, String svgIdPrefix) {
    return attachSvgImage(menu, null, file, svgMenuPath, svgIdPrefix);
  }

  public Optional<T> attachSvgImage(
      T menu, String overrideSvgId, MultipartFile file, String svgMenuPath, String svgIdPrefix) {
    Optional<Svg> svgOptional = svgImageParser.parse(overrideSvgId, file, svgIdPrefix);
    if (!svgOptional.isPresent()) {
      return Optional.empty();
    }

    Optional<Filename> uploaded = imageService.upload(menu.getBrand(), file, svgMenuPath);
    return uploaded.map(
        uploadedImage ->
            ImageUtil.setSvgFields(menu, uploadedImage, svgMenuPath, svgOptional.get()));
  }

  public Optional<T> removeSvgImage(T menu) {
    return Optional.ofNullable(menu.getSvgFilename())
        .map(
            svgFilename -> {
              String imagePath =
                  PathUtil.normalizedPath(svgFilename.getPath(), svgFilename.getFilename());
              Boolean isDeleted = imageService.removeImage(menu.getBrand(), imagePath);
              log.info("File {} removal status : {}", imagePath, isDeleted);

              return ImageUtil.removeSvgFields(menu);
            });
  }
}
