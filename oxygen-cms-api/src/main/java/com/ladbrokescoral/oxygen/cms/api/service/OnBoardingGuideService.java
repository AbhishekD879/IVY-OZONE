package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.OnBoardingGuide;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.entity.SvgFilename;
import com.ladbrokescoral.oxygen.cms.api.repository.OnBoardingGuideRepository;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import com.ladbrokescoral.oxygen.cms.util.ImageUtil;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.multipart.MultipartFile;

@Validated
@Slf4j
@Service
public class OnBoardingGuideService extends SortableService<OnBoardingGuide> {

  private final ImageService imageService;
  private final String relativePath;

  @Autowired
  public OnBoardingGuideService(
      OnBoardingGuideRepository repository,
      ImageService imageService,
      @Value("${images.guide.path}") String pathToGuide) {
    super(repository);
    this.imageService = imageService;
    this.relativePath = pathToGuide;
  }

  public void attachSvgImage(OnBoardingGuide entity, @ValidFileType("svg") MultipartFile file) {
    Filename filename =
        imageService
            .upload(entity.getBrand(), file, relativePath)
            .orElseThrow(
                () -> new IllegalStateException("An error occurred during image uploading"));

    Svg svg = new Svg();
    svg.setValue(file.getOriginalFilename());
    SvgFilename svgFilename = ImageUtil.getSvgFilename(filename, relativePath, svg);
    entity.setGuidePath(PathUtil.normalizedPath(svgFilename.getPath(), svgFilename.getFilename()));
    entity.setSvgFilename(svgFilename);
  }

  public void removeSvgImage(OnBoardingGuide entity) {
    SvgFilename svg = entity.getSvgFilename();
    if (svg != null
        && StringUtils.isNotBlank(svg.getPath())
        && StringUtils.isNotBlank(svg.getFilename())) {
      String imagePath = PathUtil.normalizedPath(svg.getPath(), svg.getFilename()).substring(1);
      Boolean isDeleted = imageService.removeImage(entity.getBrand(), imagePath);
      log.info("File {} removal status : {}", imagePath, isDeleted);
      entity.setSvgFilename(null);
      entity.setGuidePath(null);
    }
  }
}
