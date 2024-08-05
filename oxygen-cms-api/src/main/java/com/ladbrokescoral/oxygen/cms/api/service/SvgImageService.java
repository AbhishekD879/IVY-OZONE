package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.SvgImage;
import com.ladbrokescoral.oxygen.cms.api.entity.SvgSprite;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.SvgImageRepository;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.ObjectUtils;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.multipart.MultipartFile;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;

@Component
@Slf4j
public class SvgImageService extends AbstractService<SvgImage> {

  private final SvgEntityService<SvgImage> svgEntityService;
  private final String svgImagesBasePath;

  private final SvgImageRepository svgImageRepository;
  private final SvgImageParser svgImageParser;
  private static final String SYMBOL_TAG = "symbol";
  private static final String ID_ATTRIBUTE = "id";

  @Autowired
  public SvgImageService(
      SvgImageRepository repository,
      SvgEntityService<SvgImage> svgEntityService,
      @Value("${images.svg.path}") String svgImagesBasePath,
      SvgImageParser svgImageParser) {
    super(repository);
    this.svgImageRepository = repository;
    this.svgEntityService = svgEntityService;
    this.svgImagesBasePath = svgImagesBasePath;
    this.svgImageParser = svgImageParser;
  }

  public List<SvgImage> searchByBrand(String brand, String svgId, Boolean isActive) {
    List<SvgImage> images = repository.findByBrand(brand);

    if (Objects.nonNull(svgId) || Objects.nonNull(isActive)) {
      Stream<SvgImage> svgStream = images.stream();

      if (Objects.nonNull(isActive)) {
        svgStream = svgStream.filter(i -> i.isActive() == isActive);
      }

      if (Objects.nonNull(svgId) && svgId.length() > 0) {
        svgStream = svgStream.filter(i -> i.getSvgId().toLowerCase().contains(svgId.toLowerCase()));
      }

      images = svgStream.collect(Collectors.toList());
    }

    return images;
  }

  public List<SvgImage> findAllByBrandAndSprite(String brand, String sprite) {
    return svgImageRepository.findAllByBrandAndSprite(brand, sprite);
  }

  public SvgImage createSvgImage(SvgImage svgImage, MultipartFile file, String svgIdPrefix) {
    if (StringUtils.isBlank(svgImage.getSprite())) {
      svgImage.setSprite(SvgSprite.ADDITIONAL.getSpriteName());
    }
    log.debug(
        "Creating svg image with id {} with size {} from file {}",
        svgImage.getSvgId(),
        file.getSize(),
        file.getOriginalFilename());
    svgEntityService.attachSvgImage(
        svgImage, svgImage.getSvgId(), file, svgImagesBasePath, svgIdPrefix);
    return svgImage;
  }

  public SvgImage createSvgImage(SvgImage svgImage, MultipartFile file) {
    // TODO: rework it after IM is release for both brands
    return createSvgImage(svgImage, file, "#");
  }

  @Override
  public SvgImage update(SvgImage existingEntity, SvgImage updateEntity) {
    return save(merge(existingEntity, updateEntity));
  }

  public SvgImage replaceSvgImage(
      String id, @ValidFileType("svg") MultipartFile file, SvgImage svgEntity) {
    SvgImage svg = findOne(id).orElseThrow(NotFoundException::new);
    String svgId = svg.getSvgId();
    if (Objects.nonNull(file)) {
      svgEntityService.removeSvgImage(svg);
      Optional<SvgImage> attachedImage =
          svgEntityService.attachSvgImage(svg, svgId, file, svgImagesBasePath, "");
      if (!attachedImage.isPresent()) {
        log.warn("Failed to attach file to svg {}", svgId);
        svg = merge(svg, svgEntity);
      }

      return attachedImage.map(e -> merge(e, svgEntity)).orElse(svg);
    }

    return merge(svg, svgEntity);
  }

  public Optional<SvgImage> removeSvgImage(String id) {
    return findOne(id).flatMap(svgEntityService::removeSvgImage);
  }

  public List<String> getSprites(String brand) {
    return Stream.of(SvgSprite.values()).map(SvgSprite::getSpriteName).collect(Collectors.toList());
  }

  private SvgImage merge(SvgImage existingEntity, SvgImage updateEntity) {

    updateEntity.setSvg(StringUtils.defaultIfBlank(updateEntity.getSvg(), existingEntity.getSvg()));
    if (Objects.nonNull(updateEntity.getSvgId())
        && !updateEntity.getSvgId().equals(existingEntity.getSvgId())
        && (Objects.nonNull(updateEntity.getSvg()) || Objects.nonNull(existingEntity.getSvg()))) {
      String newId = updateEntity.getSvgId();
      String svgContent =
          Objects.nonNull(updateEntity.getSvg()) ? updateEntity.getSvg() : existingEntity.getSvg();
      // checking and replace svgId vs symbol id using it's outer context
      // without outer context "svg-id1" might match "svg-id11" and after replace it becomes
      // svg-id111
      String updatedSvgContent = updateSvgId(newId, svgContent);
      updateEntity.setSvg(updatedSvgContent);
    }

    updateEntity.setSvgId(
        StringUtils.defaultIfBlank(updateEntity.getSvgId(), existingEntity.getSvgId()));
    updateEntity.setSvgFilename(
        ObjectUtils.defaultIfNull(updateEntity.getSvgFilename(), existingEntity.getSvgFilename()));
    updateEntity.setSprite(
        StringUtils.defaultIfBlank(updateEntity.getSprite(), existingEntity.getSprite()));

    return updateEntity;
  }

  public String updateSvgId(String newId, String svgContent) {
    try {
      Document document = svgImageParser.convertStringToDocument(svgContent);
      Node symbolNode = svgImageParser.getFirstNodeByTagName(document, SYMBOL_TAG);
      ((Element) symbolNode).setAttribute(ID_ATTRIBUTE, newId);
      symbolNode.normalize();
      return svgImageParser.toString(symbolNode);
    } catch (Exception exception) {
      log.error("SVG Id updation parsing error");
    }
    return svgContent;
  }
}
