package com.ladbrokescoral.oxygen.questionengine.service.impl;

import com.fasterxml.jackson.core.type.TypeReference;
import com.ladbrokescoral.oxygen.questionengine.configuration.ObjectMapperFactory;
import com.ladbrokescoral.oxygen.questionengine.model.cms.Quiz;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.core.io.ClassPathResource;

import java.io.IOException;
import java.time.Instant;
import java.util.Arrays;
import java.util.List;
import java.util.Queue;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;

@RunWith(MockitoJUnitRunner.class)
public class QuizDataSourceImplTest {

    @Mock
    private Queue<Quiz> quizCache;

    @InjectMocks
    private QuizDataSourceImpl quizDataSource;

    private Quiz quiz;

    @Before
    public void setUp() throws IOException {
        quiz =  ObjectMapperFactory.getInstance().readValue(
                new ClassPathResource("/quiz.json").getFile(),
                new TypeReference<Quiz>() {});
    }

    @Test
    public void tstQuizDataSource(){
        quizDataSource.addAll(Arrays.asList(quiz));
        Quiz quiz = new Quiz();
        quiz.setId("tst1");
        quiz.setDisplayFrom(Instant.parse("2022-04-20T05:18:07.148Z"));
        quiz.setDisplayTo(Instant.parse("2022-04-21T05:18:07.148Z"));
        quizDataSource.addAll(Arrays.asList(quiz));

        Quiz quiz1 = new Quiz();
        quiz1.setId("tst12");
        quiz1.setDisplayFrom(Instant.parse("2022-02-20T05:18:07.148Z"));
        quiz1.setDisplayTo(Instant.parse("2022-02-21T05:18:07.148Z"));
        quizDataSource.addAll(Arrays.asList(quiz1));

        Quiz quiz2 = new Quiz();
        quiz2.setId("tst123");
        quiz2.setDisplayFrom(Instant.parse("2022-02-20T05:18:07.148Z"));
        quiz2.setDisplayTo(Instant.parse("2022-02-21T05:18:07.148Z"));
        quizDataSource.addAll(Arrays.asList(quiz2));

        assertNotNull(quizDataSource.getPeek());
        assertEquals(4, quizDataSource.size());
        assertEquals(false, quizDataSource.isEmpty());
        assertEquals("tst12", quizDataSource.getPoll().getId());
        quizDataSource.clear();
        assertEquals(0, quizDataSource.size());
    }


}
