package com.ladbrokescoral.oxygen.questionengine.crm;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.AppQuizHistoryDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.CoinDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.PrizeDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuizDto;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.QuizSubmitDto;
import com.ladbrokescoral.oxygen.questionengine.model.cms.PrizeType;
import com.ladbrokescoral.oxygen.questionengine.repository.AwardFailureRepository;
import com.ladbrokescoral.oxygen.questionengine.service.QuizHistoryService;
import okhttp3.OkHttpClient;
import okhttp3.mock.MockInterceptor;

import org.junit.Before;
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.web.reactive.function.client.WebClient;
import uk.co.jemos.podam.api.PodamFactory;
import uk.co.jemos.podam.api.PodamFactoryImpl;

import javax.net.ssl.SSLException;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import static okhttp3.mock.MediaTypes.MEDIATYPE_JSON;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class CrmServiceImplTest {

    CrmServiceImpl crmService;
    @Mock
    QuizHistoryService quizService;

    @Mock
    AwardFailureRepository failureRepository;
    private static final String SOURCE_ID = "/123";
    private static final String ID = "12345";
    private PodamFactory factory = new PodamFactoryImpl();
    List<String> crmErrorCodes = List.of("ER101", "ER102", "ER104", "ER999", "ER998", "ER997");
    private MockInterceptor interceptor;
    @Mock
    CrmEndPoint crmEndPoint;

    @BeforeEach
    public void init() {
        interceptor = new MockInterceptor();
        OkHttpClient client = new OkHttpClient.Builder().addInterceptor(interceptor).build();
        crmService = new CrmServiceImpl("http://test.com", client, quizService, failureRepository);
    }

    @Test
    void getAwardTest() {
        ReflectionTestUtils.setField(crmService, "crmErrorCodes", crmErrorCodes);
        when(quizService.findQuizHistory(any())).thenReturn(getAppHistoryLive());
        interceptor
                .addRule()
                .post(
                        "http://test.com/api/rest/v1/reward/awardAPI")
                .respond(getResourceFileAsString("award.json").toString());
        QuizSubmitDto quizSubmitDto = getQuizSubmitModel();
        String awardStatus = crmService.getAward(quizSubmitDto);
        Assertions.assertNotNull(awardStatus);
    }

    @Test
    void getAwardTestPrizeTypeNONE() {
        ReflectionTestUtils.setField(crmService, "crmErrorCodes", crmErrorCodes);
        when(quizService.findQuizHistory(any())).thenReturn(getAppHistoryNONE());
        interceptor
                .addRule()
                .post(
                        "http://test.com/api/rest/v1/reward/awardAPI")
                .respond(getResourceFileAsString("award.json").toString());
        QuizSubmitDto quizSubmitDto = getQuizSubmitModel();
        String awardStatus = crmService.getAward(quizSubmitDto);
        Assertions.assertNotNull(awardStatus);
    }

    @Test
    void getAwardCrmSuccessCodeTest() {
        ReflectionTestUtils.setField(crmService, "crmErrorCodes", crmErrorCodes);
        when(quizService.findQuizHistory(any())).thenReturn(getAppHistory());
        interceptor
                .addRule()
                .post(
                        "http://test.com/api/rest/v1/reward/awardAPI")
                .respond(getResourceFileAsString("awardSucess.json").toString());
        QuizSubmitDto quizSubmitDto = getQuizSubmitModel();
        String awardStatus = crmService.getAward(quizSubmitDto);
        Assertions.assertNotNull(awardStatus);
    }

    @Test
    void getAwardCrmErrorCodeTest() {
        ReflectionTestUtils.setField(crmService, "crmErrorCodes", crmErrorCodes);
        when(quizService.findQuizHistory(any())).thenReturn(getAppHistoryCoinEmpty());
        interceptor
                .addRule()
                .post(
                        "http://test.com/api/rest/v1/reward/awardAPI")
                .respond(getResourceFileAsString("awarderrorcode.json").toString());
        QuizSubmitDto quizSubmitDto = getQuizSubmitModel();
        String awardStatus = crmService.getAward(quizSubmitDto);
        Assertions.assertNotNull(awardStatus);
    }

    @Test
    void getAwardCrmErrorCodeWithCoinTest() {
        ReflectionTestUtils.setField(crmService, "crmErrorCodes", crmErrorCodes);
        when(quizService.findQuizHistory(any())).thenReturn(getAppHistoryCrmErrorCode());
        interceptor
                .addRule()
                .post(
                        "http://test.com/api/rest/v1/reward/awardAPI")
                .respond(getResourceFileAsString("awarderrorcode.json").toString());
        QuizSubmitDto quizSubmitDto = getQuizSubmitModel();
        String awardStatus = crmService.getAward(quizSubmitDto);
        Assertions.assertNotNull(awardStatus);
    }

    @Test
    void getAwardJsonTest() {
        ReflectionTestUtils.setField(crmService, "crmErrorCodes", crmErrorCodes);
        when(quizService.findQuizHistory(any())).thenReturn(getAppHistoryLive());
        interceptor
                .addRule()
                .post(
                        "http://test.com/api/rest/v1/reward/awardAPI")
                .respond(getAppHistoryLive().toString());
        QuizSubmitDto quizSubmitDto = getQuizSubmitModel();
        String awardStatus = crmService.getAward(quizSubmitDto);
        Assertions.assertNotNull(awardStatus);
    }

    @Test
    void getAwardTest_error() {
        ReflectionTestUtils.setField(crmService, "crmErrorCodes", crmErrorCodes);
        when(quizService.findQuizHistory(any())).thenReturn(getAppHistoryLive());
        interceptor
                .addRule()
                .post(
                        "http://test.com/api/rest/v1/reward/awardAPI")
                .respond(404);
        QuizSubmitDto quizSubmitDto = getQuizSubmitModel();
        String awardStatus = crmService.getAward(quizSubmitDto);
        Assertions.assertNotNull(awardStatus);
    }

    @Test
    void getAwardErrorBodyTest() {
        ReflectionTestUtils.setField(crmService, "crmErrorCodes", crmErrorCodes);
        when(quizService.findQuizHistory(any())).thenReturn(getAppHistoryLive());
        interceptor
                .addRule()
                .post(
                        "http://test.com/api/rest/v1/reward/awardAPI")
                .respond("Ok");
        QuizSubmitDto quizSubmitDto = getQuizSubmitModel();
        String awardStatus = crmService.getAward(quizSubmitDto);
        Assertions.assertNotNull(awardStatus);
    }

    private QuizSubmitDto getQuizSubmitModel() {
        return factory.manufacturePojo(QuizSubmitDto.class)
                .setQuizId(ID)
                .setSourceId(SOURCE_ID);
    }

    protected String getResourceFileAsString(String resourceFileName) {
        InputStream is = getClass().getClassLoader().getResourceAsStream(resourceFileName);
        BufferedReader reader = new BufferedReader(new InputStreamReader(is));
        return reader.lines().collect(Collectors.joining("\n"));
    }

    private AppQuizHistoryDto getAppHistoryCoinEmpty() {
        AppQuizHistoryDto appHistory = new AppQuizHistoryDto();
        QuizDto live = new QuizDto();
        Map<Integer, PrizeDto> correctAnswersPrizes = new HashMap<>();
        /*PrizeDto prizeDto = new PrizeDto();
        prizeDto.setPrizeType(PrizeType.COIN);
        correctAnswersPrizes.put(0, prizeDto);*/
       /* CoinDto coinDto = new CoinDto();
        coinDto.setValue(null);*/
        live.setCoin(null);
        live.setCorrectAnswersPrizes(correctAnswersPrizes);
        appHistory.setLive(live);
        return appHistory;
    }

    private AppQuizHistoryDto getAppHistoryCrmErrorCode() {
        AppQuizHistoryDto appHistory = new AppQuizHistoryDto();
        QuizDto live = new QuizDto();
        Map<Integer, PrizeDto> correctAnswersPrizes = new HashMap<>();
        PrizeDto prizeDto = new PrizeDto();
        prizeDto.setPrizeType(PrizeType.COIN);
        correctAnswersPrizes.put(0, prizeDto);
        CoinDto coinDto = new CoinDto();
        coinDto.setValue(null);
        live.setCoin(coinDto);
        live.setCorrectAnswersPrizes(correctAnswersPrizes);
        appHistory.setLive(live);
        return appHistory;
    }

    private AppQuizHistoryDto getAppHistory() {
        AppQuizHistoryDto appHistory = new AppQuizHistoryDto();
        QuizDto live = new QuizDto();
        Map<Integer, PrizeDto> correctAnswersPrizes = new HashMap<>();
        PrizeDto prizeDto = new PrizeDto();
        prizeDto.setPrizeType(PrizeType.COIN);
        correctAnswersPrizes.put(0, prizeDto);
        CoinDto coinDto = new CoinDto();
        coinDto.setSiteCoreId(null);
        coinDto.setValue(null);
        live.setCoin(coinDto);
        live.setCorrectAnswersPrizes(correctAnswersPrizes);
        appHistory.setLive(live);
        return appHistory;
    }

    private AppQuizHistoryDto getAppHistoryNONE() {
        AppQuizHistoryDto appHistory = new AppQuizHistoryDto();
        QuizDto live = new QuizDto();
        Map<Integer, PrizeDto> correctAnswersPrizes = new HashMap<>();
        PrizeDto prizeDto = new PrizeDto();
        prizeDto.setPrizeType(PrizeType.NONE);
        correctAnswersPrizes.put(0, prizeDto);
        CoinDto coinDto = new CoinDto();
        coinDto.setValue(12);
        coinDto.setSiteCoreId("Test123");
        live.setCoin(coinDto);
        live.setCorrectAnswersPrizes(correctAnswersPrizes);
        appHistory.setLive(live);
        return appHistory;
    }

    private AppQuizHistoryDto getAppHistoryLive() {
        AppQuizHistoryDto appHistory = new AppQuizHistoryDto();
        QuizDto live = new QuizDto();
        Map<Integer, PrizeDto> correctAnswersPrizes = new HashMap<>();
        PrizeDto prizeDto = new PrizeDto();
        prizeDto.setPrizeType(PrizeType.COIN);
        correctAnswersPrizes.put(0, prizeDto);
        CoinDto coinDto = new CoinDto();
        coinDto.setSiteCoreId(null);
        coinDto.setValue(12);
        live.setCoin(coinDto);
        live.setCorrectAnswersPrizes(correctAnswersPrizes);
        appHistory.setLive(live);
        return appHistory;
    }
}
