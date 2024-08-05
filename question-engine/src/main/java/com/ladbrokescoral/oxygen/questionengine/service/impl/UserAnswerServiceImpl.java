package com.ladbrokescoral.oxygen.questionengine.service.impl;

import com.ladbrokescoral.oxygen.questionengine.crm.CrmService;
import com.ladbrokescoral.oxygen.questionengine.dto.AbstractQuestionDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.AnswerDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuestionDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuizDto;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.QuizSubmitDto;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.UserAnswerDto;
import com.ladbrokescoral.oxygen.questionengine.exception.NotFoundException;
import com.ladbrokescoral.oxygen.questionengine.exception.QuizSubmissionException;
import com.ladbrokescoral.oxygen.questionengine.model.UserAnswer;
import com.ladbrokescoral.oxygen.questionengine.model.cms.PredefinedAnswer;
import com.ladbrokescoral.oxygen.questionengine.repository.UserAnswerRepository;
import com.ladbrokescoral.oxygen.questionengine.service.QuizRewardService;
import com.ladbrokescoral.oxygen.questionengine.service.QuizService;
import com.ladbrokescoral.oxygen.questionengine.service.UserAnswerService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.Collection;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class UserAnswerServiceImpl implements UserAnswerService {
    private final QuizService quizService;
    private final UserAnswerRepository userAnswerRepository;
    private final ModelMapper modelMapper;
    private final QuizRewardService rewardService;
    private final CrmService crmService;
    private static final String REWARD_ERROR_CODE = "ER000";

    @Override
    public Optional<UserAnswerDto> findById(UserAnswer.Id id) {
        return userAnswerRepository
                .findById(id)
                .map(userAnswer -> modelMapper.map(userAnswer, UserAnswerDto.class));
    }

    @Override
    public UserAnswerDto getById(UserAnswer.Id id) {
        UserAnswer userAnswer = userAnswerRepository.findById(id).orElseThrow(() -> new NotFoundException("No UserAnswer with id '%s' found", id));

        return modelMapper.map(userAnswer, UserAnswerDto.class);
    }


    @Override
    public UserAnswerDto save(QuizSubmitDto quizSubmitDto) {
        log.info("UserAnswer save method starts {} ", quizSubmitDto);
        if (!isDoNotShowAgainAnswer(quizSubmitDto)) {
            validateQuizSubmission(quizSubmitDto);
        }
        Instant now = Instant.now();
        UserAnswer answer = modelMapper.map(quizSubmitDto, UserAnswer.class)
                .setCreatedDate(now)
                .setModifiedDate(now)
                .setUsernameSourceId(quizSubmitDto.getUsername() + quizSubmitDto.getSourceId());
        UserAnswer savedAnswer = userAnswerRepository.save(answer);
        UserAnswerDto userAnswerDto = modelMapper.map(savedAnswer, UserAnswerDto.class);
        String awardStatus = crmService.getAward(quizSubmitDto);
        log.info("CRM Award-API awardFlag::: {}", awardStatus);
        userAnswerDto.setRewardStatus(awardStatus);
        if (!isDoNotShowAgainAnswer(quizSubmitDto)) {
            rewardService.assignQuizReward(quizSubmitDto.getSourceId());
        }
        return userAnswerDto;
    }

    private boolean isDoNotShowAgainAnswer(QuizSubmitDto quizSubmitDto) {
        return quizSubmitDto.getQuestionIdToAnswerId().containsKey(PredefinedAnswer.DO_NOT_SHOW_AGAIN.name());
    }

    @Override
    public List<UserAnswer> findByQuizIdOrderByCreatedDateDesc(String quizId) {
        return userAnswerRepository.findByQuizIdOrderByCreatedDateDesc(quizId);
    }

    private void validateQuizSubmission(QuizSubmitDto submitModel) {
        Optional<QuizDto> live = quizService.findLiveQuiz(submitModel.getSourceId());

        if (!live.isPresent() || !live.get().getId().equals(submitModel.getQuizId())) {
            throw new QuizSubmissionException("You are trying to submit quiz that is no longer in live");
        }

        Optional<UserAnswer> userAnswer = findUserAnswer(live.get(), submitModel.getUsername());
        boolean missedDeadline = isMissedDeadline(live.get().getEntryDeadline());

        if (!userAnswer.isPresent() && missedDeadline) {
            throw new QuizSubmissionException("Sorry, deadline for quiz submission is over");
        }

        if (userAnswer.isPresent()) {
            throw new QuizSubmissionException("Quiz has already been submitted", modelMapper.map(userAnswer, UserAnswerDto.class));
        }

        if (!questionsToAnswersIdsMatch(live.get(), submitModel)) {
            throw new QuizSubmissionException("Submitted answers do not match to the ones configured in CMS", modelMapper.map(userAnswer, UserAnswerDto.class));
        }
    }

    private boolean isMissedDeadline(Instant deadline) {
        return Instant.now().isAfter(deadline);
    }

    private Optional<UserAnswer> findUserAnswer(QuizDto quiz, String username) {
        return findUserAnswers(quiz, username);
    }

    private Optional<UserAnswer> findUserAnswers(QuizDto quiz, String username) {
        return userAnswerRepository.findById(new UserAnswer.Id(quiz.getId(), username));
    }

    private boolean questionsToAnswersIdsMatch(QuizDto quizDto, QuizSubmitDto submission) {
        List<QuestionDto> questions = quizDto.getFirstQuestion().flatten().toList();
        boolean hasSameSize = questions.size() == submission.getQuestionIdToAnswerId().size();

        return hasSameSize && containsAllQuestions(submission, questions) && answersIdsMatch(submission, questions);
    }

    private boolean containsAllQuestions(QuizSubmitDto submission, List<QuestionDto> questions) {
        return questions
                .stream()
                .map(AbstractQuestionDto::getId)
                .allMatch(questionId -> submission.getQuestionIdToAnswerId().containsKey(questionId));
    }

    private boolean answersIdsMatch(QuizSubmitDto submission, List<QuestionDto> questions) {
        List<String> answersIds = questions
                .stream()
                .map(AbstractQuestionDto::getAnswers)
                .flatMap(List::stream)
                .map(AnswerDto::getId)
                .toList();

        return submission.getQuestionIdToAnswerId().values()
                .stream()
                .flatMap(Collection::stream)
                .allMatch(answersIds::contains);
    }
}
