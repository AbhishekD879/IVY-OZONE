package com.ladbrokescoral.oxygen.questionengine.job;

import com.fasterxml.jackson.core.type.TypeReference;
import com.ladbrokescoral.oxygen.questionengine.configuration.ObjectMapperFactory;
import com.ladbrokescoral.oxygen.questionengine.configuration.properties.ApplicationProperties;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.AppQuizHistoryDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuizDto;
import com.ladbrokescoral.oxygen.questionengine.model.cms.Quiz;
import com.ladbrokescoral.oxygen.questionengine.model.cms.QuizHistory;
import com.ladbrokescoral.oxygen.questionengine.service.QuizService;
import com.ladbrokescoral.oxygen.questionengine.service.UpsellService;
import com.ladbrokescoral.oxygen.questionengine.service.impl.QuizCacheDataSourceImpl;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.cms.CmsService;
import org.junit.Assert;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.modelmapper.ModelMapper;
import org.springframework.cache.Cache;
import org.springframework.core.io.ClassPathResource;
import org.springframework.test.util.ReflectionTestUtils;

import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.mockito.ArgumentMatchers.any;

@RunWith(MockitoJUnitRunner.class)
public class RepopulateCachesSchedulerTest {

    @InjectMocks private RepopulateCachesScheduler repopulateCachesScheduler;

    @Mock private ModelMapper modelMapper;
    @Mock private Cache cache;
    @Mock private QuizCacheDataSourceImpl quizCacheDataSource;
    @Mock private CmsService cmsService;
    @Mock private ApplicationProperties applicationProperties;

    private Map<String, QuizHistory> quizHistoryMapCache;
    private AppQuizHistoryDto historyDto;


    @Before
    public void setUp() throws IOException {
        ReflectionTestUtils.setField(repopulateCachesScheduler, "quizHistoryCache", cache);
        ReflectionTestUtils.setField(repopulateCachesScheduler, "liveQuizCache", cache);

        QuizHistory quizHistory = new QuizHistory();
        quizHistory.setSourceId("/football");

        quizHistoryMapCache = new HashMap<>();
        quizHistoryMapCache.put("/football",quizHistory);
    }

    @Test
    public void tstPopulateHistoryCaches(){
        Mockito.when(quizCacheDataSource.getQuizHistory()).thenReturn(quizHistoryMapCache);
        Mockito.when(modelMapper.map(any(),any())).thenReturn(Mockito.mock(AppQuizHistoryDto.class));

        Assert.assertNotNull(quizHistoryMapCache);
        repopulateCachesScheduler.populateHistoryCaches();
    }

    @Test
    public void tstPopulateHistoryCachesWithEmptyQuizHistory(){
        Mockito.when(quizCacheDataSource.getQuizHistory()).thenReturn(new HashMap<>());

        Assert.assertNotNull(quizHistoryMapCache);
        repopulateCachesScheduler.populateHistoryCaches();
    }


}
