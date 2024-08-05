package com.ladbrokescoral.oxygen.cms.api.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.dataformat.csv.CsvMapper;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.QuestionSummaryReport;
import com.ladbrokescoral.oxygen.cms.api.entity.QuizPopupSetting;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.Question;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.QuestionDetails;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.Quiz;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.Upsell;
import com.ladbrokescoral.oxygen.cms.api.exception.BadRequestException;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.exception.SvgImageParseException;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.repository.BigQueryQuestionEngineRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.QuestionEngineRepository;
import java.io.IOException;
import java.text.DecimalFormat;
import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.function.Function;
import java.util.stream.Collectors;
import org.apache.commons.lang3.ObjectUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
public class QuestionEngineService extends AbstractService<Quiz> {
  private static final DecimalFormat ENTRIES_PERCENT_FORMAT = new DecimalFormat("#.0");

  private final QuestionEngineRepository questionEngineRepository;
  private final ImageService imageService;
  private final SvgImageParser svgImageParser;
  private final String path;
  private final String questionEngineImages;
  private final QuizPopupSettingService quizPopupSettingService;
  private final BigQueryQuestionEngineRepository bigQueryQuestionEngineRepository;
  private final CsvMapper csvMapper = new CsvMapper();

  public QuestionEngineService(
      QuestionEngineRepository repository,
      ImageService imageService,
      SvgImageParser svgImageParser,
      @Value("${images.quizUpsellFallback.path}") String path,
      @Value("${images.questionEngineImages.path}") String questionEngineImages,
      QuizPopupSettingService quizPopupSettingService,
      BigQueryQuestionEngineRepository bigQueryQuestionEngineRepository) {
    super(repository);
    this.questionEngineRepository = repository;
    this.imageService = imageService;
    this.svgImageParser = svgImageParser;
    this.path = path;
    this.questionEngineImages = questionEngineImages;
    this.quizPopupSettingService = quizPopupSettingService;
    this.bigQueryQuestionEngineRepository = bigQueryQuestionEngineRepository;
  }

  public List<Quiz> getQuizzesByBrandAndSourceId(String brand, String sourceId) {
    return questionEngineRepository.findByBrandAndSourceId(brand, sourceId);
  }

  public Question getQuestionTree(String quizId, String questionId) {
    return findOne(quizId)
        .flatMap(quiz -> find(quiz.getFirstQuestion(), questionId))
        .orElseThrow(NotFoundException::new);
  }

  @Override
  public <S extends Quiz> S save(S entity) {
    validate(entity, entity.getId());

    return super.save(entity);
  }

  @Override
  public Quiz update(Quiz existingEntity, Quiz updateEntity) {
    if (isStartedAndActive(existingEntity)
        && !existingEntity.getDisplayFrom().equals(updateEntity.getDisplayFrom())) {
      throw new ValidationException(
          "You cannot update Quiz Display From date because it has already been started and shown to customers");
    }
    validate(updateEntity, updateEntity.getId());

    Quiz updatedQuiz = super.update(existingEntity, updateEntity);

    if (!existingEntity.getDisplayTo().equals(updateEntity.getDisplayTo())) {
      QuizPopupSetting quizPopupSetting =
          quizPopupSettingService.getByBrand(updatedQuiz.getBrand());

      quizPopupSettingService.update(
          quizPopupSetting, quizPopupSetting.setExpirationDate(updatedQuiz.getDisplayTo()));
    }
    return updatedQuiz;
  }

  public Quiz uploadFallbackImage(String id, MultipartFile fallbackImage) {
    Quiz quiz =
        findOne(id)
            .map(q -> q.getUpsell() == null ? q.setUpsell(new Upsell()) : q)
            .orElseThrow(NotFoundException::new);

    Optional<Filename> file = imageService.upload(quiz.getBrand(), fallbackImage, path);

    if (file.isPresent()) {
      quiz.getUpsell().setFallbackImage(file.get());
    } else {
      throw new FileUploadException();
    }
    return save(quiz);
  }

  public Quiz deleteFallbackImage(String id) {
    Quiz quiz =
        findOne(id)
            .filter(q -> q.getUpsell() != null)
            .filter(q -> q.getUpsell().getFallbackImage() != null)
            .orElseThrow(NotFoundException::new);

    if (!imageService.removeImage(
        quiz.getBrand(), quiz.getUpsell().getFallbackImage().getFullPath())) {
      throw new FileUploadException();
    }
    quiz.getUpsell().setFallbackImage(null);
    return save(quiz);
  }

