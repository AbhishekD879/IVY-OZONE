package com.ladbrokescoral.oxygen.questionengine.job;

import com.fasterxml.jackson.core.type.TypeReference;
import com.ladbrokescoral.oxygen.questionengine.configuration.ObjectMapperFactory;
import com.ladbrokescoral.oxygen.questionengine.model.cms.Quiz;
import com.ladbrokescoral.oxygen.questionengine.service.AbstractDataSource;
import com.ladbrokescoral.oxygen.questionengine.service.QuizService;
import com.ladbrokescoral.oxygen.questionengine.service.impl.QuizCacheDataSourceImpl;
import com.ladbrokescoral.oxygen.questionengine.service.impl.QuizDataSourceImpl;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.modelmapper.ModelMapper;
import org.springframework.core.io.ClassPathResource;
import org.springframework.test.util.ReflectionTestUtils;

import java.io.IOException;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.*;

@RunWith(MockitoJUnitRunner.class)
public class QuizCachesSchedulerTest {

    @InjectMocks
    private QuizCachesScheduler quizCachesScheduler;

    @Mock private  ModelMapper modelMapper;
    @Mock private  QuizService quizService;
    @Mock private  QuizCacheDataSourceImpl quizCacheDataSource;

    private List<Quiz> quizzes;

    @Before
    public void setUp() throws IOException {
         quizzes =  ObjectMapperFactory.getInstance().readValue(
                new ClassPathResource("/quizzes.json").getFile(),
                new TypeReference<List<Quiz>>() {});
    }

    @Test
    public void tstSaveQuizCaches(){
        ReflectionTestUtils.setField(quizCachesScheduler, "allPriviousQuizes", quizzes);
        setQuizzesMap();

        Assert.assertNotNull(quizCachesScheduler);
        quizCachesScheduler.saveQuizCaches();
    }

    @Test
    public void tstSaveQuizCachesWithEmptyQuizzesMap(){
        ReflectionTestUtils.setField(quizCachesScheduler, "quizzesMap", new HashMap<>());
        ReflectionTestUtils.setField(quizCachesScheduler, "allPriviousQuizes", quizzes);

        Assert.assertNotNull(quizCachesScheduler);
        quizCachesScheduler.saveQuizCaches();
    }

    @Test
    public void tstSaveQuizCachesWithEmptyPriviousQuizes(){
        ReflectionTestUtils.setField(quizCachesScheduler, "allPriviousQuizes", new ArrayList<>());
        setQuizzesMap();

        Assert.assertNotNull(quizCachesScheduler);
        quizCachesScheduler.saveQuizCaches();
    }

    @Test
    public void tstSaveQuizCachesWithEmptyQuizzes(){
        ReflectionTestUtils.setField(quizCachesScheduler, "allPriviousQuizes", new ArrayList<>());
        ReflectionTestUtils.setField(quizCachesScheduler, "quizzesMap", new HashMap<>());

        Assert.assertNotNull(quizCachesScheduler);
        quizCachesScheduler.saveQuizCaches();
    }

    @Test
    public void tstSaveQuizCachesWhenOneLiveQuizBecomesPrevious(){
        ReflectionTestUtils.setField(quizCachesScheduler, "allPriviousQuizes", quizzes);

        quizzes.get(0).setDisplayTo(Instant.now());
        QuizDataSourceImpl quizDataSource = new QuizDataSourceImpl();
        quizDataSource.addAll(quizzes);

        Map<String, AbstractDataSource<Quiz>> quizzesMap = new HashMap<>();
        quizzesMap.put("/footBall", quizDataSource);
        ReflectionTestUtils.setField(quizCachesScheduler, "quizzesMap", quizzesMap);

        Assert.assertNotNull(quizCachesScheduler);
        quizCachesScheduler.saveQuizCaches();
    }

    @Test
    public void tstWithEmptyQuizzesMapValue(){
        ReflectionTestUtils.setField(quizCachesScheduler, "allPriviousQuizes", quizzes);

        Map<String, AbstractDataSource<Quiz>> quizzesMap = new HashMap<>();
        quizzesMap.put("/footBall",new QuizDataSourceImpl());
        ReflectionTestUtils.setField(quizCachesScheduler, "quizzesMap", quizzesMap);

        Assert.assertNotNull(quizCachesScheduler);
        quizCachesScheduler.saveQuizCaches();
    }

    @Test
    public void tstGetQuizHistoryMapWhenLiveQuizzesNull(){
        List<Quiz> liveQuizzes = new ArrayList<>();
        liveQuizzes.add(null);

        Assert.assertNotNull(liveQuizzes);
        ReflectionTestUtils.setField(quizCachesScheduler, "allPriviousQuizes", quizzes);
        ReflectionTestUtils.invokeMethod(quizCachesScheduler,"getQuizHistoryMap",new HashMap<>(),liveQuizzes);
    }

    private void setQuizzesMap(){
        Instant displayTo = Instant.now().plus(2, ChronoUnit.HOURS);
        quizzes.stream().forEach(quiz -> quiz.setDisplayTo(displayTo));
        QuizDataSourceImpl quizDataSource = new QuizDataSourceImpl();
        quizDataSource.addAll(quizzes);

        Map<String, AbstractDataSource<Quiz>> quizzesMap = new HashMap<>();
        quizzesMap.put("/footBall", quizDataSource);
        ReflectionTestUtils.setField(quizCachesScheduler, "quizzesMap", quizzesMap);
    }





}
