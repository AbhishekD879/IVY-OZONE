package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.EndPage;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.exception.SvgImageParseException;
import com.ladbrokescoral.oxygen.cms.api.repository.EndPageRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.QuestionEngineRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
@Slf4j
public class EndPageService extends AbstractService<EndPage> {
  private final ImageService imageService;
  private SvgImageParser svgImageParser;
  private final QuestionEngineRepository questionEngineRepository;
  private final MongoTemplate mongoTemplate;
  private final String path;

  public EndPageService(
      EndPageRepository repository,
      ImageService imageService,
      SvgImageParser svgImageParser,
      QuestionEngineRepository questionEngineRepository,
      MongoTemplate mongoTemplate,
      @Value("${images.endpage.svg}") String path) {
    super(repository);
    this.imageService = imageService;
    this.svgImageParser = svgImageParser;
    this.questionEngineRepository = questionEngineRepository;
    this.mongoTemplate = mongoTemplate;
    this.path = path;
  }

  @Override
  public EndPage update(EndPage existingEntity, EndPage updateEntity) {
    updateQuizzesEndPage(updateEntity);
    return super.update(existingEntity, updateEntity);
  }

  @Override
  public void delete(String id) {
    deleteQuizzesEndPage(id);
    super.delete(id);
  }

  public EndPage uploadBackground(String id, MultipartFile backgroundSvgImage) {
    EndPage endPage = findOne(id).orElseThrow(NotFoundException::new);

    parseSvgFile(backgroundSvgImage);
    Filename background = uploadFile(endPage.getBrand(), backgroundSvgImage);
    endPage.setBackgroundSvgImage(background);

    save(endPage);
    updateQuizzesEndPage(endPage);

    return endPage;
  }

  public void deleteBackground(String id) {
    EndPage endPage =
        findOne(id)
            .filter(page -> page.getBackgroundSvgImage() != null)
            .orElseThrow(NotFoundException::new);

    imageService.removeImage(endPage.getBrand(), endPage.getBackgroundSvgImage().getFullPath());

    save(endPage.setBackgroundSvgImage(null));

    updateQuizzesEndPage(endPage);
  }

  private Filename uploadFile(String brand, MultipartFile file) {
    return imageService.upload(brand, file, path).orElseThrow(FileUploadException::new);
  }

  private void parseSvgFile(MultipartFile svgFile) {
    String svg =
        svgImageParser.parse(svgFile).map(Svg::getSvg).orElseThrow(SvgImageParseException::new);

    log.info("Uploading svg file: '{}'", svg);
  }

  private void updateQuizzesEndPage(EndPage endPage) {
    questionEngineRepository
        .findByEndPageId(mongoTemplate, endPage.getId())
        .forEach(quiz -> questionEngineRepository.save(quiz.setEndPage(endPage)));
  }

  private void deleteQuizzesEndPage(String id) {
    questionEngineRepository
        .findByEndPageId(mongoTemplate, id)
        .forEach(quiz -> questionEngineRepository.save(quiz.setEndPage(null)));
  }
}