  public Quiz uploadQuestionDetailsImages(
      String brand,
      String quizId,
      String questionId,
      MultipartFile homeTeamKit,
      MultipartFile awayTeamKit,
      MultipartFile channel) {

    Quiz quiz = findOne(quizId).orElseThrow(NotFoundException::new);

    Question questionTree =
        find(quiz.getFirstQuestion(), questionId).orElseThrow(NotFoundException::new);
    QuestionDetails questionDetails = questionTree.getQuestionDetails();

    if (homeTeamKit != null) {
      questionDetails.setHomeTeamSvg(getUploadedSvg(brand, questionTree, homeTeamKit));
    }
    if (awayTeamKit != null) {
      questionDetails.setAwayTeamSvg(getUploadedSvg(brand, questionTree, awayTeamKit));
    }
    if (channel != null) {
      questionDetails.setChannelSvg(getUploadedSvg(brand, questionTree, channel));
    }

    save(quiz);
    return quiz;
  }

  public Quiz uploadQuizLogoImage(String brand, String quizId, MultipartFile quizLogo) {
    Quiz quiz = findOne(quizId).orElseThrow(NotFoundException::new);
    quiz.setQuizLogoSvg(getUploadedSvg(brand, quizLogo));
    save(quiz);
    return quiz;
  }

  public Quiz deleteQuizLogoImage(String quizId) {
    Quiz quiz = findOne(quizId).orElseThrow(NotFoundException::new);
    quiz.setQuizLogoSvg(new Filename());
    save(quiz);
    return quiz;
  }

  public Quiz uploadQuizBackgroundImage(String brand, String quizId, MultipartFile quizBackground) {
    Quiz quiz = findOne(quizId).orElseThrow(NotFoundException::new);
    quiz.setQuizBackgroundSvg(getUploadedSvg(brand, quizBackground));
    save(quiz);
    return quiz;
  }

  public Quiz deleteQuizBackgroundImage(String quizId) {
    Quiz quiz = findOne(quizId).orElseThrow(NotFoundException::new);
    quiz.setQuizBackgroundSvg(new Filename());
    save(quiz);
    return quiz;
  }

  public Quiz uploadDefaultQuestionDetailsImages(
      String brand,
      String quizId,
      MultipartFile homeTeamKit,
      MultipartFile awayTeamKit,
      MultipartFile channel) {
    Quiz quiz = findOne(quizId).orElseThrow(NotFoundException::new);

    QuestionDetails defaultQuestionsDetails = quiz.getDefaultQuestionsDetails();
    if (homeTeamKit != null) {
      defaultQuestionsDetails.setHomeTeamSvg(getUploadedSvg(brand, homeTeamKit));
    }
    if (awayTeamKit != null) {
      defaultQuestionsDetails.setAwayTeamSvg(getUploadedSvg(brand, awayTeamKit));
    }
    if (channel != null) {
      defaultQuestionsDetails.setChannelSvg(getUploadedSvg(brand, channel));
    }

    save(quiz);
    return quiz;
  }

  public Quiz deleteDefaultQuestionDetailsImages(String quizId, String teamType) {
    Quiz quiz = findOne(quizId).orElseThrow(NotFoundException::new);

    if ("home".equals(teamType)) {
      quiz.getDefaultQuestionsDetails().setHomeTeamSvg(new Filename());
    } else if ("away".equals(teamType)) {
      quiz.getDefaultQuestionsDetails().setAwayTeamSvg(new Filename());
    } else if ("channel".equals(teamType)) {
      quiz.getDefaultQuestionsDetails().setChannelSvg(new Filename());
    }
    save(quiz);
    return quiz;
  }

  public Quiz uploadPopupIconImage(
      String brand, String quizId, String iconType, MultipartFile file) {
    Quiz quiz = findOne(quizId).orElseThrow(NotFoundException::new);

    return updateQuizWithPopup(iconType, quiz, getUploadedSvg(brand, file));
  }

  public Quiz deletePopupIconImage(String quizId, String iconType) {
    Quiz quiz = findOne(quizId).orElseThrow(NotFoundException::new);
    return updateQuizWithPopup(iconType, quiz, new Filename());
  }

