package com.ladbrokescoral.oxygen.cms.util;

import static com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl.Size;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.entity.SvgFilename;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.LargeImageAbstractMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.MediumImageAbstractMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.SmallImageAbstractMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.SvgAbstractMenu;
import java.util.Arrays;

public class ImageUtil {

  private ImageUtil() {}

  private static final String DEFAULT_EXT = "jpg";

  public static String getImageExtension(String fileName) {
    String[] split = fileName.split("\\.");
    return split.length > 0 ? split[split.length - 1] : DEFAULT_EXT;
  }

  public static boolean isValidType(String type, String... allowedTypes) {
    return Arrays.stream(allowedTypes).anyMatch(el -> el.equalsIgnoreCase(type));
  }

  public static <T extends SvgAbstractMenu> T setSvgFields(
      T entity, Filename filename, String svgPath, Svg svg) {
    SvgFilename svgFilename = getSvgFilename(filename, svgPath, svg);

    entity.setSvgFilename(svgFilename);
    entity.setSvg(svg.getSvg());
    entity.setSvgId(svg.getId());

    return entity;
  }

  public static SvgFilename getSvgFilename(Filename filename, String svgPath, Svg svg) {
    SvgFilename svgFilename = new SvgFilename();
    svgFilename.setFilename(filename.getFilename());
    svgFilename.setPath(svgPath);
    svgFilename.setSize(Integer.valueOf(filename.getSize()));
    svgFilename.setOriginalname(svg.getValue());
    svgFilename.setFiletype("image/svg+xml");
    return svgFilename;
  }

  public static <T extends SvgAbstractMenu> T removeSvgFields(T entity) {
    entity.setSvg(null);
    entity.setSvgFilename(null);
    entity.setSvgId(null);

    return entity;
  }

  public static <T extends SmallImageAbstractMenu> T populateSmallFields(
      T entity, Size size, String uri) {
    entity.setHeightSmall(size.getHeight());
    entity.setWidthSmall(size.getWidth());
    entity.setUriSmall(uri);

    return entity;
  }

  public static <T extends SmallImageAbstractMenu> T removeSmallFields(T entity) {
    entity.setHeightSmall(null);
    entity.setWidthSmall(null);
    entity.setUriSmall(null);

    return entity;
  }

  public static <T extends MediumImageAbstractMenu> T populateMediumFields(
      T entity, Size size, String uri) {
    entity.setHeightMedium(size.getHeight());
    entity.setWidthMedium(size.getWidth());
    entity.setUriMedium(uri);

    return entity;
  }

  public static <T extends MediumImageAbstractMenu> T removeMediumFields(T entity) {
    entity.setHeightMedium(null);
    entity.setWidthMedium(null);
    entity.setUriMedium(null);

    return entity;
  }

  public static <T extends LargeImageAbstractMenu> T populateLargeFields(
      T entity, Size size, String uri) {
    entity.setHeightLarge(size.getHeight());
    entity.setWidthLarge(size.getWidth());
    entity.setUriLarge(uri);

    return entity;
  }

  public static <T extends LargeImageAbstractMenu> T removeLargeFields(T entity) {
    entity.setHeightLarge(null);
    entity.setWidthLarge(null);
    entity.setUriLarge(null);

    return entity;
  }
}
