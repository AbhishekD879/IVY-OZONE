package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.Quiz;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.SplashPage;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.SplashPageImageType;
import com.ladbrokescoral.oxygen.cms.api.exception.BadRequestException;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.exception.SvgImageParseException;
import com.ladbrokescoral.oxygen.cms.api.repository.QuestionEngineRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.QuizSplashPageRepository;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
public class QuizSplashPageService extends AbstractService<SplashPage> {

  private final ImageService imageService;
  private SvgImageParser svgImageParser;
  private final QuestionEngineRepository questionEngineRepository;
  private final MongoTemplate mongoTemplate;
  private final String path;

  public QuizSplashPageService(
      QuizSplashPageRepository repository,
      ImageService imageService,
      SvgImageParser svgImageParser,
      QuestionEngineRepository questionEngineRepository,
      MongoTemplate mongoTemplate,
      @Value("${images.splashpage.svg}") String path) {
    super(repository);
    this.imageService = imageService;
    this.svgImageParser = svgImageParser;
    this.questionEngineRepository = questionEngineRepository;
    this.mongoTemplate = mongoTemplate;
    this.path = path;
  }

  public SplashPage handleFileUploading(
      String id,
      boolean isSvg,
      MultipartFile logoFile,
      MultipartFile backgroundFile,
      MultipartFile footer) {
    SplashPage splashPage = findOne(id).orElseThrow(NotFoundException::new);
    if (isSvg) {
      handleBackground(backgroundFile, splashPage);
      handleLogo(logoFile, splashPage);
      handleFooter(footer, splashPage);
    }
    save(splashPage);
    updateQuizzesSplashPages(splashPage);
    return splashPage;
  }

  public SplashPage handleFileDelete(String id, String imageType) {
    SplashPage splashPage = findOne(id).orElseThrow(NotFoundException::new);

    String svgPath;

    switch (SplashPageImageType.valueOf(imageType)) {
      case LOGO:
        svgPath = splashPage.logoSvgPath();
        splashPage.clearLogoSvg();
        break;
      case BACKGROUND:
        svgPath = splashPage.backgroundSvgPath();
        splashPage.clearBackgroundSvg();
        break;
      case FOOTER:
        svgPath = splashPage.footerSvgPath();
        splashPage.clearFooterSvg();
        break;
      default:
        throw new UnsupportedOperationException("Unknown image type: " + imageType);
    }

    save(splashPage);
    updateQuizzesSplashPages(splashPage);
    imageService.removeImage(splashPage.getBrand(), svgPath);
    return splashPage;
  }

  public void updateQuizzesSplashPages(SplashPage splashPage) {
    List<Quiz> quizzesBySplashPageId =
        questionEngineRepository.findBySplashPageId(mongoTemplate, splashPage.getId());
    quizzesBySplashPageId.forEach(
        quiz -> {
          quiz.setSplashPage(splashPage);
          questionEngineRepository.save(quiz);
        });
  }

  public void deleteQuizzesSplashPages(String id) {
    questionEngineRepository
        .findBySplashPageId(mongoTemplate, id)
        .forEach(quiz -> questionEngineRepository.save(quiz.setSplashPage(null)));
  }

  public void deleteAllFiles(String id) {
    SplashPage splashPage = findOne(id).orElseThrow(NotFoundException::new);

    String logoSvgPath = splashPage.logoSvgPath();
    String backgroundSvgPath = splashPage.backgroundSvgPath();

    if (!logoSvgPath.isEmpty()) {
      imageService.removeImage(splashPage.getBrand(), logoSvgPath);
    }
    if (!backgroundSvgPath.isEmpty()) {
      imageService.removeImage(splashPage.getBrand(), backgroundSvgPath);
    }
  }

  private void handleFooter(MultipartFile footerFile, SplashPage splashPage) {
    if (footerFile != null) {
      Filename footer = getUploadedSvg(splashPage.getBrand(), footerFile);
      splashPage.setFooterSvgFile(footer);
      splashPage.setFooterSvgFilename(footer.getOriginalname());
    }
  }

  private void handleLogo(MultipartFile logoFile, SplashPage splashPage) {
    if (logoFile != null) {
      Filename logo = getUploadedSvg(splashPage.getBrand(), logoFile);
      splashPage.setLogoSvgFile(logo);
      splashPage.setLogoSvgFilename(logo.getOriginalname());
    }
  }

  private void handleBackground(MultipartFile backgroundFile, SplashPage splashPage) {
    if (backgroundFile != null) {
      Filename background = getUploadedSvg(splashPage.getBrand(), backgroundFile);
      splashPage.setBackgroundSvgFile(background);
      splashPage.setBackgroundSvgFilename(background.getOriginalname());
    }
  }

  private Filename getUploadedSvg(String brand, MultipartFile svg) {
    try {
      Optional<Svg> parsedSvg = svgImageParser.parse(svg);
      if (!parsedSvg.isPresent()) {
        throw new BadRequestException("Svg parsing error for image: " + svg.getOriginalFilename());
      }
    } catch (SvgImageParseException ex) {
      throw new BadRequestException("Svg parsing error for image: " + svg.getOriginalFilename());
    }

    return imageService
        .upload(brand, svg, path)
        .orElseThrow(
            () ->
                new FileUploadException(
                    "Image uploading error for image: " + svg.getOriginalFilename()));
  }
}