  @Cacheable(cacheNames = "questions-summary-report")
  public QuestionEngineCsvReport generateQuestionsSummaryCsvReport(String quizId)
      throws IOException {
    if (!repository.existsById(quizId)) {
      throw new NotFoundException(String.format("Quiz with id '%s' not found", quizId));
    }

    List<QuestionSummaryReport> questionSummaries =
        bigQueryQuestionEngineRepository.findQuestionSummariesByQuizId(quizId);
    Map<Integer, Integer> questionToTotalNumberOfEntries =
        questionSummaries.stream()
            .collect(
                Collectors.toMap(
                    QuestionSummaryReport::getQuestionNumber,
                    QuestionSummaryReport::getNumberOfEntries,
                    Integer::sum));

    questionSummaries.forEach(
        questionSummary ->
            questionSummary
                .setTotalNumberOfEntries(
                    questionToTotalNumberOfEntries.get(questionSummary.getQuestionNumber()))
                .setPercentOfTotalEntries(
                    calculateEntriesPercentage(
                        questionSummary.getNumberOfEntries(),
                        questionToTotalNumberOfEntries.get(questionSummary.getQuestionNumber()))));

    String csvData =
        csvMapper
            .writer()
            .with(
                csvMapper
                    .typedSchemaFor(new TypeReference<QuestionSummaryReport>() {})
                    .withUseHeader(true))
            .writeValueAsString(questionSummaries);

    return new QuestionEngineCsvReport(csvData, Instant.now());
  }

  private Quiz updateQuizWithPopup(String iconType, Quiz quiz, Filename uploadedSvg) {
    if ("submit".equals(iconType)) {
      quiz.getSubmitPopup().setIcon(uploadedSvg);
    } else if ("exit".equals(iconType)) {
      quiz.getExitPopup().setIcon(uploadedSvg);
    }
    return save(quiz);
  }

  private boolean isStartedAndActive(Quiz existingEntity) {
    return existingEntity.isActive() && existingEntity.getDisplayFrom().isBefore(Instant.now());
  }

  private Filename getUploadedSvg(String brand, MultipartFile svg) {
    return getUploadedSvg(brand, null, svg);
  }

  private Filename getUploadedSvg(String brand, Question questionTree, MultipartFile svg) {
    String questionMessage = questionTree != null ? " for question: " + questionTree.getText() : "";

    try {
      Optional<Svg> parsedSvg = svgImageParser.parse(svg);
      if (!parsedSvg.isPresent()) {
        throw new BadRequestException(
            "Svg parsing error for image: " + svg.getOriginalFilename() + questionMessage);
      }
    } catch (SvgImageParseException ex) {
      throw new BadRequestException(
          "Svg parsing error for image: " + svg.getOriginalFilename() + questionMessage);
    }

    return imageService
        .upload(brand, svg, questionEngineImages)
        .orElseThrow(
            () ->
                new FileUploadException(
                    "Image uploading error for image: "
                        + svg.getOriginalFilename()
                        + questionMessage));
  }

  private void validate(Quiz entity, String id) {
    if (questionEngineRepository
        .existsBySourceIdAndIdIsNotAndBrandAndActiveIsTrueAndDisplayFromIsLessThanAndDisplayToIsGreaterThan(
            entity.getSourceId(),
            id,
            entity.getBrand(),
            entity.getDisplayTo(),
            entity.getDisplayFrom())) {
      throw new ValidationException(
          "Active quiz with this source id is already exist. "
              + "Source id has to be unique and not overlap date range [display from - display to]");
    }
    if (entity.getUpsell() != null) {
      validateUpsell(entity.getUpsell());
    }

    if (entity.isActive() && entity.getFirstQuestion() != null && validateEmptyTexts(entity)) {
      throw new ValidationException(
          "Cannot save quiz. "
              + "For an active quiz all questions must have \"text\" and option \"text\" fields filled");
    }
  }

  private boolean validateEmptyTexts(Quiz entity) {
    return entity
        .getFirstQuestion()
        .flatten()
        .anyMatch(
            question ->
                ObjectUtils.isEmpty(question.getText())
                    || question.getAnswers().stream()
                        .anyMatch(answer -> ObjectUtils.isEmpty(answer.getText())));
  }

  private void validateUpsell(Upsell upsell) {
    if (ObjectUtils.isNotEmpty(upsell.getOptions())) {
      upsell
          .getOptions()
          .forEach(
              (questionIdPair, selectionId) -> {
                String[] ids = questionIdPair.split(";");

                if (ids.length < 2) {
                  throw new ValidationException(
                      "upsell.options keys must be in a form of \"question-id-1;question-id-2\" and so on");
                }
              });
    }
  }

  private static Optional<Question> find(Question question, String questionId) {
    if (question.getId().equals(questionId)) {
      return Optional.of(question);
    }
    return question.getAnswers().stream()
        .map(question::getNextQuestion)
        .filter(Objects::nonNull)
        .map(nextQuestion -> find(nextQuestion, questionId))
        .map(maybeQuestion -> maybeQuestion.filter(q -> q.getId().equals(questionId)))
        .filter(Optional::isPresent)
        .findFirst()
        .flatMap(Function.identity());
  }

  private String calculateEntriesPercentage(double entries, double totalEntries) {
    return ENTRIES_PERCENT_FORMAT.format(entries / totalEntries * 100.0);
  }
}
