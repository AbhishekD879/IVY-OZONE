package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.entity.TimelineFileType;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Template;
import com.ladbrokescoral.oxygen.cms.api.exception.BadRequestException;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import com.ladbrokescoral.oxygen.cms.api.exception.SvgImageParseException;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.repository.TimelinePostPageRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.TimelineTemplateRepository;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import java.util.Optional;
import org.apache.commons.lang3.ObjectUtils;
import org.bson.types.ObjectId;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
public class TimelineTemplateService extends AbstractService<Template> {
  private final ImageService imageService;
  private final SvgImageParser imageParser;

  private final String timelineImagePath;

  private final TimelinePostPageRepository postRepository;

  public TimelineTemplateService(
      TimelineTemplateRepository repository,
      TimelinePostPageRepository postRepository,
      ImageService imageService,
      SvgImageParser imageParser,
      @Value("${images.timelineImages.path}") String timelineImagePath) {
    super(repository);
    this.postRepository = postRepository;
    this.imageService = imageService;
    this.imageParser = imageParser;
    this.timelineImagePath = timelineImagePath;
  }

  public Template uploadAndSetRightCornerImage(
      Template template, @ValidFileType("png") MultipartFile file) {
    template.setTopRightCornerImage(getUploadedImage(template, file));
    return save(template);
  }

  public Template uploadAndSetSvgImage(
      Template template, @ValidFileType("svg") MultipartFile file) {
    template.setTopRightCornerImage(getUploadedSvg(template, file));
    return save(template);
  }

  @Override
  public void delete(String id) {
    if (ObjectUtils.isEmpty(postRepository.findByTemplateId(new ObjectId(id)))) {
      super.delete(id);
    } else {
      throw new ValidationException("Couldn't remove template with present posts");
    }
  }

  public Template deleteImage(Template template, TimelineFileType timelineFileType) {
    if (timelineFileType == TimelineFileType.TOP_RIGHT_CORNER) {
      removeTopRightCornerImage(template);
    } else {
      removeHeaderIconImage(template);
    }

    return save(template);
  }

  private void removeHeaderIconImage(Template template) {
    template.setPostIconSvgId(null);
  }

  private void removeTopRightCornerImage(Template template) {
    if (!imageService.removeImage(
        template.getBrand(), template.getTopRightCornerImage().getFullPath())) {
      throw new FileUploadException();
    }
    template.setTopRightCornerImage(null);
  }

  private Filename getUploadedImage(Template template, MultipartFile file) {
    String message = " for template: " + template.getName();

    return imageService
        .upload(template.getBrand(), file, timelineImagePath)
        .orElseThrow(
            () ->
                new FileUploadException(
                    "Image uploading error for image: " + file.getOriginalFilename() + message));
  }

  private Filename getUploadedSvg(Template template, MultipartFile svg) {
    String message = " for template: " + template.getName();

    try {
      Optional<Svg> parsedSvg = imageParser.parse(svg);
      if (!parsedSvg.isPresent()) {
        throw new BadRequestException(
            "Svg parsing error for image: " + svg.getOriginalFilename() + message);
      }
    } catch (SvgImageParseException ex) {
      throw new BadRequestException(
          "Svg parsing error for image: " + svg.getOriginalFilename() + message);
    }

    return imageService
        .upload(template.getBrand(), svg, timelineImagePath)
        .orElseThrow(
            () ->
                new FileUploadException(
                    "Image uploading error for image: " + svg.getOriginalFilename() + message));
  }
}
