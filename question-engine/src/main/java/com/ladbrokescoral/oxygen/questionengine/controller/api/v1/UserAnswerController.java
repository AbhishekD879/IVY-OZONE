package com.ladbrokescoral.oxygen.questionengine.controller.api.v1;

import com.ladbrokescoral.oxygen.questionengine.aspect.annotation.Authenticate;
import com.ladbrokescoral.oxygen.questionengine.aspect.annotation.StreamToBigQuery;
import com.ladbrokescoral.oxygen.questionengine.aspect.annotation.Username;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.QuizSubmitDto;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.UserAnswerDto;
import com.ladbrokescoral.oxygen.questionengine.model.UserAnswer;
import com.ladbrokescoral.oxygen.questionengine.service.UserAnswerService;
import com.newrelic.api.agent.Trace;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.util.UriComponents;
import org.springframework.web.util.UriComponentsBuilder;

import javax.validation.Valid;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/user-answer")
@Slf4j
public class UserAnswerController {

    private  UserAnswerService userAnswerService;

    @Autowired
    public UserAnswerController(UserAnswerService userAnswerService) {
        this.userAnswerService = userAnswerService;
    }

    @GetMapping("/{username}/{quiz-id}")
    @Authenticate
    @Trace
    public UserAnswerDto findById(@PathVariable @Username String username, @PathVariable("quiz-id") String quizId) {
        return userAnswerService.getById(new UserAnswer.Id(quizId, username));
    }

    @PostMapping
    @Authenticate
    @Trace
    @StreamToBigQuery
    public ResponseEntity<UserAnswerDto> save(@RequestBody @Valid @Username QuizSubmitDto quizSubmitDto,
                                              UriComponentsBuilder uriComponentsBuilder) {

        UserAnswerDto userAnswer = userAnswerService.save(quizSubmitDto);

        UriComponents uriComponents = uriComponentsBuilder.path("api/v1/user-answer/{username}/{quiz-id}")
                .buildAndExpand(quizSubmitDto.getUsername(), quizSubmitDto.getQuizId());

        HttpHeaders headers = new HttpHeaders();
        headers.setLocation(uriComponents.toUri());

        return new ResponseEntity<>(userAnswer, headers, HttpStatus.CREATED);
    }
}
