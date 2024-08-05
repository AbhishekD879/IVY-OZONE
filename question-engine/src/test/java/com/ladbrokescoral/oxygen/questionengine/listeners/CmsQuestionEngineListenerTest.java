package com.ladbrokescoral.oxygen.questionengine.listeners;

import com.fasterxml.jackson.core.type.TypeReference;
import com.ladbrokescoral.oxygen.event.PublicApiEvent;
import com.ladbrokescoral.oxygen.model.ApiCollectionConfig;
import com.ladbrokescoral.oxygen.questionengine.configuration.ObjectMapperFactory;
import com.ladbrokescoral.oxygen.questionengine.model.cms.Quiz;
import com.ladbrokescoral.oxygen.questionengine.service.AbstractDataSource;
import com.ladbrokescoral.oxygen.questionengine.service.QuizService;
import com.ladbrokescoral.oxygen.service.CmsService;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.core.io.ClassPathResource;
import org.springframework.test.util.ReflectionTestUtils;

import java.io.IOException;
import java.util.*;

import static org.junit.Assert.assertNotNull;
import static org.mockito.ArgumentMatchers.anyString;

@RunWith(MockitoJUnitRunner.class)
public class CmsQuestionEngineListenerTest {

    @InjectMocks
    private CmsQuestionEngineListener cmsQuestionEngineListener;

    List<String> endPoints;

    Map<String,List<String>> hashMap;

    List<ApiCollectionConfig> apiCollectionConfig;

    List<Quiz> quizzes;

    @Mock
    private CmsService cmsService;

    @Mock
    private QuizService quizService;

    @Mock
    private List<Quiz> allPriviousQuizes;

    @Mock
    private Map<String, AbstractDataSource<Quiz>> quizzesMap;

    @Before
    public void setUp() throws IOException {
        endPoints = new ArrayList<>();
        hashMap = new HashMap<>();
        apiCollectionConfig = ObjectMapperFactory.getInstance().readValue(
                new ClassPathResource("/configMap.json").getFile(),
                new TypeReference<List<ApiCollectionConfig>>() {});

        quizzes = ObjectMapperFactory.getInstance().readValue(
                new ClassPathResource("/quizzes.json").getFile(),
                new TypeReference<List<Quiz>>() {});
        hashMap.put("/question-engine",new ArrayList<>());
        hashMap.get("/question-engine").add("quiz");
        endPoints.addAll(hashMap.keySet());
        ReflectionTestUtils.setField(cmsQuestionEngineListener,"configMap",hashMap);
        ReflectionTestUtils.setField(cmsQuestionEngineListener,"endpoints",endPoints);
        ReflectionTestUtils.setField(cmsQuestionEngineListener,"brand","ladbrokes");
    }

    @Test
    public void tstWithEmptyCollectionName(){
        PublicApiEvent event = new PublicApiEvent("cms", "/question-engine", "");
        assertNotNull(cmsQuestionEngineListener);
        cmsQuestionEngineListener.onApplicationEvent(event);
    }

    @Test
    public void configMapChangeTest(){
        PublicApiEvent event = new PublicApiEvent("cms", "/question-engine", "configMap");
        assertNotNull(cmsQuestionEngineListener);
        Mockito.when(cmsService.apiCollectionConfig(anyString())).thenReturn(apiCollectionConfig);
        cmsQuestionEngineListener.onApplicationEvent(event);
    }

    @Test
    public void configMapChangeFoundCmsDataEmptyTest() {
        PublicApiEvent event = new PublicApiEvent("cms", "/question-engine", "configMap");
        assertNotNull(apiCollectionConfig);
        Mockito.when(cmsService.apiCollectionConfig(anyString())).thenReturn(new ArrayList<>());
        cmsQuestionEngineListener.onApplicationEvent(event);
    }

    @Test
    public void quizEventTest() {
        PublicApiEvent event = new PublicApiEvent("cms", "/question-engine", "quiz");
        assertNotNull(event);
        Mockito.doNothing().when(quizService).findPreviousLiveAndFutureQuizzes();
        cmsQuestionEngineListener.onApplicationEvent(event);
    }

    @Test
    public void quizEventTestWithEmptyConfigMapValue() {
        PublicApiEvent event = new PublicApiEvent("cms", "/question-engine", "quiz");
        assertNotNull(event);

        Map<String,List<String>> configMap = new HashMap<>();
        configMap.put("/question-engine", null);

        ReflectionTestUtils.setField(cmsQuestionEngineListener,"configMap", configMap);
        cmsQuestionEngineListener.onApplicationEvent(event);
    }

    @Test
    public void quizEventTestWithWrongEndPts() {
        PublicApiEvent event = new PublicApiEvent("cms", "/question-engine", "quiz");
        assertNotNull(event);

        ReflectionTestUtils.setField(cmsQuestionEngineListener,"endpoints",new ArrayList<>());
        cmsQuestionEngineListener.onApplicationEvent(event);
    }

}
