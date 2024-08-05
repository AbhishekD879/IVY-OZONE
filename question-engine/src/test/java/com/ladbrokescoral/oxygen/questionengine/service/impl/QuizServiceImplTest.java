package com.ladbrokescoral.oxygen.questionengine.service.impl;

import com.fasterxml.jackson.core.type.TypeReference;
import com.ladbrokescoral.oxygen.questionengine.configuration.ObjectMapperFactory;
import com.ladbrokescoral.oxygen.questionengine.model.cms.Quiz;
import com.ladbrokescoral.oxygen.questionengine.service.AbstractDataSource;
import com.ladbrokescoral.oxygen.questionengine.service.QuizHistoryService;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.cms.CmsService;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.modelmapper.ModelMapper;
import org.springframework.core.io.ClassPathResource;

import java.io.IOException;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

@RunWith(MockitoJUnitRunner.class)
public class QuizServiceImplTest {

    @InjectMocks private QuizServiceImpl quizService;

    @Mock private CmsService cmsService;
    @Mock private QuizHistoryService quizHistoryService;
    @Mock private ModelMapper modelMapper;
    @Mock private List<Quiz> allPriviousQuizes;
    @Mock private Map<String, AbstractDataSource<Quiz>> quizzesMap;

    private List<Quiz> quizzes;

    @Before
    public void setUp() throws IOException {
        quizzes = ObjectMapperFactory.getInstance().readValue(
                new ClassPathResource("/quizzes.json").getFile(),
                new TypeReference<List<Quiz>>() {});

        Quiz quiz = new Quiz();
        quiz.setDisplayFrom(Instant.parse("2022-03-20T05:18:07.148Z"));
        quiz.setDisplayTo(Instant.now());
        quiz.setActive(true);
        quizzes.add(quiz);
    }

    @Test
    public void tstFindPreviousLiveAndFutureQuizzes(){
        Mockito.when(quizHistoryService.getAllQuizzes()).thenReturn(quizzes);

        quizService.findPreviousLiveAndFutureQuizzes();
        Assert.assertNotNull(allPriviousQuizes);
        Assert.assertNotNull(quizzesMap);
    }

    @Test
    public void tstWhenQuizzesIsNull(){
        Mockito.when(quizHistoryService.getAllQuizzes()).thenReturn(null);

        Assert.assertNotNull(quizService);
        quizService.findPreviousLiveAndFutureQuizzes();
    }

}
